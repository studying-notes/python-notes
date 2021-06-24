h1 = '''
<!Doctype html>
<html>

<head>
    <title>单元测试报告</title>
    <style>
        body {
            width: 80%;
            margin: 40px auto;
            font-weight: bold;
            font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
            font-size: 18px;
            color: #000;
        }

        table {
            *border-collapse: collapse;
            border-spacing: 0;
            width: 100%;
        }

        .tableStyle {
            /* border: solid #ggg 1px; */
            border-style: outset;
            border-width: 2px;
            /* border: 2px; */
            border-color: blue;
        }

        .tableStyle tr:hover {
            background: rgb(173, 216, 230);
        }

        .tableStyle td,
        .tableStyle th {
            border-left: solid 1px rgb(146, 208, 80);
            border-top: 1px solid rgb(146, 208, 80);
            padding: 15px;
            text-align: center;
        }

        .tableStyle th {
            padding: 15px;
            background-color: rgb(146, 208, 80);
            background-image: -webkit-gradient(linear, left top, left bottom, from(#92D050), to(#A2D668));
            /* rgb(146, 208, 80) */
        }
    </style>
</head>

<body>
    <center>
        <h1>测试报告</h1>
    </center>
    <br/>
    <table class="tableStyle">
        <thead>
            <tr>
                <th>Search Words</th>
                <th>Assert Words</th>
                <th>Start Time</th>
                <th>Waste Time</th>
                <th>Status</th>
            </tr>
        </thead>
'''

h2 = '''
    </table>
</body>

</html>
'''

def generate_html(tr_data):
    html = h1 + tr_data + h2
    with open('report.html', 'w', encoding='utf-8') as fp:
        fp.write(html)