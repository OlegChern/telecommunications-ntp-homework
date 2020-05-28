import struct


class NtpPacket:
    _format = "!B B b b 11I"

    def __init__(self, version=2, mode=3, transmit=0):
        # initial octet
        self.LeapIndicator = 0
        self.Version = version
        self.Mode = mode

        # 1st octet
        self.Stratum = 0
        # 2nd octet
        self.Poll = 0
        # 3rd octet
        self.Precision = 0

        # 4-7 octet
        self.RootDelay = 0
        # 8-11 octet
        self.RootDispersion = 0
        # 12-15 octet
        self.ReferenceID = 0
        # 16-23 octet
        self.ReferenceTimestamp = 0
        # 24-31 octet
        self.OriginTimestamp = 0
        # 32-39 octet
        self.ReceiveTimestamp = 0
        # 40-47 octet
        self.TransmitTimestamp = transmit

    @staticmethod
    def get_fraction(number, precision):
        return int(number % 1. * 2. ** precision)

    def serialize(self):
        initial_octet = (self.LeapIndicator << 6) + (self.Version << 3) + self.Mode

        packet = struct.pack(self._format,
                             initial_octet,
                             self.Stratum,
                             self.Poll,
                             self.Precision,
                             int(self.RootDelay) + self.get_fraction(self.RootDelay, 16),
                             int(self.RootDispersion) + self.get_fraction(self.RootDelay, 16),
                             self.ReferenceID,
                             int(self.ReferenceTimestamp),
                             self.get_fraction(self.ReferenceTimestamp, 32),
                             int(self.OriginTimestamp),
                             self.get_fraction(self.OriginTimestamp, 32),
                             int(self.ReceiveTimestamp),
                             self.get_fraction(self.ReceiveTimestamp, 32),
                             int(self.TransmitTimestamp),
                             self.get_fraction(self.TransmitTimestamp, 32))

        return packet

    def deserialize(self, raw_data: bytes):
        unpacked = struct.unpack(self._format, raw_data)

        self.LeapIndicator = unpacked[0] >> 6
        self.Version = unpacked[0] >> 3 & 0b111
        self.Mode = unpacked[0] & 0b111

        self.Stratum = unpacked[1]
        self.Poll = unpacked[2]
        self.Precision = unpacked[3]

        self.RootDelay = (unpacked[4] >> 16) + (unpacked[4] & 0xFFFF) / 2 ** 16
        self.RootDispersion = (unpacked[5] >> 16) + (unpacked[5] & 0xFFFF) / 2 ** 16

        self.ReferenceID = f"{str((unpacked[6] >> 24) & 0xFF)} " \
                           f"{str((unpacked[6] >> 16) & 0xFF)} " \
                           f"{str((unpacked[6] >> 8) & 0xFF)} " \
                           f"{str(unpacked[6] & 0xFF)}"

        self.ReferenceTimestamp = unpacked[7] + unpacked[8] / 2 ** 32
        self.OriginTimestamp = unpacked[9] + unpacked[10] / 2 ** 32
        self.ReceiveTimestamp = unpacked[11] + unpacked[12] / 2 ** 32
        self.TransmitTimestamp = unpacked[13] + unpacked[14] / 2 ** 32
