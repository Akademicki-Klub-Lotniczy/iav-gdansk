import sys

FLIGHT_ALTITUDE = 1.6
FLIGHT_SPEED = 2
FLIGHT_SPEED_DURING_SCAN = 0.4
SIMULATE_BEACON = len(sys.argv) == 1


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'detailed': {
            'class': 'logging.Formatter',
            # 'datefmt': '%H:%M:%S',
            'format': '%(asctime)s %(name)-30s %(levelname)-20s %(message)s'
        }
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
        }
    },

    'loggers': {
        'states.calibrate_and_launch': {
            'level': 'INFO',
        },
        'states.find_marker_cross_method': {
            'level': 'DEBUG',
        },
        'states.fly_along_angle': {
            'level': 'DEBUG',
        },
        'states.land_on_final_marker': {
            'level': 'DEBUG',
        },
        'exceptions': {
            'level': 'DEBUG',
        },
        'fake_bluetooth': {
            'level': 'INFO',
        },
        'background': {
            'level': 'INFO',
        },
        'real_bluetooth': {
            'level': 'DEBUG',
        },
        'flight_utils': {
            'level': 'INFO',
        },
        'nav_utils': {
            'level': 'INFO',
        },
    },
}
