from datetime import datetime


class SIAHeader:

    crc: bytes
    length: int
    id: str
    stmp: str
    seq: int
    lprev: str
    ts: str

    def __init__(self, payload: bytes) -> None:
        self.crc = payload[:4]
        self.lenght = payload[4:4 + 4]
        self.id = payload[payload.find(b'"'):payload.rfind(b'"') + 1]
        self.stmp = payload[payload.rfind(b'"') + 1:payload.find(b'[')]
        self.seq = self.stmp[:self.stmp.find(b'L')]
        self.lprev = self.stmp[self.stmp.find(b'L'):self.stmp.find(b'#')]
        self.acct = self.stmp[self.stmp.find(b'#') + 1:payload.find(b'[')]
        t_str = payload[payload.find(b']') + 2:]
        self.ts = datetime.strptime(t_str.decode("utf-8"), '%H:%M:%S,%m-%d-%Y') if t_str else datetime.now()


class CIDPayload:

    acct: str
    q: int
    xyz: int
    ss: str
    ccc: str


    def __init__(self, payload: bytes) -> None:
        self.acct_number = payload[:5]
        self.q = int(payload[6:7])
        self.xyz = int(payload[7:10])
        self.ss = payload[11:13].decode("utf-8")
        self.ccc = payload[14:].decode("utf-8")


class IntegraMessage:

    header: SIAHeader
    payload: CIDPayload = None

    def __init__(self, payload: bytes) -> None:
        self.header = SIAHeader(payload)
        pload = payload[payload.find(b'[') + 1:payload.find(b']')]
        if pload:
            self.payload = CIDPayload(pload)
