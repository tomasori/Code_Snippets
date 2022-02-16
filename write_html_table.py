#
# creates a populated HTML Table to send to webbrowser
#
#
# Coded by Tomas Orihuela, PE
# Structural engineer designing offshore platforms for the Oil & Gas industry
# and Offshore Renewable Energy (Offshore Wind)
# www.sacsly.com
# www.tomasorihuela.com
#
#
# Original code is not mine. I found a few examples and tweaked it for my need.
#


html_tableheader = """<div class="ztbl-header">
<table cellpadding="0" cellspacing="0" border="0">
<thead>
<tr>{}
<tr>
</thead>
</table>
</div>"""

html_tablecontent = """<div class="ztbl-content">
<table cellpadding="0" cellspacing="0" border="0">
<tbody>
{}</tbody>
</table>
</div>"""

th = "\n    <th>{}</th>"
tr = "<tr>\n{}</tr>\n"
td = "    <td>{}</td>\n"

items_headers = ['First', 'MI', 'Last', 'Age']
items_content = [['AAA', 'B', 'LLL', '40'], ['SSS', 'R', 'BBBB', '32'], ['CCC', 'B', 'MMMMM', '41']]
subitems_header = ''.join([th.format(item) for item in items_headers])
subitems_content = [tr.format(''.join([td.format(a) for a in item])) for item in items_content]

header_s  = html_tableheader.format(subitems_header)
content_s = html_tablecontent.format("".join(subitems_content))


###########
# TESTING
#

print( header_s )
print( content_s )
