"""
Date: 2022.05.11 14:00
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.11 14:00
"""

# # HTTP/2 Tutorial

# This tutorial aims at creating an HTTP/2 session using Scapy. The frontpage of Google will be fetched. The favicon will also be loaded as a dependency of the frontpage. Finally, a Google query will be submitted. The first queries will be generated using some Scapy helpers. The last one will be generated by hand, to better illustrate the low level APIs.
#
# This tutorial can be run without any privileges (no root, no CAP_NET_ADMIN, no CAP_NET_RAW). One can select "Cell -> Run All" to perform the three queries.

# ## Building the socket

# First, we need to build an TLS socket to the HTTP server, and to negotiate the HTTP/2 protocol as the next protocol. Doing so requires a fairly recent version of the Python ssl module. We indeed need support of ALPN (https://www.rfc-editor.org/rfc/rfc7301.txt).
# We build our TCP socket first.

# In[99]:


import socket

dn = "www.google.fr"

# Get the IP address of a Google HTTP endpoint
l = socket.getaddrinfo(
    dn, 443, socket.INADDR_ANY, socket.SOCK_STREAM, socket.IPPROTO_TCP
)
assert len(l) > 0, "No address found :("

s = socket.socket(l[0][0], l[0][1], l[0][2])
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if hasattr(socket, "SO_REUSEPORT"):
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
ip_and_port = l[0][4]

# We now build our SSL context and we wrap the previously defined socket in it.

# In[100]:


import ssl

# Testing support for ALPN
assert ssl.HAS_ALPN

# Building the SSL context
ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_ctx.set_ciphers(
    ":".join(
        [  # List from ANSSI TLS guide v.1.1 p.51
            "ECDHE-ECDSA-AES256-GCM-SHA384",
            "ECDHE-RSA-AES256-GCM-SHA384",
            "ECDHE-ECDSA-AES128-GCM-SHA256",
            "ECDHE-RSA-AES128-GCM-SHA256",
            "ECDHE-ECDSA-AES256-SHA384",
            "ECDHE-RSA-AES256-SHA384",
            "ECDHE-ECDSA-AES128-SHA256",
            "ECDHE-RSA-AES128-SHA256",
            "ECDHE-ECDSA-CAMELLIA256-SHA384",
            "ECDHE-RSA-CAMELLIA256-SHA384",
            "ECDHE-ECDSA-CAMELLIA128-SHA256",
            "ECDHE-RSA-CAMELLIA128-SHA256",
            "DHE-RSA-AES256-GCM-SHA384",
            "DHE-RSA-AES128-GCM-SHA256",
            "DHE-RSA-AES256-SHA256",
            "DHE-RSA-AES128-SHA256",
            "AES256-GCM-SHA384",
            "AES128-GCM-SHA256",
            "AES256-SHA256",
            "AES128-SHA256",
            "CAMELLIA128-SHA256",
        ]
    )
)
ssl_ctx.set_alpn_protocols(["h2"])  # h2 is a RFC7540-hardcoded value
ssl_sock = ssl_ctx.wrap_socket(s, server_hostname=dn)

# We then connect the socket to the TCP endpoint.

# In[101]:


ssl_sock.connect(ip_and_port)
assert "h2" == ssl_sock.selected_alpn_protocol()

# ## Reading the server settings and acknowledging them.

# With HTTP/2, the server is the first to talk, sending its settings for the HTTP/2 session. Let's read them. For this, we wrap the TLS connection into a Scapy SuperSocket for easier management.

# In[102]:


import scapy.supersocket as supersocket
import scapy.contrib.http2 as h2
import scapy.config

scapy.config.conf.debug_dissector = True
ss = supersocket.SSLStreamSocket(ssl_sock, basecls=h2.H2Frame)
srv_set = ss.recv()
srv_set.show()

# Let's make a note of the server settings for later usage.
# We define variables for the server settings. They are assigned the RFC-defined default values. These values are overwritten by the settings provided by the server, if they are provided.

# In[103]:


