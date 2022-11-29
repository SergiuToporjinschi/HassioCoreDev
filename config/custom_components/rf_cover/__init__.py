import logging

import voluptuous as vol

from homeassistant import config_entries, core
import homeassistant.helpers.config_validation as cv

from .const import *

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
                vol.Required(PIN): cv.positive_int,
                vol.Required(REPEAT): cv.positive_int,
                vol.Required(PAUSE): cv.positive_int,
                vol.Required(INIT): vol.Schema({
                    vol.Required(LEN): cv.positive_int,
                    vol.Required(TIME): vol.Schema({
                        vol.Required(HIGH): cv.positive_int,
                        vol.Required(LOW): cv.positive_int
                    })
                }),
                vol.Required(BIT): vol.Schema({
                    vol.Required(TIME): vol.Schema({
                        vol.Required(SHORT): cv.positive_int,
                        vol.Required(LONG): cv.positive_int
                    })
                })
            })
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass: core.HomeAssistant, config: config_entries.ConfigEntry) -> bool:
    """Set up the RFCover component."""
    _LOGGER.info("rf_cover log %s", SERVICE_NAME)
    hass.data.setdefault(DOMAIN, {})
    hass.states.async_set(SERVICE_STATE_NAME, "False")
    hass.data[DOMAIN]["rfConfig"] = config[DOMAIN]
    # hass.config_entries.async_update_entry(config, unique_id="sss")
    async def async_handle_sendCommand(call):
        """handle send command service"""
        command = call.data.get(SERVICE_PAYLOAD_NAME, None)
        ## TODO add send command
        hass.states.async_set(SERVICE_STATE_NAME, "True")
        _LOGGER.info("Sending command %s", command)
        hass.states.async_set(SERVICE_STATE_NAME, "False")

    hass.services.async_register(DOMAIN, SERVICE_NAME, async_handle_sendCommand)
    return True