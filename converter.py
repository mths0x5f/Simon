import yaml
import json

with open('probe.json') as script:
    data = json.load(script)

with open('probe.yaml', 'w') as script:
	script.write(yaml.dump(data))