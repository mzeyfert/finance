import requests
from xml.etree import ElementTree
from typing import Union
import datetime
import logging


class Cbr:
    url = "http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx"
    def get_headers(self) -> dict:
        headers = {
            'Content-Type': 'application/soap+xml; charset=utf-8',
        }
        return headers

    def get_current_date(self) -> str:
        return datetime.datetime.today().strftime("%Y-%m-%d")
    
    def get_soap_payload(self) -> str:
        payload = f'''
            <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
            <soap12:Body>
                <KeyRateXML xmlns="http://web.cbr.ru/">
                <fromDate>{self.get_current_date()}</fromDate>
                <ToDate>{self.get_current_date()}</ToDate>
                </KeyRateXML>
            </soap12:Body>
            </soap12:Envelope>
        '''
        return payload
    
    def parse_soap_response(self, response):
        # Проходим по структуре ответа
        # И ищем тег rate
        soap_response = ElementTree.fromstring(response)
        for child in soap_response.iter():
            if child.tag == "Rate":
                return(child.text)
    
    def get_rate(self) -> Union[float, str]:
        try:
            response = requests.request("POST", self.url, headers=self.get_headers(), data=self.get_soap_payload())
        except requests.ConnectionError:
            logging.error("Connection error to cbr.ru")
            rate = "Is not provided. Check connection"
        else:
            rate = self.parse_soap_response(response.content)
        return rate


if __name__ == "__main__":
    cbr = Cbr()
    print(cbr.get_rate())