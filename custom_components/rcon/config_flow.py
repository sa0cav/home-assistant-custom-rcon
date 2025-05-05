# custom_components/rcon/config_flow.py

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_PASSWORD
from .const import DOMAIN, GAMES

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST): str,
    vol.Optional(CONF_PORT, default=25575): int,
    # Gör lösenord valfritt — default tom sträng
    vol.Optional(CONF_PASSWORD, default=""): str,
    vol.Required("game", default=list(GAMES.keys())[0]): vol.In(list(GAMES.keys())),
})

class RconConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow för RCON-integration med valfritt lösenord."""
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Visa formulär första gången, skapa entry därefter."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=STEP_USER_DATA_SCHEMA
            )

        # Bygg unikt ID av host + spel
        unique = f"{user_input[CONF_HOST]}_{user_input['game']}"
        await self.async_set_unique_id(unique)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=f"{user_input['game']} @ {user_input[CONF_HOST]}",
            data=user_input
        )
