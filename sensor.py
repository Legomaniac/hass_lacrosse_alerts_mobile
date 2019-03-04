import logging

import voluptuous as vol

from homeassistant.components.sensor import ENTITY_ID_FORMAT, PLATFORM_SCHEMA
from homeassistant.const import TEMP_FAHRENHEIT, CONF_ID
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

REQUIREMENTS = ['pylacrossapi==0.3']

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ID): cv.string,
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the lacrosse alerts mobile platform."""
    import pylacrossapi
    device_id = config.get(CONF_ID)
    unit_measure = 0
    time_zone = 10
    lacrosse_device = pylacrossapi.lacrosse(device_id, unit_measure, time_zone)
    add_devices([LaCrosseAmbientSensor(lacrosse_device), LaCrosseProbeSensor(lacrosse_device), LaCrosseHumidSensor(lacrosse_device)])

class LaCrosseAlertsMobileSensor(Entity):
    """Representation of a LaCrosse Alerts Mobile Sensor."""
    def __init__(self, lacrosse_device):
        """Initialize the sensor."""
        self._lacrosse_device = lacrosse_device
        self._state = None

    def update(self):
        obs = self._lacrosse_device.getObservation(1)
        self._ambient = obs[0]['ambient_temp']
        self._probe = obs[0]['probe_temp']
        self._humidity = obs[0]['humidity']

class LaCrosseAmbientSensor(LaCrosseAlertsMobileSensor):
    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Outside Ambient'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._ambient

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_FAHRENHEIT

class LaCrosseProbeSensor(LaCrosseAlertsMobileSensor):
    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Outside Probe'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._probe

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_FAHRENHEIT

class LaCrosseHumidSensor(LaCrosseAlertsMobileSensor):
    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Outside Humidity'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._humidity

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return '%'

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return 'mdi:water-percent'
