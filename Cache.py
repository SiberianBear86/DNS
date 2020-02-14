import pickle
import time
from Answer import *

CACHE = {}


class CacheUnit:
    def __init__(self, answer, times):
        self.answer = answer
        self.time = times
        #self.ttl = ttl

    def __eq__(self, other):
        return self.time == other.time and self.answer == other.answer

    def __hash__(self):
        return hash(self.answer.ttl)


def get_cache():
    global CACHE
    return CACHE


def set_cache(cache):
    global CACHE
    CACHE = cache


def save_cache():
    with open('data.pkl', 'wb') as file:
        pickle.dump(CACHE, file)


def load_cache():
    global CACHE
    try:
        with open('data.pkl', 'rb') as file:
            CACHE = pickle.load(file)
    except EOFError:
        CACHE = {}
    update_cache()


def update_cache():
    global CACHE
    cur_time = time.time()
    keys_to_remove = []

    for key in CACHE:
        units_to_remove = []
        for ans in CACHE[key]:
            if cur_time - ans.time >= ans.answer.ttl:
                units_to_remove.append(ans)

        for unit in units_to_remove:
            CACHE[key].remove(unit)

        if not CACHE[key]:
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del CACHE[key]


def add_to_cache(packet):

    def get_answer(answer):
        if answer is not None:
            for ans in answer:
                add_record(ans)

    def add_record(answer):
        key = (answer.name, answer.type)
        flag = False
        if key in CACHE:
            for cache in CACHE[key]:
                if answer == cache.answer:
                    cache.time = answer.ttl
                    flag = True
            if not flag:
                CACHE[key].add(CacheUnit(answer, time.time()))
        else:
            CACHE[key] = {CacheUnit(answer, time.time())}

        print(CACHE)

    get_answer(packet.answer)
    get_answer(packet.authority)
    get_answer(packet.additional)


def get_from_cache(key, packet):
    data = []
    for p in CACHE[key]:
        if time.time() - p.time <= p.answer.ttl:
            data.append((p.answer.rdata, p.answer.rdlength))
        else:
            CACHE[key].discard(p)
    rdata = [d[0] for d in data]
    rdl = data[0][1]
    for data in rdata:
        packet.answer.append(Answer(key[0], key[1], 1, 300, rdl, data))
    packet.header.set_ancount(len(rdata))
    return packet




