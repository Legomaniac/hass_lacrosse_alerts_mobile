# LaCrosse Alerts Mobile for Home Assistant
Hass component to read data from lacrossealertsmobile.com
----
Progess:
- Worked with @concongo to get his module updated for Python 3
- Used that module to implement direct call to the API in place of my hodge-podge method of loading the website
- Working towards HASS level 'correctness'

Todo:
- Fix: `Error doing job: Task exception was never retrieved` on first run. Example:
`Traceback (most recent call last):
  File "/opt/homeassistant/lib64/python3.7/site-packages/homeassistant/helpers/entity_platform.py", line 352, in _async_add_entity
    await entity.async_update_ha_state()
  File "/opt/homeassistant/lib64/python3.7/site-packages/homeassistant/helpers/entity.py", line 232, in async_update_ha_state
    state = self.state
  File "/home/homeassistant/.homeassistant/custom_components/lacrosse_alerts_mobile/sensor.py", line 85, in state
    return self._humidity
AttributeError: 'LaCrosseHumidSensor' object has no attribute '_humidity'`
