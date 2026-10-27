# Captain ETA

Voyage ETA and passage-schedule calculator for ship operations. Single page, no build step — open `index.html` in a browser.

![Captain ETA: Istanbul → Rotterdam → Hamburg voyage with ETA, sea time, fuel and CO₂](docs/screenshots/planner.png)

## What it does
- **Multi-port route** with port stays — ETA/ETD for every call, in UTC and local time (per-port UTC offset).
- **Sea-route distances** between all built-in ports, precomputed berth to berth (see below). Any leg can be overridden manually (`man`).
- **Route options:** Kiel Canal & Øresund (off = deep-draft routing via the Great Belt / Skagen), and *Avoid Suez* (via the Cape of Good Hope).
- **Sea margin** applied to sea time (equivalent to an effective speed reduction, shown in the summary).
- **Bunkers** — fuel at sea from daily consumption, CO₂ using IMO conversion factors (HFO 3.114, VLSFO/LFO 3.151, MGO/MDO 3.206, LNG 2.750).
- **ETA message** — copies a telex-style ETA/ETD notice for agents and charterers.
- **PDF** voyage estimate, saved voyages (browser storage) with CSV export.

## Files
- `index.html` — the app.
- `ports.js` — generated port list, coordinates and distance matrix (do not edit by hand).

## How distances are computed
- **Regional legs:** shortest water path on a 1-arc-minute Mercator grid built from Natural Earth 10 m coastlines and NOAA ETOPO1 bathymetry. Open water shallower than 10 m is avoided where a deeper route exists. Straits, canals and river approaches that are too narrow for the grid (Bosphorus, Dardanelles, Kiel, Suez, Panama, Elbe, Scheldt, Thames, St Lawrence, …) are opened explicitly, and paths are smoothed to straight legs.
- **Long-haul legs:** European ports join the Eurostat MARNET sea-route network through ocean gateways (Gibraltar, Ushant, Red Sea, North Scotland); other inter-regional legs use MARNET directly.
- **Validation:** checked against NGA Pub. 151 *Distances Between Ports*. Median deviation is about 1 %; short coastal legs carry the largest relative error.

Distances do not model traffic separation schemes, pilot boarding positions or draft limits beyond the options above. For a binding ETA, check critical legs against your own distance tables.
