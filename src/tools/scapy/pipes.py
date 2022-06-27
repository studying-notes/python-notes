"""
Date: 2022.05.11 13:43
Description: Pipes
LastEditors: Rustle Karl
LastEditTime: 2022.05.11 13:43
"""
from scapy.pipetool import CLIFeeder, PipeEngine
from scapy.scapypipes import InjectSink

"""
Pipes are an advanced Scapy feature that aims sniffing, modifying and 
printing packets. The API provides several buildings blocks. All of them, 
have high entries and exits (>>) as well as low (>) ones.

For example, the `CliFeeder` is used to send message from the Python 
command line to a low exit. It can be combined to the `InjectSink` that 
reads message on its low entry and inject them to the specified network 
interface. These blocks can be combined as follows:
"""

# Instantiate the blocks
clf = CLIFeeder()
ijs = InjectSink("enx3495db043a28")

# Plug blocks together
clf > ijs

# Create and start the engine
pe = PipeEngine(clf)
pe.start()

# Packet can be sent using the following command on the prompt:
clf.send("Hello Scapy !")
