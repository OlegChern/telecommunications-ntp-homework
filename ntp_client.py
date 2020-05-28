import socket
import datetime
import time

from ntp_packet import NtpPacket


class NtpClient:
    # NTP requires sending time in seconds passed from the 1st January 1900
    _format_difference = (datetime.date(1970, 1, 1) - datetime.date(1900, 1, 1)).days * 24 * 3600

    def __init__(self, ntp_server, server_port, waiting_time=5):
        self.ServerAddress = ntp_server
        self.ServerPort = server_port
        self.WaitingTime = waiting_time

    def get_time(self):
        cur_time = time.time() + self._format_difference
        request = NtpPacket(version=2, mode=3, transmit=cur_time)

        response = NtpPacket()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(self.WaitingTime)
            sock.sendto(request.serialize(), (self.ServerAddress, self.ServerPort))

            raw_response = sock.recv(48)
            time_of_arrival = time.time() + self._format_difference
            response.deserialize(raw_response)

        delta = self.calculate_delta(response.OriginTimestamp, response.TransmitTimestamp, response.ReceiveTimestamp,
                                     time_of_arrival)

        return datetime.datetime.fromtimestamp(time.time() + delta).strftime("%c")

    @staticmethod
    def calculate_delta(original, transmitted, received, arrived):
        transmission_time = ((arrived - original) - (transmitted - received)) / 2
        total_delta = received - original - transmission_time

        return total_delta


