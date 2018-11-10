from integra.monitor.dict import dict_helpers as dh


class Event:
    k: str
    k_desc: str
    s: str
    desc: str

    def __init__(self, s: str, k: str, desc: str) -> None:
        self.k = k
        self.k_desc = dh.get_event_category(k)
        self.s = s
        self.desc = desc
        pass

