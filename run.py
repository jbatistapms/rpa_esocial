import os, uuid
from dotenv import load_dotenv
from dropbox import Dropbox
from flask import Flask, request
load_dotenv()

app = Flask(__name__)
dbx = Dropbox(os.getenv('ACCESS_TOKEN'))

def gravar_arquivo(dados: bytes):
    if 'DEBUG' in os.environ:
        with open(f'./dev/{uuid.uuid4()}.csv', 'wb') as arq_csv:
            arq_csv.write(dados)
    else:
        dbx.files_upload(request.data, f'/rpas/{uuid.uuid4()}.csv')

@app.route('/envio', methods=['POST'])
def envio():
    gravar_arquivo(request.data)
    return "OK"

if __name__ == '__main__':
    app.run(debug=True)