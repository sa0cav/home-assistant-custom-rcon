# custom_components/rcon/const.py
import os
import yaml

# Domän för integrationen  # TODO translate
DOMAIN = "rcon"

# Läs in spel och kommandon från YAML  # TODO translate
def load_commands() -> dict:
    here = os.path.dirname(__file__)
    path = os.path.join(here, "commands.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# Tillgängliga spel och deras kommandon  # TODO translate
GAMES = load_commands()