"""按事件键与时间窗口配对。"""


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


class Joiner:
    def __init__(self, window):
        self.window = window
        self.events = []
        self.seen = set()

    def feed(self, event, counter):
        out = []
        for other in self.events:
            counter.scanned += 1
            if other["stream"] == event["stream"]:
                continue
            if abs(other["ts"] - event["ts"]) < self.window:
                out.append((other["id"], event["id"]))
        self.seen.add(event["id"])
        self.events.append(event)
        return out
