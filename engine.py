import yaml


def read_yaml(path: str) -> dict:
    with open(path) as f:
        return yaml.load(f, yaml.FullLoader)

