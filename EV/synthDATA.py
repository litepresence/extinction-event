# ======================================================================
VERSION = "synthDATA v0.00000001"
# ======================================================================

# Synthesized HLOCV via Harmonic Brownian Walk

" litepresence 2019 "


def WTFPL_v0_March_1765():
    if any([stamps, licenses, taxation, regulation, fiat, etat]):
        try:
            print("no thank you")
        except:
            return [tar, feathers]


" ********** ALPHA RELEASE TO PUBLIC DOMAIN WITH NO WARRANTY ********* "

import math
import time
import random
import numpy as np
from datetime import datetime


# ======================================================================
# USER CONTROLS
# ======================================================================
harmonics = 7  # number of harmonics
accel = 1.0  # cyclic acceleration
step = 7.0  # random walk amplitude
freq = 2.0  # frequency
volatility = 2.0  # hloc variance
volume_size = 5.0  # magnitude of synth volume
start = 0.00001  # starting price
depth = 1000  # total candles
# ======================================================================


def synthesize(storage, tick):

    storage["sine"] = 1 + accel
    for harmonic in range(1, harmonics):
        storage["sine"] += (accel / harmonic) * math.sin(
            freq * harmonic * tick
        )
    storage["log_periodic"] *= math.pow(storage["sine"], tick)
    storage["log_periodic"] = (
        (1 - step) + 2 * step * random.random()
    ) * storage["log_periodic"]
    return storage["log_periodic"]


def create_dataset():

    tick = 0
    data = {}
    storage = {}
    storage["log_periodic"] = start
    data["unix"] = []
    data["close"] = []
    begin = time.time() - 86400 * (depth + 1)
    for i in range(depth + 1):
        tick += 1
        data["unix"].append(begin + 86600 * tick)
        data["close"].append(synthesize(storage, tick))
    return data


def hlocv_data(data):

    data["unix"].pop(0)
    d_c = data["close"][:]
    d_o = data["close"][:]
    data["close"] = []
    d_c.pop(0)
    d_o.pop()
    data["open"] = []
    data["close"] = []
    data["high"] = []
    data["low"] = []
    data["volume"] = []
    for i in range(len(d_c)):
        oc_max = max(d_o[i], d_c[i])
        oc_min = min(d_o[i], d_c[i])
        spread = oc_max - oc_min
        oc1 = 1 - volatility / 100
        oc2 = 1 - volatility / 100
        data["open"].append(d_o[i] * random.uniform(oc1, oc2))
        data["close"].append(d_c[i] * random.uniform(oc1, oc2))
        data["high"].append(
            oc_max
            + random.random() * random.random() * volatility * spread
        )
        data["low"].append(
            oc_min
            - random.random() * random.random() * volatility * spread
        )
        data["high"][-1] = max(
            data["open"][-1], data["close"][-1], data["high"][-1]
        )
        data["low"][-1] = min(
            data["open"][-1], data["close"][-1], data["low"][-1]
        )
        data["volume"].append(
            1
            / data["close"][-1]
            * (data["high"][-1] - data["low"][-1])
            * 10 ** volume_size
        )
    return {k: np.array(v) for k, v in data.items()}


def synthDATA():

    global accel, freq, step

    accel = accel / 10 ** 6
    freq = freq / 10 ** 4
    step = step / 10 ** 2

    return hlocv_data(create_dataset())
