from telegram.client import Telegram

from redis import Redis
from redis import ConnectionError

from datetime import datetime

from ah_settings import settings
from ah_settings import bmodes
from vicinfo import VictimInfo, victim_from_json

from termcolor import colored

import json
import random

# Settings
s = settings['del-edit-detector']

#
#
#

def pretty_print(mode: str, msg: str):
    mode_color = 'white'
    if mode == bmodes.FWD:
        mode_color = 'green'
    elif mode == bmodes.DETECTOR:
        mode_color = 'yellow'
    elif mode == bmodes.DBG:
        mode_color = 'blue'
    print(colored('[', 'white') + colored(mode, mode_color) + colored(']: ', 'white') + colored(msg, 'white'))

if not settings['del-edit-detector']['enable']:
    print("Detector not enabled")
    exit(1)

# Redis stuff
redis = Redis(
    s['redis']['host'], 
    port=s['redis']['port'], 
    db=s['redis']['db'], 
    password=s['redis']['password']
)

try:
    redis.ping()
except ConnectionError as e:
    pretty_print(bmodes.DETECTOR, colored('ERROR', 'red') + colored('Redis connection error:', 'white'))
    print(e)
    exit()

#
#
#

# initialize telegram client
tg = Telegram(
    settings['telegram_sender']['api-key'],
    settings['telegram_sender']['api-hash'],
    database_encryption_key=settings['telegram_sender']['database-encryption-key'],
    phone=settings['telegram_sender']['phone'],
    default_workers_queue_size=10000
)

# login to telegram, you may have to input a 2fa-key
tg.login()

def ps_get_message(message):
    print(message)

    try:
        obj = victim_from_json(message['data'])
        print("Victim:")
        print(obj)
        print()
    except:
        print("Could not decode message")

#
# Redis sub
#
ps = redis.pubsub()
ps.subscribe(**{'ah_user_notify': ps_get_message})

tg.idle()