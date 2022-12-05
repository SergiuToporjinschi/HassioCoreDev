from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.components.cover import (
    PLATFORM_SCHEMA,
    CoverDeviceClass,
    CoverEntity,
    CoverEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_CODE, CONF_DEVICE_CLASS, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType

from .const import *
from .mixins import GPIOCon

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Dummy cover"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_CODE): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_DEVICE_CLASS, default=CoverDeviceClass.SHADE): cv.string,
    }
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities,
):
    """Setup sensors from a config entry created in the integrations UI."""
    # Update our config to include new repos and remove those that have been removed.
    config = hass.data[DOMAIN][config_entry.entry_id]
    if config_entry.options:
        config.update(config_entry.options)
    name = config_entry.data.get(CONF_NAME)
    code = config_entry.data.get(CONF_CODE)
    device_class = config_entry[CONF_DEVICE_CLASS]
    async_add_entities([RFCover(config, code, name, device_class)], True)


async def async_setup_platform(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType,
) -> None:
    """Setup for platform"""
    _LOGGER.debug("rf_cover log ")
    config = hass.data[DOMAIN].get("rfConfig")
    device_class = config_entry[CONF_DEVICE_CLASS]
    name = config_entry[CONF_NAME]
    code = config_entry[CONF_CODE]
    device_class = config_entry[CONF_DEVICE_CLASS]
    async_add_entities([RFCover(config, code, name, device_class)], True)


def send(hass: HomeAssistant, command: str) -> None:
    """sends commands to GPIP via service"""
    hass.services.call(DOMAIN, SERVICE_NAME, {SERVICE_PAYLOAD_NAME: command}, True)


class RFCover(GPIOCon, CoverEntity):
    """RF cover device"""

    def __init__(self, config, code, name, device_class) -> None:
        """Initialize the cover device."""
        super().__init__(config)
        self._attr_supported_features = (
            CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP
        )
        self._attr_is_closed = False
        self._attr_assumed_state = True
        self._name = name
        self._attr_name = name
        self._attr_code = code
        self._attr_device_class = device_class
        self._state = True

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Open shades"""
        _LOGGER.info("RFCover async_open_cover %s", self.name)
        self.hass.async_add_job(self.send_open)
        # self.send_open()

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Close shades"""
        _LOGGER.info("RFCover async_close_cover %s", self.name)
        self.hass.async_add_job(self.send_close)
        # self.send_close()
        # self.hass.add_job(send, self.hass, self._attr_code + " 00110011")

    async def async_stop_cover(self, **kwargs: Any) -> None:
        """Stops shades"""
        _LOGGER.info("RFCover async_stop_cover %s", self.name)
        self.hass.async_add_job(self.send_stop)
        # self.send_stop()
        # self.hass.add_job(send, self.hass, self._attr_code + " 01010101")

    def _get_code(self) -> str:
        """Get shade code"""
        return self._attr_code

    @property
    def name(self) -> str:
        """Return the name of the switch."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return self._name + "." + self._attr_code