srv_max_frm_sz = 1 << 14
srv_hdr_tbl_sz = 4096
srv_max_hdr_tbl_sz = 0
srv_global_window = 1 << 14
for setting in srv_set.payload.settings:
    if setting.id == h2.H2Setting.SETTINGS_HEADER_TABLE_SIZE:
        srv_hdr_tbl_sz = setting.value
    elif setting.id == h2.H2Setting.SETTINGS_MAX_HEADER_LIST_SIZE:
        srv_max_hdr_lst_sz = setting.value
    elif setting.id == h2.H2Setting.SETTINGS_INITIAL_WINDOW_SIZE:
        srv_global_window = setting.value

# HTTP/2 is a very polite protocol. We need to acknowledge the server settings. For this, we first need to send a constant string, which is a connection preface. This serves the purpose of confirming to the server that the HTTP/2 protocol is understood by the client. Scapy builds the appropriate packet for us to send from this constant string.

# In[104]:


import scapy.packet as packet

# We verify that the server window is large enough for us to send some data.
srv_global_window -= len(h2.H2_CLIENT_CONNECTION_PREFACE)
assert srv_global_window >= 0

ss.send(packet.Raw(h2.H2_CLIENT_CONNECTION_PREFACE))

# Then, we build the acknowledgment frame and we send our own settings in another frame. We will define very LARGE values (maximum values as defined in the RFC7540, in most cases), just so that we don't end up having to handle window management in this tutorial.

# In[105]:


set_ack = h2.H2Frame(flags={"A"}) / h2.H2SettingsFrame()
set_ack.show()

# In[106]:


own_set = h2.H2Frame() / h2.H2SettingsFrame()
max_frm_sz = (1 << 24) - 1
max_hdr_tbl_sz = (1 << 16) - 1
win_sz = (1 << 31) - 1
own_set.settings = [
    h2.H2Setting(id=h2.H2Setting.SETTINGS_ENABLE_PUSH, value=0),
    h2.H2Setting(id=h2.H2Setting.SETTINGS_INITIAL_WINDOW_SIZE, value=win_sz),
    h2.H2Setting(id=h2.H2Setting.SETTINGS_HEADER_TABLE_SIZE, value=max_hdr_tbl_sz),
    h2.H2Setting(id=h2.H2Setting.SETTINGS_MAX_FRAME_SIZE, value=max_frm_sz),
]

# We then send the two frames and then read the acknowledgment of our settings from the server. We set up a loop because the first frames that we may read could be PING frames or window management frames.

# In[107]:


h2seq = h2.H2Seq()
h2seq.frames = [set_ack, own_set]
# We verify that the server window is large enough for us to send our frames.
srv_global_window -= len(str(h2seq))
assert srv_global_window >= 0
ss.send(h2seq)

# Loop until an acknowledgement for our settings is received
new_frame = None
while isinstance(new_frame, type(None)) or not (
    new_frame.type == h2.H2SettingsFrame.type_id and "A" in new_frame.flags
):
    if not isinstance(new_frame, type(None)):
        # If we received a frame about window management
        if new_frame.type == h2.H2WindowUpdateFrame.type_id:
            # For this tutorial, we don't care about stream-specific windows, but we should :)
            if new_frame.stream_id == 0:
                srv_global_window += new_frame.payload.win_size_incr
        # If we received a Ping frame, we acknowledge the ping,
        # just by setting the ACK flag (A), and sending back the query
        elif new_frame.type == h2.H2PingFrame.type_id:
            new_flags = new_frame.getfieldval("flags")
            new_flags.add("A")
            new_frame.flags = new_flags
            srv_global_window -= len(str(new_frame))
            assert srv_global_window >= 0
            ss.send(new_frame)
        else:
            assert (
                new_frame.type != h2.H2ResetFrame.type_id
                and new_frame.type != h2.H2GoAwayFrame.type_id
            ), "Error received; something is not right!"
    try:
        new_frame = ss.recv()
        new_frame.show()
    except:
        import time

        time.sleep(1)
        new_frame = None

# ## Build the form query with the helpers

# We are now building a query for the frontpage https://www.google.fr/. We use the HTTP/2 Scapy Module helpers to build this query. The parse_txt_hdrs helper receives various parameters regarding the size of the header blocks and the frame to automatically split the values on multiple frames, if need be. It also receives two callbacks to know which flavour of HPack header encoding we should apply.
#
# We either use the server settings if they were specified or the default values.
#
# You may note that we say that cookies are sensitive, regardless of their content. We would do something a bit smarter, if we knew what is the name of the cookies that are sensitive, and those that are merely informative. In HTTP/2 cookies are split into multiple "cookie" headers, while in HTTP/1.1, they are all stored inside the same header.
#
# As the client of this HTTP/2 connection, we need to use odd stream ids, per RFC7540. Since this is the first query, we will use the stream id 1.

