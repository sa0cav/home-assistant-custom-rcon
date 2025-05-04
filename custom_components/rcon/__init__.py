import asyncio
import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_PASSWORD
from homeassistant.helpers import config_validation as cv
from .const import DOMAIN
from mcrcon import MCRcon

# Schema för validering av service-data
SERVICE_SCHEMA = vol.Schema({
    vol.Required("command"): cv.string,
})

async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})

    conf = config.get(DOMAIN, {})
    host = conf.get(CONF_HOST)
    port = conf.get(CONF_PORT, 25575)
    password = conf.get(CONF_PASSWORD)

    client = MCRcon(host, password, port)
    hass.data[DOMAIN]["client"] = client

    async def handle_send_command(call: ServiceCall):
        cmd = call.data.get("command")
        try:
            response = client.command(cmd)
        except Exception as e:
            response = f"Error: {e}"
        hass.bus.async_fire(
            f"{DOMAIN}_response",
            {"command": cmd, "response": response}
        )

    hass.services.async_register(
        DOMAIN,
        "send_command",
        handle_send_command,
        schema=SERVICE_SCHEMA
    )

    return True
