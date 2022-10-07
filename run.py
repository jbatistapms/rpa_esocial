import os, uuid
from pathlib import PurePath
from dotenv import load_dotenv
from dropbox import Dropbox
from flask import Flask, request
load_dotenv(os.path.join(PurePath(__file__).parent, '.env'))

app = Flask(__name__)
dbx = Dropbox(os.getenv('DROPBOX_TOKEN'))
tokens_autorizados = os.getenv('TOKENS').split(',')

def checar_token(token) -> bool:
    _, token = token.split()
    return token in tokens_autorizados

def gravar_arquivo(dados: bytes) -> None:
    if 'DEBUG' in os.environ:
        with open(f'./dev/{uuid.uuid4()}.csv', 'wb') as arq_csv:
            arq_csv.write(dados)
    else:
        dbx.files_upload(request.data, f'/rpas/{uuid.uuid4()}.csv')

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