# In[108]:


tblhdr = h2.HPackHdrTable()
qry_frontpage = tblhdr.parse_txt_hdrs(
    """:method GET
    :path /
    :authority www.google.fr
    :scheme https
    accept-encoding: gzip, deflate
    accept-language: fr-FR
    accept: text/html
    user-agent: Scapy HTTP/2 Module
    """,
    stream_id=1,
    max_frm_sz=srv_max_frm_sz,
    max_hdr_lst_sz=srv_max_hdr_lst_sz,
    is_sensitive=lambda hdr_name, hdr_val: hdr_name in ["cookie"],
    should_index=lambda x: x
    in [
        "x-requested-with",
        "user-agent",
        "accept-language",
        ":authority",
        "accept",
    ],
)
qry_frontpage.show()

# The previous helper updated the HPackHdrTable structure with the headers that should be indexed. We don't need to look inside that table if we only use helpers. For the sake of this tutorial, though, we will.

# In[109]:


for i in range(
    max(tblhdr._static_entries.keys()) + 1,
    max(tblhdr._static_entries.keys()) + 1 + len(tblhdr._dynamic_table),
):
    print("Header: {} Value: {}".format(tblhdr[i].name(), tblhdr[i].value()))

# We also build a query for the favicon.

# In[110]:


qry_icon = tblhdr.parse_txt_hdrs(
    """:method GET
    :path /favicon.ico
    :authority www.google.fr
    :scheme https
    accept-encoding: gzip, deflate
    accept-language: fr-FR
    accept: image/x-icon; image/vnd.microsoft.icon
    user-agent: Scapy HTTP/2 Module
    """,
    stream_id=3,
    max_frm_sz=srv_max_frm_sz,
    max_hdr_lst_sz=srv_max_hdr_tbl_sz,
    is_sensitive=lambda hdr_name, hdr_val: hdr_name in ["cookie"],
    should_index=lambda x: x
    in [
        "x-requested-with",
        "user-agent",
        "accept-language",
        ":authority",
        "accept",
    ],
)
qry_icon.show()

# You may note that several of the headers that are in common between the two queries (the one for the frontpage and the one for the /favicon.ico) are compressed in the second query. They are only referred to by an index number of the dynamic HPack Header Table.
# We now alter the favicon query to be dependent of the query for the form.

# In[111]:


real_qry_icon = h2.H2Frame(
    stream_id=qry_icon.frames[0][h2.H2Frame].stream_id,
    flags={"+"}.union(qry_icon.frames[0][h2.H2Frame].flags),
) / h2.H2PriorityHeadersFrame(
    hdrs=qry_icon.frames[0][h2.H2HeadersFrame].hdrs,
    stream_dependency=1,
    weight=32,
    exclusive=0,
)
real_qry_icon.show()

# We can now send both queries to the server.

# In[112]:


h2seq = h2.H2Seq()
h2seq.frames = [qry_frontpage.frames[0], real_qry_icon]
srv_global_window -= len(str(h2seq))
assert srv_global_window >= 0
ss.send(h2seq)

# Let's read the answers!

# In[113]:


# The stream variable will contain all read frames; we will read on until stream 1 and stream 3 are closed by the server.
stream = h2.H2Seq()
# Number of streams closed by the server
closed_stream = 0

new_frame = None
while True:
    if not isinstance(new_frame, type(None)):
        if new_frame.stream_id in [1, 3]:
            stream.frames.append(new_frame)
            if "ES" in new_frame.flags:
                closed_stream += 1
        # If we read a PING frame, we acknowledge it by sending the same frame back, with the ACK flag set.
        elif new_frame.stream_id == 0 and new_frame.type == h2.H2PingFrame.type_id:
            new_flags = new_frame.getfieldval("flags")
            new_flags.add("A")
            new_frame.flags = new_flags
            ss.send(new_frame)

        # If two streams were closed, we don't need to perform the next operations
        if closed_stream >= 2:
            break
    try:
        new_frame = ss.recv()
        new_frame.show()
    except:
        import time

        time.sleep(1)
        new_frame = None

