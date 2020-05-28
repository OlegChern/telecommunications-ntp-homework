from ntp_client import NtpClient


def main():
    client = NtpClient()
    print(client.get_time())


if __name__ == "__main__":
    main()
