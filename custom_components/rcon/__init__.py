import asyncio
from homeassistant.core import HomeAssistant, ServiceCall
from .const import DOMAIN
from mcrcon import MCRcon

async def async_setup(hass: HomeAssistant, config: dict):
    # Initiera datastruktur
    hass.data.setdefault(DOMAIN, {})

    # Läs in konfiguration från configuration.yaml (om du inte har config_flow)
    conf = config.get(DOMAIN, {})
    host = conf.get("host")
    port = conf.get("port", 25575)
    password = conf.get("password")

    # Skapa RCON-klienten och spara den
    client = MCRcon(host, password, port)
    hass.data[DOMAIN]["client"] = client

    # Registrera servicen för att skicka valfritt RCON-kommando
    async def handle_send_command(call: ServiceCall):
        cmd = call.data.get("command")
        try:
            # Skicka kommandot
            response = client.command(cmd)
        except Exception as e:
            # Hantera fel, skicka event med felmeddelande
            response = f"Error: {e}"

        # Avfyra ett Home Assistant-event med kommandot och svaret
        hass.bus.async_fire(
            f"{DOMAIN}_response",
            {"command": cmd, "response": response}
        )

    # Registrera service under domänen "rcon" och namnet "send_command"
    hass.services.async_register(
        DOMAIN,
        "send_command",
        handle_send_command,
        schema=SERVICE_SCHEMA  # Om du vill validera fält; kan utelämnas
    )

    return True
