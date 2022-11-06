from pathlib import WindowsPath
import sys
from tinydb import TinyDB
from tinydb.table import Table


class BancoDeDados:
    bd: TinyDB = None
    arquivos: Table = None
    pessoas: Table = None
    recibos: Table = None

    def definir_loc(self, loc: WindowsPath) -> None:
        self.bd = TinyDB(loc)
        self.arquivos = self.bd.table('arquivos')
        self.pessoas = self.bd.table('pessoas')
        self.recibos = self.bd.table('recibos')