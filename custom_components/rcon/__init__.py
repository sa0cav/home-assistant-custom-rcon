# custom_components/rcon/__init__.py

import logging
import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry, config_validation as cv
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SERVICE_NAME = "send_command"
SERVICE_SCHEMA = vol.Schema({
    vol.Required("server"):  cv.string,
    vol.Required("command"): cv.string,
})

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Initialize client, device, and rcon.send_command service."""
    # Store all info needed later
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = entry.data
    # (Re)register our service
    hass.services.async_register(
        DOMAIN,
        SERVICE_NAME,
        lambda call: hass.async_create_task(handle_send_command(hass, call)),
        schema=SERVICE_SCHEMA,
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Clean up when the integration is removed."""
    hass.services.async_remove(DOMAIN, SERVICE_NAME)
    hass.data[DOMAIN].pop(entry.entry_id)
    return True

async def handle_send_command(hass: HomeAssistant, call: ServiceCall):
    """Handle rcon.send_command – choose correct backend and fire event."""
    server = call.data.get("server")
    cmd = call.data.get("command")

    # Determine backend based on configuration (example logic)
    host = hass.data[DOMAIN][call.context.config_entry_id]["host"]
    port = hass.data[DOMAIN][call.context.config_entry_id].get("port", 25575)
    password = hass.data[DOMAIN][call.context.config_entry_id].get("password", "")

    try:
        from mcrcon import MCRcon
        _LOGGER.debug("Using MCRcon for %s:%s", host, port)
        client = MCRcon(host, password, port)
        client.connect()
        response = client.command(cmd)
        client.disconnect()
    except ImportError:
        try:
            import valve.rcon
            _LOGGER.debug("Using python-valve for %s:%s", host, port)
            response = valve.rcon.RCON((host, port), password).execute(cmd)
        except ImportError:
            raise RuntimeError("No RCON library installed for the game")
    except Exception as e:
        _LOGGER.error("RCON error for %s: %s", server, e)
        response = f"Error: {e}"

    # Trim state to a maximum of 255 characters
    trimmed = response if len(response) <= 255 else response[:252] + "…"
    hass.bus.async_fire(
        f"{DOMAIN}_response",
        {
            "server":        server,
            "command":       cmd,
            "response":      trimmed,
            "full_response": response,
        }
    )
