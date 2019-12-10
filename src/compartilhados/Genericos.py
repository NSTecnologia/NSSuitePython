# !/usr/bin/env python
# coding: utf-8

import os
import json
import base64
from datetime import datetime

class Genericos:

    # Esta função grava uma linha de texto em um arquivo de log
    @staticmethod
    def gravar_linha_log(modelo, conteudo_salvar):

        local_salvar = os.getcwd() + '\\log\\'
        if not os.path.exists(local_salvar):
            os.mkdir(local_salvar)

        data_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        nome_arq = local_salvar + str(datetime.today().date()) + '.txt'

        arquivo = open(nome_arq, 'a', encoding='utf-8')
        arquivo.write(str(data_atual) + ' - ' + modelo + ' - ' + conteudo_salvar + '\n')
        arquivo.close()
        pass

    # Esta função salva um XML
    @staticmethod
    def salvar_xml(xml, caminho, nome):
        local_save = caminho + nome + '.xml'
        arquivo = open(local_save, 'wb')
        arquivo.write(str(xml).encode())
        arquivo.close()
        pass

    # Esta função salva um JSON
    @staticmethod
    def salvar_json(data, caminho, nome):
        local_save = caminho + nome + '.json'
        arquivo = open(local_save, 'w')
        arquivo.write(json.dumps(data))
        arquivo.close()
        pass

    # Esta função salva um PDF
    @staticmethod
    def salvar_pdf(pdf, caminho, nome):
        local_save = caminho + nome + '.pdf'
        arquivo = open(local_save, 'wb')
        arquivo.write(base64.b64decode(pdf))
        pass
