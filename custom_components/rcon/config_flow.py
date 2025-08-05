from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_PASSWORD, CONF_NAME
from .const import DOMAIN, GAMES
import voluptuous as vol

class RconConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for RCON integration."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required(CONF_NAME): str,
                    vol.Required("game"): vol.In(GAMES),
                })
            )

        self._game = user_input["game"]
        self._name = user_input[CONF_NAME]

        # Set default port based on game
        default_port = 25575 if self._game == "minecraft" else 27015

        return self.async_show_form(
            step_id="server",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Optional(CONF_PORT, default=default_port): int,
                vol.Optional(CONF_PASSWORD, default=""): str,
            })
        )

    async def async_step_server(self, user_input=None):
        if user_input is None:
            return self.async_abort(reason="incomplete_form")

        data = {
            CONF_NAME: self._name,
            "game": self._game,
            CONF_HOST: user_input[CONF_HOST],
            CONF_PORT: user_input.get(CONF_PORT),
            CONF_PASSWORD: user_input.get(CONF_PASSWORD, "")
        }

        unique_id = f"{data[CONF_HOST]}_{data[CONF_PORT]}_{data['game']}_{data[CONF_NAME]}"
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=data[CONF_NAME],
            data=data
        )
