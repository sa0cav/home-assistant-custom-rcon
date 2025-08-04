import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_PASSWORD, CONF_NAME
from .const import DOMAIN, GAMES

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): str,
    vol.Required(CONF_HOST): str,
    vol.Optional(CONF_PORT, default=25575): int,
    vol.Optional(CONF_PASSWORD, default=""): str,
    vol.Required("game", default=GAMES[0]): vol.In(GAMES),
})

class RconConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for RCON integration."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=STEP_USER_DATA_SCHEMA
            )

        unique_id = (
            f"{user_input[CONF_HOST]}_{user_input.get(CONF_PORT,25575)}_"
            f"{user_input['game']}_{user_input[CONF_NAME]}"
        )
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=user_input[CONF_NAME],
            data=user_input
        )
