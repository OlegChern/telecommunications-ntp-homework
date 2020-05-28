import argparse

from ntp_client import NtpClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser("a simple NTP client which will print accurate time")
    parser.add_argument("-a", "--address", help="desired NTP server address", type=str, default="pool.ntp.org")
    parser.add_argument("-p", "--port", help="desired NTP server port", type=int, default=123)
    parser.add_argument("-w", "--wait", help="server response waiting time (in seconds)", type=int, default=123)

    args = parser.parse_args()

    client = NtpClient(args.address, args.port, args.wait)
    print(client.get_time())
