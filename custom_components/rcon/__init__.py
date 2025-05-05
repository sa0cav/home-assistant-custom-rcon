# custom_components/rcon/__init__.py

import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from mcrcon import MCRcon
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """YAML-support (kan lämnas tom om du bara använder UI)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Initiera RCON-klient och ladda plattformar."""
    data = entry.data
    host = data.get("host")
    port = data.get("port")
    # Tolka tom sträng som ingen password
    password = data.get("password") or None

    # Skapa och anslut klient
    client = MCRcon(host, password, port)
    await hass.async_add_executor_job(client.connect)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "client": client,
        "game": data.get("game")
    }

    _register_service(hass, entry.entry_id)

    # Forwarda till sensor och button
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")
    await hass.config_entries.async_forward_entry_setup(entry, "button")

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Stäng av klient och ta bort plattformar."""
    info = hass.data[DOMAIN].pop(entry.entry_id, None)
    if info and info.get("client"):
        await hass.async_add_executor_job(info["client"].disconnect)

    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    await hass.config_entries.async_forward_entry_unload(entry, "button")
    return True

def _register_service(hass: HomeAssistant, entry_id: str):
    """Registrera rcon.send_command med återanslutning vid fel."""
    from homeassistant.core import ServiceCall
    import voluptuous as vol
    from homeassistant.helpers import config_validation as cv

    SERVICE_SCHEMA = vol.Schema({vol.Required("command"): cv.string})

    async def handle_send_command(call: ServiceCall):
        cmd = call.data.get("command")
        info = hass.data[DOMAIN][entry_id]
        client = info["client"]

        _LOGGER.debug("Skickar RCON-kommando: %s", cmd)
        try:
            response = await hass.async_add_executor_job(client.command, cmd)
        except Exception as e:
            _LOGGER.warning("RCON-anslutning tappad, försöker återansluta: %s", e)
            await hass.async_add_executor_job(client.disconnect)
            await hass.async_add_executor_job(client.connect)
            try:
                response = await hass.async_add_executor_job(client.command, cmd)
            except Exception as e2:
                _LOGGER.error("Återanslutning misslyckades: %s", e2)
                response = f"Error after reconnect: {e2}"

        _LOGGER.debug("RCON-svar: %s", response)
        hass.bus.async_fire(
            f"{DOMAIN}_response",
            {"command": cmd, "response": response}
        )

    if not hass.services.has_service(DOMAIN, "send_command"):
        hass.services.async_register(
            DOMAIN,
            "send_command",
            handle_send_command,
            schema=SERVICE_SCHEMA
        )
