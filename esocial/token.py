import os, sys
from pathlib import WindowsPath
from pprint import pprint

import pkcs11, signxml
from lxml import etree
from M2Crypto import m2, Engine, SSL
from M2Crypto import m2urllib2 as urllib2

from . import core

id_ = 'pkcs11'
MODULE_PATH = os.getenv('MODULE_PATH')
OPENSLL_DIR = os.getenv('OPENSLL_DIR')
KEY_LABEL = os.getenv('KEY_LABEL')
TOKEN_ID = os.getenv('TOKEN_ID')
TOKEN_LABEL = os.getenv('TOKEN_LABEL')
TOKEN_SLOT = os.getenv('TOKEN_SLOT')

sys.path.append(OPENSLL_DIR)

engine = Engine.load_dynamic_engine(
    id_,
    str(WindowsPath(__file__).parent.joinpath("pacotes", "pkcs11.dll"))
)
ssl_engine = Engine.Engine(id_)
ssl_engine.ctrl_cmd_string("MODULE_PATH", MODULE_PATH)
#ssl_engine.ctrl_cmd_string("PIN", TOKEN_PIN)
ssl_engine.init()

token = f"slot_{TOKEN_SLOT}-id_{TOKEN_ID}"
key = ssl_engine.load_private_key(token)
cert = ssl_engine.load_certificate(token)

ssl_context = SSL.Context('sslv23')
ssl_context.set_cipher_list("HIGH:!aNULL:!eNULL:@STRENGTH")
ssl_context.set_default_verify_paths()
ssl_context.set_client_CA_list_from_file(cafile=core.ca_path())

#SSL.Connection.postConnectionCheck = None

m2.ssl_ctx_use_x509(ssl_context.ctx, cert.x509)
m2.ssl_ctx_use_pkey_privkey(ssl_context.ctx, key.pkey)

opener = urllib2.build_opener(ssl_context)
urllib2.install_opener(opener=opener)

def teste_requisicao():
    try:
        request = urllib2.Request(method='GET', url=core.URL_WS_ENV_RESTRITO)
        with urllib2.urlopen(request) as resp:
            pprint(dict(resp.headers))
            print(resp.status)
            print(type(resp))
    except Exception as erro:
        print(erro.fp.read())
        print(erro.fp.headers)
        print(erro.fp.code)

def obter_token():
    lib = pkcs11.lib(MODULE_PATH)
    token = lib.get_token(token_label=TOKEN_LABEL)
    session = token.open()
    return session.get_key(
        object_class=pkcs11.constants.ObjectClass.PRIVATE_KEY,
        label=KEY_LABEL,
    )

def assinar(xml):
    root  = etree.fromstring(bytes(xml, encoding='utf8'))
    return signxml.XMLSigner(
        method=signxml.methods.enveloped,
        signature_algorithm="rsa-sha256",
        digest_algorithm="sha256",
        c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315",
    ).sign(
        data=root,
        key=PrimaryKey(),
        cert=cert.as_pem(),
    )

class PrimaryKey(object):
    def __init__(self) -> None:
        self._key = obter_token()
    
    def sign(self, data: bytes, padding=None, algorithm=None):
        return self._key.sign(
            data=data,
            mechanism=pkcs11.mechanisms.Mechanism.SHA256_RSA_PKCS,
        )

if __name__ == '__main__':
    print(obter_token())