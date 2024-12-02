import logging
import voluptuous as vol
from typing import Any, Optional, Tuple

from .triones import TrionesInstance
from .const import DOMAIN

from homeassistant.const import CONF_MAC
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (COLOR_MODE_RGB, PLATFORM_SCHEMA,
                                            LightEntity, ATTR_RGB_COLOR, ATTR_BRIGHTNESS, COLOR_MODE_WHITE, ATTR_WHITE)
from homeassistant.util.color import (match_max_scale)
from homeassistant.helpers import device_registry

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_MAC): cv.string
})

async def async_setup_entry(hass, config_entry, async_add_devices):
    instance = hass.data[DOMAIN][config_entry.entry_id]
    async_add_devices([TrionesLight(instance, config_entry.data["name"], config_entry.entry_id)])

class TrionesLight(LightEntity):
    def __init__(self, instance: TrionesInstance, name: str, entry_id: str):
        """Initialize a Triones light."""
        self._instance = instance
        self._name = name
        self._entry_id = entry_id

        # Set attributes
        self._attr_unique_id = self._instance.mac
        self._attr_name = self._name
        self._is_on = None
        self._rgb_color = None
        self._white_brightness = None

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        rgb = kwargs.get("rgb_color", self._rgb_color)
        if rgb:
            await self._instance.set_color(rgb)
        else:
            await self._instance.turn_on()

        self._is_on = True

    async def async_turn_off(self, **kwargs):
        """Turn the light off."""
        await self._instance.turn_off()
        self._is_on = False

    async def async_update(self):
        """Fetch the latest state from the device."""
        await self._instance.update()
        self._is_on = self._instance.is_on
        self._rgb_color = self._instance.rgb_color
        self._white_brightness = self._instance.white_brightness

    @property
    def is_on(self):
        """Return whether the light is on."""
        return self._is_on

    @property
    def rgb_color(self):
        """Return the RGB color value."""
        return self._rgb_color
    