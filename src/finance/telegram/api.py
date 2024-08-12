import sys
import argparse
import requests
import time
from dataclasses import dataclass
from typing import Dict
import logging
import re

logger = logging

@dataclass
class URIComponents:
    telegram_url: str = 'https://api.telegram.org'
    bot: str = 'bot'

@dataclass
class TelegramMethods:
    get_updates: str = 'getUpdates'
    send_messages: str = 'sendMessage'

@dataclass
class Message:
    chat: int
    text: str

@dataclass
class Update:
    update_id: int
    message: Message

class TelegramApi:
    url = URIComponents.telegram_url
    
    def __init__(self, token: str):
        self.token: str = token
        self.offset = None

    def get_uri(self, method: str) -> str:
        return f'{self.url}/{URIComponents.bot}{self.token}/{method}'

    def parse_updates(self, updates: Dict) -> Update:
        messages = updates.get('result')
        if not messages:
            return None
        last_message: Dict = messages[-1]
        message = Message(chat=last_message.get('message', {}).get('chat', {}).get('id'),
                          text=last_message.get('message', {}).get('text')
                          )
        message_obj = Update(update_id=last_message.get('update_id'),
                             message=message)
        return message_obj

    def send_message(self, chat_id: str, text: str):
        try:
            uri = self.get_uri(method=TelegramMethods.send_messages)
            response = requests.get(url=uri, params={'text': text, 'chat_id': chat_id})
        except requests.exceptions.ConnectionError:
            logger.error(f'Error with connection to {self.url}')
            return None

    def get_text(self, input_text: str) -> str:
        if re.match(r'^кс$', input_text):
            answer = 'КC: <нужно добавить значение>'
        else:
            answer = 'Неизвестный формат сообщения'
        return answer

    def get_updates(self):
        try:
            uri = self.get_uri(method=TelegramMethods.get_updates)
            response = requests.get(url=uri, params={'offset': self.offset})
        except requests.exceptions.ConnectionError:
            logger.error(f'Error with connection to {self.url}')
            return None
        else:
            return response.json()

    def start_server(self) -> None:
        time_to_wait = 5
        while True:
            updates = self.get_updates()
            last_message = self.parse_updates(updates)
            if last_message:
                text = self.get_text(last_message.message.text)
                self.send_message(chat_id=last_message.message.chat, text=text)
                self.offset = last_message.update_id + 1
            time.sleep(time_to_wait)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', required=True)
    cli_args = parser.parse_args()
    telegram_api = TelegramApi(token=cli_args.token)
    telegram_api.start_server()  


if __name__ == "__main__":
    sys.exit(main())
