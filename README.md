# Captain ETA

Precision maritime navigation terminal — voyage and ETA planner for masters.

Plan voyages across 233 ports with MT-calibrated distances, en-route ETA updates, and port security (ISPS) SL1–3 lookup. Fully offline.

## Features

- Voyage planning: departure → arrival port, distance, speed → ETA
- MT-calibrated distance table (233 ports)
- En-route ETA update from remaining distance/time
- Last-10-port LOCODE / flag / security level history
- Pilot ↔ port mode
- 15 themes, TR/EN UI
- PDF / Excel export
- Istanbul SL1 preferred by default

## Tech

- Pure web UI (HTML/CSS/JS)
- **Tauri** (Rust) desktop shell — ~2 MB
- Distance data: `data/*.json` (141 real MT values + haversine × basin factor)

## Download

- **Windows:** `CaptainETA_x64-setup.exe` (or `.msi`) from Releases
- **Linux:** `.deb` package

## Screenshot

![Captain ETA](screenshot.png)

## License

MIT — Recep Oğuz Yağbasan
