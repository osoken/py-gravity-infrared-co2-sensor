# -*- coding: utf-8 -*-

import os
import time
import json
from logging.config import dictConfig


from flask import Flask, jsonify

from . sensor import GravityInfraredCO2Sensor


def gen_app(config_object=None, logsetting_file=None):
    if logsetting_file is not None:
        with open(logsetting_file, 'r') as fin:
            dictConfig(json.load(fin))
    elif os.getenv('GRAVITYINFRAREDCO2SENSOR_LOGGER') is not None:
        with open(os.getenv('GRAVITYINFRAREDCO2SENSOR_LOGGER'), 'r') as fin:
            dictConfig(json.load(fin))
    app = Flask(__name__)
    app.config.from_object('gravityinfraredco2sensor.config')
    if os.getenv('GRAVITYINFRAREDCO2SENSOR') is not None:
        app.config.from_envvar('GRAVITYINFRAREDCO2SENSOR')
    if config_object is not None:
        app.config.update(**config_object)

    sensor = GravityInfraredCO2Sensor(
        app.config['DEVICE'],
        timeout=app.config['TIMEOUT'],
        hook=lambda v: app.logger.info('sensor value.', extra=v)
    )
    sensor.start()

    @app.route('/api/co2')
    def api_co2():
        return jsonify({
            'co2': sensor.co2,
            'timestamp': time.time()
        })

    return app
