# custom_components/rcon/__init__.py
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from mcrcon import MCRcon
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    # YAML-support (kan lämnas tom om du inte använder YAML)  # TODO translate
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Initiera RCON-klient
    data = entry.data
    host = data.get("host")
    port = data.get("port")
    password = data.get("password")

    client = MCRcon(host, password, port)
    await hass.async_add_executor_job(client.connect)

    # Spara klientsession
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "client": client,
        "game": data.get("game")
    }

    # Registrera service
    _register_service(hass, entry.entry_id)

    # Forwarda till sensor och button
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")
    await hass.config_entries.async_forward_entry_setup(entry, "button")

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Koppla ner och ta bort klient
    info = hass.data[DOMAIN].pop(entry.entry_id, None)
    if info and info.get("client"):
        await hass.async_add_executor_job(info["client"].disconnect)

    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    await hass.config_entries.async_forward_entry_unload(entry, "button")
    return True


def _register_service(hass: HomeAssistant, entry_id: str):
    from homeassistant.core import ServiceCall
    import voluptuous as vol
    from homeassistant.helpers import config_validation as cv

    SERVICE_SCHEMA = vol.Schema({vol.Required("command"): cv.string})

    async def handle_send_command(call: ServiceCall):
        cmd = call.data.get("command")
        client = hass.data[DOMAIN][entry_id]["client"]
        _LOGGER.debug("Skickar RCON: %s", cmd)
        try:
            response = await hass.async_add_executor_job(client.command, cmd)
        except Exception as e:
            response = f"Error: {e}"
        hass.bus.async_fire(f"{DOMAIN}_response", {"command": cmd, "response": response})

    if not hass.services.has_service(DOMAIN, "send_command"):
        hass.services.async_register(
            DOMAIN, "send_command", handle_send_command, schema=SERVICE_SCHEMA
        )