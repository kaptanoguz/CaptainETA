#!/usr/bin/env bash
# Downloads the public datasets used by the distance builder into this folder.
set -euo pipefail
cd "$(dirname "$0")"
NE=https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson
for f in ne_10m_land ne_10m_minor_islands; do
  [ -s $f.geojson ] || curl -fsSL -o $f.geojson $NE/$f.geojson
done
# NOAA ETOPO1 bathymetry, one subset per region (lon0 lon1 lat0 lat1 must match geo.py REGIONS)
python3 - <<'PY'
import subprocess, os
from geo import REGIONS
for n, lo0, lo1, la0, la1 in REGIONS:
    out = f"etopo_{n}.nc"
    if os.path.exists(out) and os.path.getsize(out) > 0: continue
    url = f"https://upwell.pfeg.noaa.gov/erddap/griddap/etopo180.nc?altitude%5B({la0}):1:({la1})%5D%5B({lo0}):1:({lo1})%5D"
    subprocess.run(["curl", "-fsSL", "--retry", "3", "-o", out, url], check=True)
    print("fetched", out)
PY
# NGA Pub. 151 "Distances Between Ports" (public domain) — validation only
[ -s pub151.pdf ] || curl -fsSL -o pub151.pdf "https://maritimesafetyinnovationlab.org/wp-content/uploads/2015/01/pub151-distances-btw-ports.pdf"
[ -s raw.txt ] || pdftotext pub151.pdf raw.txt
