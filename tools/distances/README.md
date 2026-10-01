# Distance builder

Generates `../../ports.js` — the port list and the sea-route distance matrix used by the app.

## Run
```bash
python3 -m venv venv && venv/bin/pip install -r requirements.txt
./fetch_data.sh                      # Natural Earth, NOAA ETOPO1, NGA Pub. 151 (~200 MB)
venv/bin/python build.py             # regional grids, all route variants (~15 min, 6 cores)
venv/bin/python combine.py           # joins regions + long-haul legs -> variants.pkl
venv/bin/python pub.py               # parse Pub. 151 (validation only)
venv/bin/python validate.py base     # compare against Pub. 151
venv/bin/python export.py            # writes ../../ports.js
```
All commands run from this folder.

## Inputs
- `ports_source.json` — port names and positions. Add or move ports here, then rebuild.
- `geo.py` — regions, carved channels (straits, canals, river approaches), river-port approach
  distances, barriers, shallow-water threshold and penalty, ocean gateways.

## Method
1. **Regional grids** (`build.py`): Mercator raster at 1 arc-minute per region. Land from Natural
   Earth 10 m; water shallower than 10 m (NOAA ETOPO1) costs 10× so routes keep to deep water
   unless a port can only be reached through it. Narrow passages are carved open; known
   non-navigable shoals are drawn closed. Each port snaps to the nearest water cell. Paths come
   from Dijkstra (scikit-image MCP) and are smoothed to straight segments, separately for deep and
   shallow stretches; lengths are great-circle sums.
2. **Variants:** Kiel Canal & Øresund on/off (off = deep-draft routing via the Great Belt / Skagen),
   Suez open/closed.
3. **Long haul** (`combine.py`): European ports reach other regions through ocean gateways on the
   edge of the European grid plus the Eurostat MARNET network (`searoute`); other inter-regional
   pairs use MARNET directly. A port that can only reach a region's main water body by jumping
   more than 20 nm over land is ignored for that region.
4. **Export** (`export.py`): base matrix plus the pairs that change under each option.

`export.py` drops three duplicate entries from `ports_source.json` and renames Nhava Sheva — see
`DROP` / `RENAME` at the top of the file.

## Accuracy (vs NGA Pub. 151, 338 pairs listed consistently in both directions)
Median deviation 0.9 % (8 nm); 94 % of pairs within 5 %. Short coastal legs (< 200 nm) run about
2 % short on average.
