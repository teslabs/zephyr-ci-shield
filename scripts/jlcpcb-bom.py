"""
    @package
    Generate a CSV BOM for use with JLCSMT service.

    LCSC Part numbers are copied from the "JLCPCB" field if it exists.

    Command line:
    python "/path/to/jlcpcb-bom.py" "%I" "%O.csv"
"""

import sys

sys.path.insert(0, "/usr/share/kicad/plugins")

import kicad_netlist_reader
import csv


net = kicad_netlist_reader.netlist(sys.argv[1])

with open(sys.argv[2], "w") as f:
    out = csv.writer(f)
    out.writerow(["Comment", "Designator", "Footprint", "LCSC Part #"])

    for group in net.groupComponents():
        firstComponent = group[0]

        comment = firstComponent.getValue()
        designator = ",".join([component.getRef() for component in group])
        footprint = firstComponent.getFootprint().split(":")[1]
        jlcpcb_pn = firstComponent.getField("JLCPCB") or ""

        out.writerow([comment, designator, footprint, jlcpcb_pn])
