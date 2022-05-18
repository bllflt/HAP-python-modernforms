import pytest
from pyhap.accessories.modernforms.fan import ModernFormsFan


@pytest.fixture()
def fan():
    return ModernFormsFan('')


class TestModernFormsFanDevice:

    def test_build_desired_config_simple(self, fan):
        dc = fan.build_desired_config('Fan', {"On": True})
        assert dc == {'fanOn': 1}

    @pytest.mark.parametrize(
        "homekit_value,fan_value",
        [(17, 1), (34, 2), (51, 3), (68, 4), (85, 5), (100, 6)]
    )
    def test_build_dc_fan_speed(self, fan, homekit_value, fan_value):
        dc = fan.build_desired_config('Fan', {'RotationSpeed': homekit_value})
        assert dc == {'fanSpeed': fan_value}

    @pytest.mark.parametrize(
        "homekit_value,fan_value",
        [(0, 'reverse'), (1, 'forward')]
    )
    def test_bdc_fan_direction(self, fan, homekit_value, fan_value):
        dc = fan.build_desired_config(
            'Fan', {'RotationDirection': homekit_value})
        assert dc == {'fanDirection': fan_value}

    def test_build_bdc_multi_value(self, fan):
        dc = fan.build_desired_config(
            'Fan',
            {'On': True, 'RotationSpeed': 30})
        assert dc == {'fanOn': 1, 'fanSpeed': 2}

    def test_build_desired_config_light(self, fan):
        dc = fan.build_desired_config(
            'Lightbulb', {'On': True, 'Brightness': 90})
        assert dc == {'lightOn': 1, 'lightBrightness': 90}

    @pytest.mark.parametrize(
        "srv,char,fan_key,fan_value,homekit_value", [
            ('Fan', 'RotationSpeed', 'fanSpeed', 1, 17),
            ('Fan', 'RotationSpeed', 'fanSpeed', 3, 50),
            ('Fan', 'RotationSpeed', 'fanSpeed', 6, 100),
            ('Fan', 'RotationDirection', 'fanDirection', 'reverse', 0),
            ('Fan', 'RotationDirection', 'fanDirection', 'forward', 1),
            ('Fan', 'On', 'fanOn', 1, True),
            ('Fan', 'On', 'fanOn', 0, False),
            ('Lightbulb', 'On', 'lightOn', 1, True),
            ('Lightbulb', 'Brightness', 'lightBrightness', 40, 40)
        ])
    def test_device_config(self,
                           fan, srv, char, fan_key, fan_value, homekit_value):
        fan._device_config[fan_key] = fan_value
        assert fan.device_config(srv, char) == homekit_value
