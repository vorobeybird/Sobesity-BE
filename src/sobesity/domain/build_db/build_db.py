import yaml
from pprint import pprint

with open('format.yaml') as f:
    templates = yaml.safe.load(f)

pprint(templates)
