from homeassistant.const import TEMP_FAHRENHEIT
from homeassistant.helpers.entity import Entity
import requests
import json
import re

sureNotPython = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'

class LaCrosse:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def getSessionKey(self):

        headers = {
            'origin': 'http://www.lacrossealertsmobile.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': sureNotPython,
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': '*/*',
            'referer': 'http://www.lacrossealertsmobile.com/v1.2/',
            'authority': 'decent-destiny-704.appspot.com',
        }

        params = (
            ('pkey', 'Dyd7kC4wxLDFz0rQ6W5T28DPgrM6SOBe'),
            ('action', 'userlogin'),
        )

        data = [
            ('iLogEmail', self.user),
            ('iLogPass', self.password),
        ]

        response = requests.post('https://decent-destiny-704.appspot.com/laxservices/user-api.php', headers=headers, params=params, data=data)

        return json.loads(response.text)['sessionKey']

    def getWebPage(self, sessionKey):
        cookies = {
            '_ga': 'GA1.2.553414151.1524103924',
            '_gid': 'GA1.2.1590562279.1524264911',
            '_gat': '1',
            'uSAbc': sessionKey,
        }

        headers = {
            'Pragma': 'no-cache',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://www.lacrossealertsmobile.com/v1.2/',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
        }

        response = requests.get('http://www.lacrossealertsmobile.com/v1.2/', headers=headers, cookies=cookies)

        return response


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    username = config['user']
    password = config['pass']
    add_devices([LaCrosseAmbientSensor(username, password), LaCrosseProbeSensor(username, password), LaCrosseHumidSensor(username, password)])


class LaCrosseAmbientSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, username, password):
        """Initialize the sensor."""
        self._user = username
        self._pass = password
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Outside Ambient'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_FAHRENHEIT

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        mySensor = LaCrosse(self._user, self._pass)
        sessionKey = mySensor.getSessionKey()
        webPage = mySensor.getWebPage(sessionKey)
        match = re.findall('^userGatewaysList.* ({.*})', webPage.text, flags=re.MULTILINE)
        onlyData = json.loads(match[0])
        ambient = onlyData['device0']['obs'][0]['ambient_temp']
        self._state = ambient

class LaCrosseProbeSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, username, password):
        """Initialize the sensor."""
        self._user = username
        self._pass = password
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Outside Probe'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_FAHRENHEIT

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        mySensor = LaCrosse(self._user, self._pass)
        sessionKey = mySensor.getSessionKey()
        webPage = mySensor.getWebPage(sessionKey)
        match = re.findall('^userGatewaysList.* ({.*})', webPage.text, flags=re.MULTILINE)
        onlyData = json.loads(match[0])
        probe = onlyData['device0']['obs'][0]['probe_temp']
        self._state = probe

class LaCrosseHumidSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, username, password):
        """Initialize the sensor."""
        self._user = username
        self._pass = password
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Outside Humidity'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return '%' 

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        mySensor = LaCrosse(self._user, self._pass)
        sessionKey = mySensor.getSessionKey()
        webPage = mySensor.getWebPage(sessionKey)
        match = re.findall('^userGatewaysList.* ({.*})', webPage.text, flags=re.MULTILINE)
        onlyData = json.loads(match[0])
        humid = onlyData['device0']['obs'][0]['humidity']
        self._state = humid

