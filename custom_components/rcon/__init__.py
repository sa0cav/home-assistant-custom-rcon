import asyncio
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from mcrcon import MCRcon

async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})
    # Här kan du läsa host/port/password från configuration.yaml eller config_flow
    host = config[DOMAIN].get("host")
    port = config[DOMAIN].get("port", 25575)
    password = config[DOMAIN].get("password")
    # Spara instansen
    hass.data[DOMAIN]["client"] = MCRcon(host, password, port)
    return True
