import logging
from typing import Any, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_CODE, CONF_NAME
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
COVER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_CODE): cv.string,
        vol.Optional("add_another"): cv.boolean,
    }
)


async def validate_command(code):
    """Validate command is binary"""
    _LOGGER.info("validation ")
    for i in range(len(code)):
        if int(code[i]) not in [1, 0]:
            raise ValueError


class ConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config or options flow for Dummy Garage."""

    data: None

    def __init__(self):
        self.data = []

    async def async_step_user(self, user_input: Optional[dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        _LOGGER.info(" initialize first step")
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                await validate_command(user_input[CONF_CODE])
            except ValueError:
                errors["base"] = "binaryError"
            if not errors:
                # Input is valid, set data.
                self.data.append(
                    {
                        "name": user_input[CONF_NAME],
                        "code": user_input[CONF_CODE],
                        "device_class": "shade",
                    }
                )
                if user_input.get("add_another", False):
                    return await self.async_step_user()
                else:
                    # self.data[CONF_NAME] = []
                    # # Return the form of the next step.
                    return self.async_create_entry(title="RfCover", data=self.data[0])

        return self.async_show_form(
            step_id="user", data_schema=COVER_SCHEMA, errors=errors
        )

    # def async_config_entry_title(self, options: Mapping[str, Any]) -> str:
    #     """Return config entry title."""
    #     return cast(str, options["name"]) if "name" in options else ""
