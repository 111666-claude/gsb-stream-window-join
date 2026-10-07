"""按事件键与时间窗口配对。"""


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


class Joiner:
    def __init__(self, window):
        self.window = window
        self.buckets = {}
        self.seen = set()
        self.max_ts = None

    def feed(self, event, counter):
        if event["id"] in self.seen:
            return []
        if self.max_ts is not None and event["ts"] < self.max_ts - self.window:
            return []
        self.seen.add(event["id"])
        if self.max_ts is None or event["ts"] > self.max_ts:
            self.max_ts = event["ts"]
        bucket = self.buckets.setdefault(event["key"], [])
        floor = self.max_ts - 2 * self.window
        bucket[:] = [other for other in bucket if other["ts"] >= floor]
        out = []
        for other in bucket:
            counter.scanned += 1
            if other["stream"] == event["stream"]:
                continue
            if abs(other["ts"] - event["ts"]) <= self.window:
                out.append((other["id"], event["id"]))
        bucket.append(event)
        return out
