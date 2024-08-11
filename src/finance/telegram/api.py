import sys

class TelegramApi:
    def get_updates(self):
        print('No updates')

def main():
    telegram_api = TelegramApi()
    telegram_api.get_updates()


if __name__ == "__main__":
    sys.exit(main())
