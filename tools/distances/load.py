import json, os
_src = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ports_source.json'), encoding='utf-8'))
PORTS = [p['name'] for p in _src]
COORDS = {p['name']: [p['lat'], p['lon']] for p in _src}
