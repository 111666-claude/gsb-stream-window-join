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
        watermark = None if self.max_ts is None else self.max_ts - self.window
        if watermark is not None and event["ts"] < watermark:
            return []
        if self.max_ts is None or event["ts"] > self.max_ts:
            self.max_ts = event["ts"]

        out = []
        bucket = self.buckets.setdefault(event["key"], [])
        kept = []
        for other in bucket:
            counter.scanned += 1
            if other["ts"] < self.max_ts - self.window:
                continue
            kept.append(other)
            if other["stream"] == event["stream"]:
                continue
            if abs(other["ts"] - event["ts"]) <= self.window:
                out.append((other["id"], event["id"]))
        kept.append(event)
        self.buckets[event["key"]] = kept
        self.seen.add(event["id"])
        return out
