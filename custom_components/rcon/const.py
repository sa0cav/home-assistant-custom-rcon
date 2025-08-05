import os
import yaml

DOMAIN = "rcon"
COMMANDS_FILE = os.path.join(os.path.dirname(__file__), "commands.yaml")

# Load commands synchronously
def load_commands_sync() -> dict:
    try:
        with open(COMMANDS_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}

# List games for configuration flow
GAMES = ["cs2", "minecraft"]
#GAMES = list(load_commands_sync().keys())

# Async version of command loading
async def async_load_commands(hass) -> dict:
    return await hass.async_add_executor_job(load_commands_sync)

import voluptuous as vol
from homeassistant.helpers import config_validation as cv

SERVICE_SCHEMA = vol.Schema({
    vol.Required("server"):  cv.string,
    vol.Required("command"): cv.string,
})
