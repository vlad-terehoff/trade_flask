from tronpy.keys import PrivateKey
from random import random


def create_usdt_wallet():
    private_key = PrivateKey.random()
    address = private_key.public_key.to_base58check_address()
    return address


def generate_tax():
    return random() / 100