stream.show()

# Now, I don't know about you, but I can't read this :) Let's use the helpers to help us out.
#
# First we need to create a new Header table that is meaningful for headers received from the server. We set the various sizes to the values we defined in our settings.

# In[114]:


srv_tblhdr = h2.HPackHdrTable(
    dynamic_table_max_size=max_hdr_tbl_sz, dynamic_table_cap_size=max_hdr_tbl_sz
)

# Let's now convert all received headers into their textual representation, and stuff the data frames into a buffer per stream.

# In[115]:


# Structure used to store textual representation of the stream headers
stream_txt = {}
# Structure used to store data from each stream
stream_data = {}

# For each frame we previously received
for frame in stream.frames:
    # If this frame is a header
    if frame.type == h2.H2HeadersFrame.type_id:
        # Convert this header block into its textual representation.
        # For the sake of simplicity of this tutorial, we assume
        # that the header block is not large enough to require a Continuation frame
        stream_txt[frame.stream_id] = srv_tblhdr.gen_txt_repr(frame)
    # If this frame is data
    if frame.type == h2.H2DataFrame.type_id:
        if frame.stream_id not in stream_data:
            stream_data[frame.stream_id] = []
        stream_data[frame.stream_id].append(frame)

# Now, we can print the headers from the Favicon response.

# In[116]:


print(stream_txt[3])

# So, we received a 200 status code, meaning that we received the favicon. We also can see that the favicon is GZipped. Let's uncompress it and display it in this notebook.

# In[117]:


import zlib

img = zlib.decompress(stream_data[3][0].data, 16 + zlib.MAX_WBITS)
from IPython.core.display import HTML

HTML('<img src="data:image/x-icon;base64,{}" />'.format(img.encode("base64")))

# Let's now read the frontpage response.

# In[118]:


print(stream_txt[1])

# So, we received a status code 200, which means that we received a page. Let's "visualize it".

# In[119]:


data = ""
for frgmt in stream_data[1]:
    data += frgmt.payload.data

HTML(zlib.decompress(data, 16 + zlib.MAX_WBITS).decode("UTF-8", "ignore"))

# ## Throwing a query!

# Let's now query Google! For this, we will build a new query without the helpers, to explore the low-level parts of the HTTP/2 Scapy module.
# First, we will get the cookie that we were given. For this, we will search for the set-cookie header that we received.

# In[120]:


from io import BytesIO

sio = BytesIO(stream_txt[1])
cookie = [
    val[len("set-cookie: ") :].strip() for val in sio if val.startswith("set-cookie: ")
]
print(cookie)

# Now, we build the query by hand. Let's create the Header frame, so that we can later stuff all the header "lines" in it. This is a new stream, and we already used the stream ids 1 and 3, so we will use the stream id 5, which is the next available. We will set the "End Stream" and "End Headers" flags. The End Stream flag means that they are no more frames (except header frames...) after this one in this stream. The End Headers flag means that there are no Continuation frames after this frame. Continuation frames can be used to add more headers than one could fit in previous H2HeaderFrame and Continuation frames...
#
# Our frame will contain little headers and we set very large limits for this tutorial, so we will skip all the checks, but they should be done! The helpers does them, by the way.

# In[121]:


hdrs_frm = h2.H2Frame(flags={"ES", "EH"}, stream_id=5) / h2.H2HeadersFrame()

# Then, we have to specify the pseudo headers. These headers are the equivalent of "GET / HTTP/1.1\nHost: www.google.fr" of old.
# For this, we specify that this is a GET query over HTTPS, along with the path, and the "authority", which is the new "Host:".The GET Method and the HTTPS scheme are part of the static HPack table, according to RFC7541. Let's get the index of these headers and put them into HPackIndexedHdr packets.

# In[122]:


get_hdr_idx = tblhdr.get_idx_by_name_and_value(":method", "GET")
get_hdr = h2.HPackIndexedHdr(index=get_hdr_idx)
get_hdr.show()
hdrs_frm.payload.hdrs.append(get_hdr)

