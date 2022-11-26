import os, re, uuid
from pathlib import PurePath

import dropbox
from dotenv import load_dotenv
from flask import Flask, request
load_dotenv(os.path.join(PurePath(__file__).parent, '.env'))

app = Flask(__name__)
dbx = dropbox.Dropbox(
    oauth2_refresh_token=os.getenv('DROPBOX_REFRESH_TOKEN'),
    app_key=os.getenv('DROPBOX_APP_KEY'),
)
debug = os.getenv('DEBUG', '0') == '1'
re_token = re.compile(r'Bearer (?P<token>.+)')
tokens_autorizados = os.getenv('APP_TOKENS').split(',')

def checar_token(auth) -> bool:
    token = re_token.search(auth)
    return token is not None and token.group('token') in tokens_autorizados

def gravar_arquivo(dados: bytes) -> None:
    uuid_ = uuid.uuid4()
    if debug:
        with open(f'./dev/Recibos/Api/{uuid_}.txt', 'wb') as arq_csv:
            arq_csv.write(dados)
    else:
        if request.args.get('test', 'Falso') == 'Verdadeiro':
            dbx.files_upload(request.data, f'/Testes/Recibos/Api/{uuid_}_test.txt')
        else:
            dbx.files_upload(request.data, f'/Recibos/Api/{uuid_}.txt')

@app.route('/', methods=['GET'])
def home():
    return "Prefeitura Municipal de Sapucaia", 200

@app.route('/envio', methods=['POST'])
def envio():
    if checar_token(request.headers.get('Authorization', '')):
        gravar_arquivo(request.data)
        return "OK", 200
    else:
        return "INVALID TOKEN", 403

if __name__ == '__main__':
    app.run(debug=True)