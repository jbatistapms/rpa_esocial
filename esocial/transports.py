from typing import Any, Dict
from urllib import response

from http.server import BaseHTTPRequestHandler
from lxml import etree
from M2Crypto import m2urllib2 as urllib2
from suds.transport.http import HttpTransport
from xsdata.formats.dataclass.transports import DefaultTransport

from . import token


class HttpTransportSuds(HttpTransport):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opener = token.opener
    
    def send(self, request):
        with open("xml_enviado.xml", 'wb') as r:
            xml_tree = etree.fromstring(request.message)
            r.write(etree.tostring(xml_tree, pretty_print=True))
        return super().send(request=request)


class TransportM2Crypto(DefaultTransport):
    def get(self, url: str, headers: Dict) -> bytes:
        print("Chamando TransportM2Crypto.get()")
        request = urllib2.Request(method='GET', url=url, headers=headers)
        response = urllib2.urlopen(request, timeout=self.timeout)
        return self.handle_response(response)

    def post(self, url: str, data: Any, headers: Dict) -> Any:
        print("Chamando TransportM2Crypto.post()")

        root = etree.fromstring(bytes(data, encoding='utf8'))
        xml = etree.tostring(root, pretty_print=True)

        with open('test2.xml', 'wb') as arq:
            arq.write(xml)
        
        if isinstance(data, str):
            data = data.encode()
        
        request = urllib2.Request(method='GET', url=url, data=data, headers=headers)
        response = urllib2.urlopen(request, timeout=self.timeout)
        
        return self.handle_response(response=response)

    @classmethod
    def handle_response(cls, response: response.addinfourl) -> bytes:
        print("Chamando TransportM2Crypto.handle_response()")
        if response.status not in (200, 500):
            cls.raise_for_status(response=response)

        data = response.read()
        
        with open('test3.xml', 'wb') as arq:
            arq.write(data)

        return data

    @classmethod
    def raise_for_status(response: response.addinfourl):
        print("Chamando TransportM2Crypto.raise_for_status()")
        reason = BaseHTTPRequestHandler.responses[response.status]
        http_error_msg = ""

        if 400 <= response.status < 500:
            http_error_msg = (
                f"{response.status} Client Error: {reason} for url: {response.url}"
            )

        elif 500 <= response.status < 600:
            http_error_msg = (
                f"{response.status} Server Error: {reason} for url: {response.url}"
            )

        if http_error_msg:
            raise urllib2.error.HTTPError(
                url=response.url, 
                code=response.status,
                msg=http_error_msg,
                hdrs=response.headers,
                fp=response
            )