https_hdr_idx = tblhdr.get_idx_by_name_and_value(":scheme", "https")
https_hdr = h2.HPackIndexedHdr(index=https_hdr_idx)
https_hdr.show()
hdrs_frm.payload.hdrs.append(https_hdr)

# For the path, we will use "/search?q=scapy". The path might be a sensitive value, since it may contain values that we might not want to leak via side-channel attacks (here the query topic). For this reason, we will specify the path using a HPackLitHdrFldWithoutIndexing, which means that we don't want indexing. We also need to set the never_index bit, so that if there are intermediaries between us and the HTTP server, they will not try to compress this header.
# Before setting this header, though, we have to choose whether we want to compress the *string* "/search?q=scapy" using Huffman encoding. Let's compress it and compare its wire-length with the uncompressed version.

# In[123]:


z_str = h2.HPackZString("/search?q=scapy")
unz_str = h2.HPackLiteralString("/search?q=scapy")

print(len(str(z_str)), len(str(unz_str)))

# So the compressed version is smaller. Let's use it, since HTTP/2 is all about performances and compression.
#
# ":path" is the pseudo-header to define the query path. While we don't want to compress the *value* of the query path, the name can be compressed. As it happens, the ":path" header name is in the static header table. For this reason, we will search of its index, and then build the header.

# In[124]:


path_hdr_idx = tblhdr.get_idx_by_name(":path")
path_str = h2.HPackHdrString(data=z_str)
path_hdr = h2.HPackLitHdrFldWithoutIndexing(
    never_index=1, index=path_hdr_idx, hdr_value=path_str
)
path_hdr.show()
hdrs_frm.payload.hdrs.append(path_hdr)

# The final missing pseudo-header is the new "Host" header, called ":authority". ":authority" is in the static header table, so we *could* use it. As it happens, we can do better because we previously indexed ":authority" *with the value* "www.google.fr". Let's search for the index of this entry in the dynamic table. With luck, the server header table size is large enough so that the value is still inside it.

# In[125]:


host_hdr_idx = tblhdr.get_idx_by_name_and_value(":authority", dn)
assert not isinstance(host_hdr_idx, type(None))
print(host_hdr_idx)

# So, the ":authority www.google.fr" header is still in the dynamic table. Let's add it to the header list.

# In[126]:


host_hdr = h2.HPackIndexedHdr(index=host_hdr_idx)
host_hdr.show()
hdrs_frm.payload.hdrs.append(host_hdr)

# Now that we added all the pseudo-headers, let's add the "real" ones. The compression header is in the static table, so we just need to look it up.

# In[127]:


z_hdr_idx = tblhdr.get_idx_by_name_and_value("accept-encoding", "gzip, deflate")
z_hdr = h2.HPackIndexedHdr(index=z_hdr_idx)
z_hdr.show()
hdrs_frm.payload.hdrs.append(z_hdr)

# We also need to create the header for our new cookie. Cookie are sensitive. We don't want it to be indexed and we don't want any intermediate to index it. As such, we will use a HPackLitHdrFldWithoutIndexing and with the never_index bit set, here as well. The name "cookie", though, happens to be in the RFC7541 static headers table, so we will use it.

# In[128]:


cookie_hdr_idx = tblhdr.get_idx_by_name("cookie")
cookie_str = h2.HPackHdrString(data=h2.HPackZString(cookie[0]))
cookie_hdr = h2.HPackLitHdrFldWithoutIndexing(
    never_index=1, index=cookie_hdr_idx, hdr_value=cookie_str
)
cookie_hdr.show()
hdrs_frm.payload.hdrs.append(cookie_hdr)

# Also, we need to specify that we read French. Once more, the "accept-language" header is in the HPack static table, but "fr-Fr" might not be. Let's see if we did index that earlier.

# In[129]:


acceptlang_hdr_idx = tblhdr.get_idx_by_name_and_value("accept-language", "fr-FR")
print(acceptlang_hdr_idx)

# Excellent! This is an entry of the dynamic table and we can use it in this session! Let's use it with an HPackIndexedHdr packet.

# In[130]:


acceptlang_hdr = h2.HPackIndexedHdr(index=acceptlang_hdr_idx)
acceptlang_hdr.show()
hdrs_frm.payload.hdrs.append(acceptlang_hdr)

