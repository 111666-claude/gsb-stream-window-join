"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def ev(eid, stream, key, ts):
    return {"id": eid, "stream": stream, "key": key, "ts": ts}


def count(events, window):
    joiner = core.Joiner(window)
    total = 0
    for event in events:
        total += len(joiner.feed(event, core.Counter()))
    return total


def run(name):
    if name == "boundary":
        _line({"joins": count([ev(1, "a", "k", 10), ev(2, "b", "k", 20)], 10)})
        return 0
    if name == "key":
        _line({"joins": count([ev(1, "a", "x", 10), ev(2, "b", "y", 10)], 10)})
        return 0
    if name == "late":
        events = [ev(1, "b", "k", 100), ev(2, "a", "k", 60), ev(3, "b", "k", 40)]
        _line({"joins": count(events, 50)})
        return 0
    if name == "idem":
        events = [ev(1, "a", "k", 10), ev(2, "b", "k", 10), ev(1, "a", "k", 10)]
        _line({"joins": count(events, 50)})
        return 0
    if name == "work":
        events = []
        for i in range(800):
            events.append(ev(i * 2 + 1, "a", "k%04d" % i, i))
            events.append(ev(i * 2 + 2, "b", "k%04d" % i, i))
        joiner = core.Joiner(10)
        counter = core.Counter()
        for event in events:
            joiner.feed(event, counter)
        _line({"events": 1600, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
