# custom_components/rcon/button.py

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, load_commands  # använd funktionen, inte GAMES

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    """Sätt upp knappar baserat på commands.yaml varje gång plattformen laddas."""
    info = hass.data[DOMAIN][entry.entry_id]
    game = info.get("game", "")

    # Läs in färska kommandon för valt spel  # TODO translate
    commands = load_commands().get(game, [])

    buttons = []
    for cmd in commands:
        # Skapa knapp för varje kommando utan parametrar  # TODO translate
        if "{" not in cmd:
            buttons.append(RconPredefinedButton(entry.entry_id, cmd))
    async_add_entities(buttons)

class RconPredefinedButton(ButtonEntity):
    """Knapp som kör ett fördefinierat RCON-kommando."""

    def __init__(self, entry_id: str, command: str):
        self._entry_id = entry_id
        self._command = command
        self._attr_name = f"RCON: {command}"
        self._attr_unique_id = f"{entry_id}_{command}"

    async def async_press(self) -> None:
        """Anropa din send_command-service med valt kommando."""
        await self.hass.services.async_call(
            DOMAIN,
            "send_command",
            {"command": self._command}
        )