from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, async_load_commands

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    """Set up predefined RCON command buttons."""
    info = hass.data[DOMAIN][entry.entry_id]
    commands = (await async_load_commands(hass)).get(info["game"], [])
    buttons = [
        RconPredefinedButton(info["nickname"], cmd)
        for cmd in commands if isinstance(cmd, str)
    ]
    async_add_entities(buttons)

class RconPredefinedButton(ButtonEntity):
    """Button entity to send a predefined RCON command."""
    def __init__(self, server: str, command: str):
        self._server = server
        self._command = command
        self._attr_name = f"{server}: {command}"
        self._attr_unique_id = f"{server}_{command}"

    async def async_press(self) -> None:
        """Send the command when the button is pressed."""
        await self.hass.services.async_call(
            DOMAIN,
            "send_command",
            {"server": self._server, "command": self._command}
        )