# Let's do the same thing quickly for the other headers.

# In[131]:


accept_hdr_idx = tblhdr.get_idx_by_name_and_value("accept", "text/html")
accept_hdr = h2.HPackIndexedHdr(index=accept_hdr_idx)
accept_hdr.show()
hdrs_frm.payload.hdrs.append(accept_hdr)
ua_hdr_idx = tblhdr.get_idx_by_name_and_value("user-agent", "Scapy HTTP/2 Module")
ua_hdr = h2.HPackIndexedHdr(index=ua_hdr_idx)
ua_hdr.show()
hdrs_frm.payload.hdrs.append(ua_hdr)

# Now, we forget a piece in our previous queries regarding privacy: I want to add a Do Not Track header (https://tools.ietf.org/html/draft-mayer-do-not-track-00). Let's add this header into every subsequent queries. For this reason, I want to have it indexed. It is worth noting that the "DNT" header is not part of the HPack static table (how curious?). Finally, the value of this header is just 1. We might actually save a few bits by NOT compressing this value.

# In[132]:


dnt_name_str = h2.HPackLiteralString("dnt")
dnt_val_str = h2.HPackLiteralString("1")
dnt_name = h2.HPackHdrString(data=dnt_name_str)
dnt_value = h2.HPackHdrString(data=dnt_val_str)
dnt_hdr = h2.HPackLitHdrFldWithIncrIndexing(hdr_name=dnt_name, hdr_value=dnt_value)
dnt_hdr.show()
hdrs_frm.payload.hdrs.append(dnt_hdr)

# We are not done yet with the DNT header, though. We also need to insert it into the HPack Dynamic table, so that later lookups will find it.

# In[133]:


tblhdr.register(dnt_hdr)

# Phew! We made it! Let's see what we got so far.

# In[134]:


hdrs_frm.show2()

# Oh! Just for comparison, we would have got about the same result using the helpers (modulo some safety checks that we did not do here...).

# In[135]:


tblhdr.parse_txt_hdrs(
    """:method GET
    :scheme https
    :path /search?q=scapy
    :authority www.google.fr
    accept-encoding: gzip, deflate
    cookie: {}
    accept-language: fr-FR
    accept: text/html
    user-agent: Scapy HTTP/2 Module
    dnt: 1
    """.format(
        cookie
    ),
    stream_id=5,
    max_frm_sz=srv_max_frm_sz,
    max_hdr_lst_sz=srv_max_hdr_lst_sz,
    is_sensitive=lambda hdr_name, hdr_val: hdr_name in ["cookie", ":path"],
    should_index=lambda x: x
    in [
        "x-requested-with",
        "user-agent",
        "accept-language",
        "host",
        "accept",
        ":authority",
        "dnt",
    ],
).show2()

# Let's now send our query to Google and read the answer!

# In[137]:


srv_global_window -= len(str(hdrs_frm))
assert srv_global_window >= 0
ss.send(hdrs_frm)

h2seq = h2.H2Seq()

new_frame = None
while isinstance(new_frame, type(None)) or "ES" not in new_frame.flags:
    # As previously, if we receive a ping, we ackownledge it.
    if not isinstance(new_frame, type(None)) and new_frame.stream_id == 0:
        if new_frame.type == h2.H2PingFrame.type_id:
            new_frame.flags.add("A")
            srv_global_window -= len(str(new_frame))
            assert srv_global_window >= 0
            ss.send(new_frame)

        assert (
            new_frame.type != h2.H2ResetFrame.type_id
            and new_frame.type != h2.H2GoAwayFrame.type_id
        ), "Error received; something is not right!"

    try:
        new_frame = ss.recv()
        new_frame.show()
        if new_frame.stream_id == 5:
            h2seq.frames.append(new_frame)
    except:
        import time

        time.sleep(1)
        new_frame = None

# Let's display the answer in human-readable format. We assume, once more for the sake of simplicity that we received very few headers.

# In[141]:


stream_txt = srv_tblhdr.gen_txt_repr(h2seq.frames[0])
data = ""
for frgmt in h2seq.frames[1:]:
    data += frgmt.payload.data
print(stream_txt)
HTML(zlib.decompress(data, 16 + zlib.MAX_WBITS).decode("utf-8", "ignore"))
