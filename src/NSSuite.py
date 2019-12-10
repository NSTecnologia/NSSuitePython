# !/usr/bin/env python
# coding: utf-8

from src.compartilhados.Genericos import Genericos
from src.compartilhados.Endpoints import Endpoints
from src.compartilhados.Parametros import Parametros
from src.requisicoes.nfe.DownloadReqNFe import DownloadReqNFe

from src.retornos.bpe.EmitirSincronoRetBPe import EmitirSincronoRetBPe
from src.requisicoes.bpe.ConsStatusProcessamentoReqBPe import ConsStatusProcessamentoReqBPe
from src.requisicoes.bpe.DownloadReqBPe import DownloadReqBPe

from src.retornos.cte.EmitirSincronoRetCTe import EmitirSincronoRetCTe
from src.requisicoes.cte.ConsStatusProcessamentoReqCTe import ConsStatusProcessamentoReqCTe
from src.requisicoes.cte.DownloadReqCTe import DownloadReqCTe

from src.retornos.mdfe.EmitirSincronoRetMDFe import EmitirSincronoRetMDFe
from src.requisicoes.mdfe.ConsStatusProcessamentoReqMDFe import ConsStatusProcessamentoReqMDFe
from src.requisicoes.mdfe.DownloadReqMDFe import DownloadReqMDFe

from src.retornos.nfce.EmitirSincronoRetNFCe import EmitirSincronoRetNFCe
from src.requisicoes.nfce.DownloadReqNFCe import DownloadReqNFCe
from src.requisicoes.nfce.Impressao import Impressao

from src.retornos.nfe.EmitirSincronoRetNFe import EmitirSincronoRetNFe
from src.requisicoes.nfe.ConsStatusProcessamentoReqNFe import ConsStatusProcessamentoReqNFe

import requests
import os
import json
import webbrowser
import time


# json.loads = str to dicts para pegar itens
# json.dumps = dicts to str

class NSSuite:
    __token = 'COLOQUE_TOKEN'

    # Esta função envia um conteúdo para uma URL, em requisições do tipo POST
    @staticmethod
    def __envia_conteudo_para_api(conteudo, url, tp_conteudo):

        if tp_conteudo.upper() == 'TXT':
            content = 'text/plain;charset=utf-8'
        elif tp_conteudo.upper() == 'XML':
            content = 'application/xml;charset=utf-8'
        else:
            content = 'application/json;charset=utf-8'

        headers = {
            'Content-Type': content,
            'X-AUTH-TOKEN': NSSuite.__token
        }

        retorno = requests.post(url=url, timeout=1000, data=conteudo, headers=headers).content.decode('utf-8')

        return json.loads(retorno)

    # Métodos específicos de BPe
    @staticmethod
    def emitir_bpe_sincrono(conteudo, tp_conteudo, cnpj, tp_down, tp_amb, caminho, exibe_na_tela):
        modelo = '63'
        erros = ''
        status_envio = ''
        status_consulta = ''
        status_download = ''
        motivo = ''
        ns_nrec = ''
        ch_bpe = ''
        c_stat = ''
        n_prot = ''

        Genericos.gravar_linha_log(modelo, '[EMISSAO_SINCRONA_INICIO]')
        resposta = NSSuite.emitir_documento(modelo, conteudo, tp_conteudo)
        status_envio = resposta['status']

        if status_envio == 200 or status_envio == -6:
            ns_nrec = resposta['nsNRec']
            time.sleep(Parametros.TEMPO_ESPERA)

            cons_status_processamento = ConsStatusProcessamentoReqBPe(cnpj, ns_nrec, tp_amb)
            resposta = NSSuite.consultar_status_processamento(modelo, cons_status_processamento)
            status_consulta = resposta['status']

            if status_consulta == 200:
                c_stat = resposta['cStat']

                if c_stat == '100':
                    ch_bpe = resposta['chBPe']
                    n_prot = resposta['nProt']
                    motivo = resposta['xMotivo']

                    download_req_bpe = DownloadReqBPe(ch_bpe, tp_down, tp_amb)
                    resposta = NSSuite.dowload_documento_e_salvar(modelo, download_req_bpe, caminho, ch_bpe + '-BPe',
                                                                  exibe_na_tela)
                    status_download = resposta['status']

                    if not status_download == 200:
                        motivo = resposta['motivo']
                else:
                    motivo = resposta['xMotivo']
            elif status_consulta == -2:
                c_stat = resposta['cStat']
                motivo = resposta['erro']['motivo']
            else:
                motivo = resposta['motivo']

        elif status_envio == -5:
            c_stat = resposta['erro']['cStat']
            motivo = resposta['erro']['xMotivo']
        elif status_envio == -4 or status_envio == -2:
            motivo = resposta['motivo']
            erros = resposta['erros']
        else:
            try:
                motivo = resposta['motivo']
            except:
                motivo = json.dumps(resposta)

        emitir_sincrono_bpe = EmitirSincronoRetBPe(ch_bpe, status_envio, status_consulta, status_download,
                                                   c_stat, n_prot, motivo, ns_nrec, erros)
        retorno = emitir_sincrono_bpe.__dict__
        Genericos.gravar_linha_log(modelo, '[JSON_RETORNO]')
        Genericos.gravar_linha_log(modelo, json.dumps(retorno, ensure_ascii=False))
        Genericos.gravar_linha_log(modelo, '[EMISSAO_SINCRONA_FIM]')

        return retorno

    @staticmethod
    def nao_embarque(modelo, nao_emb_req_bpe):
        global url_nao_emb
        if modelo == '63':
            url_nao_emb = Endpoints.BPeNaoEmb
        else:
            raise Exception('Não definido endpoint para o modelo ' + modelo)

        data = nao_emb_req_bpe.__dict__
        Genericos.gravar_linha_log(modelo, '[NAO_EMBARQUE_DADOS]')
        Genericos.gravar_linha_log(modelo, json.dumps(data, ensure_ascii=False))

        resposta = NSSuite.__envia_conteudo_para_api(json.dumps(data), url_nao_emb, 'json')

        Genericos.gravar_linha_log(modelo, '[NAO_EMBARQUE_RESPOSTA]')
        Genericos.gravar_linha_log(modelo, json.dumps(resposta, ensure_ascii=False))

        return resposta

    @staticmethod
    def nao_embarque_e_salvar(modelo, nao_emb_req_bpe, download_evento_req, caminho, chave, exibe_na_tela):
        resposta = NSSuite.nao_embarque(modelo, nao_emb_req_bpe)
        status = resposta['status']

        if status == 200:
            c_stat = resposta['retEvento']['cStat']
            if c_stat == 135:
                resposta_download = NSSuite.download_evento_e_salvar(modelo, download_evento_req, caminho, chave, '',
                                                                     exibe_na_tela)
            else:
                print('Ocorreu um erro ao não embarcar, veja o retorno da API para mais informaçõe')
        return resposta

    # Métodos específicos de CTe
    @staticmethod
    def emitir_cte_sincrono(conteudo, modelo, tp_conteudo, cnpj, tp_down, tp_amb, caminho, exibe_na_tela):
        erros = ''
        status_envio = ''
        status_consulta = ''
        status_download = ''
        motivo = ''
        ns_nrec = ''
        ch_cte = ''
        c_stat = ''
        n_prot = ''

        Genericos.gravar_linha_log(modelo, '[EMISSAO_SINCRONA_INICIO]')
        resposta = NSSuite.emitir_documento(modelo, conteudo, tp_conteudo)
        status_envio = resposta['status']

        if status_envio == 200 or status_envio == -6:
            ns_nrec = resposta['nsNRec']
            time.sleep(Parametros.TEMPO_ESPERA)

            cons_status_processamento = ConsStatusProcessamentoReqCTe(cnpj, ns_nrec, tp_amb)
            resposta = NSSuite.consultar_status_processamento(modelo, cons_status_processamento)
            status_consulta = resposta['status']

            if status_consulta == 200:
                c_stat = resposta['cStat']
                if c_stat == '100' or c_stat == '150':
                    ch_cte = resposta['chCTe']
                    n_prot = resposta['nProt']
                    motivo = resposta['xMotivo']

                    download_req_cte = DownloadReqCTe(ch_cte, cnpj, tp_down, tp_amb)
                    resposta = NSSuite.dowload_documento_e_salvar(modelo, download_req_cte, caminho,
                                                                  ch_cte + '-CTe', exibe_na_tela)
                    status_download = resposta['status']
                    if not status_download == 200:
                        motivo = resposta['motivo']
                else:
                    motivo = resposta['xMotivo']
            else:
                motivo = resposta['motivo']
                erros = resposta['erros']
        elif status_envio == -7:
            motivo = resposta['motivo']
            ns_nrec = resposta['nsNRec']
        elif status_envio == -4:
            motivo = resposta['erro']['xMotivo']
            cStat = resposta['erro']['cStat']
        else:
            try:
                motivo = resposta['motivo']
            except '':
                motivo = resposta

        emitir_sincrono_cte = EmitirSincronoRetCTe(ch_cte, status_envio, status_consulta, status_download,
                                                   c_stat, n_prot, motivo, ns_nrec, erros)
        retorno = emitir_sincrono_cte.__dict__
        Genericos.gravar_linha_log(modelo, '[JSON_RETORNO]')
        Genericos.gravar_linha_log(modelo, json.dumps(retorno, ensure_ascii=False))
        Genericos.gravar_linha_log(modelo, '[EMISSAO_SINCRONA_FIM]')

        return retorno

    @staticmethod
    def informar_gtv(modelo, inf_gtv_req_cte):
        global url_inf_gtv
        if modelo == '57' or modelo == '67':
            url_inf_gtv = Endpoints.CTeInfGTV
        else:
            raise Exception("Não definido endpoint de informação de GTV para o modelo " + modelo);

        data = inf_gtv_req_cte.__dict__
        Genericos.gravar_linha_log(modelo, '[INFORMACOES_GTV_DADOS]')
        Genericos.gravar_linha_log(modelo, json.dumps(data, ensure_ascii=False))

        resposta = NSSuite.__envia_conteudo_para_api(json.dumps(data), url_inf_gtv, 'json')

        Genericos.gravar_linha_log(modelo, '[INFORMACOES_GTV_RESPOSTA]')
        Genericos.gravar_linha_log(modelo, json.dumps(resposta, ensure_ascii=False))

        return resposta

    @staticmethod
    def informar_gtv_e_salvar(modelo, inf_gtv_req_cte, download_evento_req, caminho, chave, exibe_na_tela):
        resposta = NSSuite.informar_gtv(modelo, inf_gtv_req_cte)
        status = resposta['status']

        if status == 200:
            resposta_download = NSSuite.download_evento_e_salvar(modelo, download_evento_req, caminho, chave, '',
                                                                 exibe_na_tela)
        else:
            print('Ocorreu um erro ao cancelar, veja o retorno da API para mais informações')
        return resposta

    # Métodos específicos de MDFe
    @staticmethod
    def emitir_mdfe_sincrono(conteudo, tp_conteudo, cnpj, tp_down, tp_amb, caminho, exibe_na_tela):

        modelo = '58'
        status_envio = ''
        status_consulta = ''
        status_download = ''
        motivo = ''
        ns_nrec = ''
        ch_mdfe = ''
        c_stat = ''
        n_prot = ''
        erros = ''

        Genericos.gravar_linha_log(modelo, '[EMISSAO_SINCRONA_INICIO]')
        resposta = NSSuite.emitir_documento(modelo, conteudo, tp_conteudo)
        status_envio = resposta['status']

        if status_envio == 200 or status_envio == -6:
            ns_nrec = resposta['nsNRec']
            time.sleep(Parametros.TEMPO_ESPERA)

            cons_status_processamento = ConsStatusProcessamentoReqMDFe(cnpj, ns_nrec, tp_amb)
            resposta = NSSuite.consultar_status_processamento(modelo, cons_status_processamento)
            status_consulta = resposta['status']

            if status_consulta == 200:
                c_stat = resposta['cStat']
                if c_stat == '100':
                    ch_mdfe = resposta['chMDFe']
                    n_prot = resposta['nProt']
                    motivo = resposta['xMotivo']

                    download_req_mdfe = DownloadReqMDFe(ch_mdfe, tp_down, tp_amb)
                    resposta = NSSuite.dowload_documento_e_salvar(modelo, download_req_mdfe, caminho, ch_mdfe + '-MDFe',
                                                                  exibe_na_tela)
                    status_download = resposta['status']

                    if not status_download == 200:
                        motivo = resposta['motivo']
                else:
                    motivo = resposta['xMotivo']
            elif status_consulta == -2:
                c_stat = resposta['erro']['cStat']
                motivo = resposta['erro']['xMotivo']
            else:
                motivo = resposta['motivo']
        elif status_envio == -5:
            c_stat = resposta['erro']['cStat']
            motivo = resposta['erro']['xMotivo']
        elif status_envio == -4 or status_envio == -2:
            motivo = resposta['motivo']
            erros = resposta['erros']
        elif status_envio == -999:
            motivo = resposta['erro']['xMotivo']
        else:
            try:
                motivo = resposta['motivo']
            except '':
                motivo = resposta

        emitir_sincrono_mdfe = EmitirSincronoRetMDFe(ch_mdfe, status_envio, status_consulta, status_download,
                                                     c_stat, n_prot, motivo, ns_nrec, erros)
        retorno = emitir_sincrono_mdfe.__dict__
        Genericos.gravar_linha_log(modelo, '[JSON_RETORNO]')
        Genericos.gravar_linha_log(modelo, json.dumps(retorno, ensure_ascii=False))
        Genericos.gravar_linha_log(modelo, '[EMISSAO_SINCRONA_FIM]')

        return retorno

    @staticmethod
    def encerrar_documento(modelo, encerrar_req):
        global url_encerramento
        if modelo == '58':
            url_encerramento = Endpoints.MDFeEncerramento
        else:
            raise Exception('Não definido endpoint de encerramento para o modelo ' + modelo)

        data = encerrar_req.__dict__
        Genericos.gravar_linha_log(modelo, '[ENCERRAMENTO_DADOS]')
        Genericos.gravar_linha_log(modelo, json.dumps(data, ensure_ascii=False))

        resposta = NSSuite.__envia_conteudo_para_api(json.dumps(data), url_encerramento, 'json')

        Genericos.gravar_linha_log(modelo, '[ENCERRAMENTO_RESPOSTA]')
        Genericos.gravar_linha_log(modelo, json.dumps(resposta, ensure_ascii=False))

        return resposta

    @staticmethod
    def encerrar_documento_e_salvar(modelo, encerrar_req, download_evento_req, caminho, chave, exibe_na_tela):
        resposta = NSSuite.encerrar_documento(modelo, encerrar_req)
        status = resposta['status']
        if status == 200:
            resposta_download = NSSuite.download_evento_e_salvar(modelo, download_evento_req, caminho, chave, '1',
                                                                 exibe_na_tela)
        else:
            print('Ocorreu um erro ao encerrar, veja o retorno da API para mais informações')

        return resposta

    @staticmethod
    def incluir_condutor(modelo, inc_condutor_req):
        global url_inc_condutor
        if modelo == '58':
            url_inc_condutor = Endpoints.MDFeIncCondutor
        else:
            raise Exception("Não definido endpoint de inclusão de condutor para o modelo " + modelo)

        data = inc_condutor_req.__dict__
        Genericos.gravar_linha_log(modelo, '[INC_CONDUTOR_DADOS]')
        Genericos.gravar_linha_log(modelo, json.dumps(data, ensure_ascii=False))

        resposta = NSSuite.__envia_conteudo_para_api(json.dumps(data), url_inc_condutor, 'json')

        Genericos.gravar_linha_log(modelo, '[INC_CONDUTOR_RESPOSTA]')
        Genericos.gravar_linha_log(modelo, json.dumps(resposta, ensure_ascii=False))

        return resposta

    @staticmethod
    def incluir_condutor_e_salvar(modelo, inc_condutor_req, download_evento_req, caminho, chave, exibe_na_tela):
        resposta = NSSuite.incluir_condutor(modelo, inc_condutor_req)
        status = resposta['status']

        if status == 200:
            resposta_download = NSSuite.download_evento_e_salvar(modelo, download_evento_req, caminho, chave, '',
                                                                 exibe_na_tela)
        else:
            print('Ocorreu um erro ao incluir condutor, veja o retorno da API para mais informações')

        return resposta

    @staticmethod
    def consultar_nao_encerrados(modelo, cons_nao_encerrados_req):
        global url_nao_encerrados
        if modelo == '58':
            url_nao_encerrados = Endpoints.MDFeConsNaoEncerrados
        else:
            raise Exception("Não definido endpoint de consulta de não encerrados para o modelo " + modelo)

        data = cons_nao_encerrados_req.__dict__
        Genericos.gravar_linha_log(modelo, '[CONS_NAO_ENCERRADOS_DADOS]')
        Genericos.gravar_linha_log(modelo, json.dumps(data, ensure_ascii=False))

        resposta = NSSuite.__envia_conteudo_para_api(json.dumps(data), url_nao_encerrados, 'json')

        Genericos.gravar_linha_log(modelo, '[CONS_NAO_ENCERRADOS_RESPOSTA]')
        Genericos.gravar_linha_log(modelo, json.dumps(resposta, ensure_ascii=False))

        return resposta

    # Métodos específicos de NFCe
    @staticmethod
    def emitir_nfce_sincrono(conteudo, tp_conteudo, tp_amb, caminho, exibe_na_tela):
        modelo = '65'
        status_envio = ''
        status_download = ''
        motivo = ''
        ch_nfe = ''
        c_stat = ''
        n_prot = ''
        erros = ''

        Genericos.gravar_linha_log(modelo, '[EMISSAO_SINCRONA_INICIO]')
        resposta = NSSuite.emitir_documento(modelo, conteudo, tp_conteudo)
        status_envio = resposta['status']

        if status_envio == 100 or status_envio == -100:
            c_stat = resposta['nfeProc']['cStat']
            if c_stat == 100 or c_stat == 150:
                ch_nfe = resposta['nfeProc']['chNFe']
                n_prot = resposta['nfeProc']['nProt']
                motivo = resposta['nfeProc']['xMotivo']
                time.sleep(Parametros.TEMPO_ESPERA)

                impressao = Impressao()
                download_req_nfce = DownloadReqNFCe(ch_nfe, impressao.__dict__, None, tp_amb)
                resposta = NSSuite.dowload_documento_e_salvar(modelo, download_req_nfce, caminho, ch_nfe + '-NFe',
                                                              exibe_na_tela)
                status_download = resposta['status']

                if status_download == 200:
                    motivo = resposta['motivo']
            else:
                motivo = resposta['nfeProc']['xMotivo']
        elif status_envio == -995:
            motivo = resposta['motivo']
            erros = resposta['erros']
        else:
            motivo = resposta['motivo']

        emitir_sincrono_nfce = EmitirSincronoRetNFCe(ch_nfe, status_envio, None, status_download,
                                                     c_stat, n_prot, motivo, None, erros)
        retorno = emitir_sincrono_nfce.__dict__
        Genericos.gravar_linha_log(modelo, '[JSON_RETORNO]')
        Genericos.gravar_linha_log(modelo, json.dumps(retorno, ensure_ascii=False))
        Genericos.gravar_linha_log(modelo, '[EMISSAO_SINCRONA_FIM]')

        return retorno

    # Métodos específicos de NFe
    @staticmethod
    def emitir_nfe_sincrono(conteudo, tp_conteudo, cnpj, tp_down, tp_amb, caminho, exibe_na_tela):
        modelo = '55'
        status_envio = ''
        status_consulta = ''
        status_download = ''
        motivo = ''
        ns_nrec = ''
        ch_nfe = ''
        c_stat = ''
        n_prot = ''
        erros = ''

        Genericos.gravar_linha_log(modelo, '[EMISSAO_SINCRONA_INICIO]')
        resposta = NSSuite.emitir_documento(modelo, conteudo, tp_conteudo)
        status_envio = resposta['status']

        if status_envio == 200 or status_envio == -6:
            ns_nrec = resposta['nsNRec']
            time.sleep(Parametros.TEMPO_ESPERA)

            cons_status_processamento = ConsStatusProcessamentoReqNFe(cnpj, ns_nrec, tp_amb)
            resposta = NSSuite.consultar_status_processamento(modelo, cons_status_processamento)
            status_consulta = resposta['status']

            if status_consulta == 200:
                c_stat = resposta['cStat']

                if c_stat == 100 or c_stat == 150:
                    ch_nfe = resposta['chNFe']
                    n_prot = resposta['nProt']
                    motivo = resposta['xMotivo']

                    download_req_nfe = DownloadReqNFe(ch_nfe, None, tp_down, tp_amb)
                    resposta = NSSuite.dowload_documento_e_salvar(modelo, download_req_nfe, caminho, ch_nfe + '-NFe',
                                                                  exibe_na_tela)
                    status_download = resposta['status']

                    if not status_download == 200:
                        motivo = resposta['motivo']
                else:
                    motivo = resposta['motivo']
            elif status_consulta == -2:
                c_stat = resposta['cStat']
                motivo = resposta['erro']['motivo']
            else:
                motivo = resposta['motivo']
        elif status_envio == -7:
            motivo = resposta['motivo']
            ns_nrec = resposta['nsNRec']
        elif status_envio == -4 or status_envio == -2:
            motivo = resposta['motivo']
            erros = resposta['erros']
        elif status_envio == -999 or status_envio == -5:
            motivo = resposta['erro']['xMotivo']
        else:
            try:
                motivo = resposta['motivo']
            except '':
                motivo = resposta

        emitir_sincrono_nfe = EmitirSincronoRetNFe(ch_nfe, status_envio, status_consulta, status_download,
                                                   c_stat, n_prot, motivo, ns_nrec, erros)
        retorno = emitir_sincrono_nfe.__dict__
        Genericos.gravar_linha_log(modelo, '[JSON_RETORNO]')
        Genericos.gravar_linha_log(modelo, json.dumps(retorno, ensure_ascii=False))
        Genericos.gravar_linha_log(modelo, '[EMISSAO_SINCRONA_FIM]')

        return retorno

    # Métodos genéricos, compartilhados entre diversas funções
    @staticmethod
    def emitir_documento(modelo, conteudo, tp_conteudo):
        global url_envio
        if modelo == '63':
            url_envio = Endpoints.BPeEnvio
        elif modelo == '57':
            url_envio = Endpoints.CTeEnvio
        elif modelo == '67':
            url_envio = Endpoints.CTeOSEnvio
        elif modelo == '58':
            url_envio = Endpoints.MDFeEnvio
        elif modelo == '65':
            url_envio = Endpoints.NFCeEnvio
        elif modelo == '55':
            url_envio = Endpoints.NFeEnvio
        else:
            raise Exception('Não definido endpoint para o modelo ' + modelo)

        Genericos.gravar_linha_log(modelo, '[ENVIO_DADOS]')
        Genericos.gravar_linha_log(modelo, conteudo)

        resposta = NSSuite.__envia_conteudo_para_api(conteudo, url_envio, tp_conteudo)

        Genericos.gravar_linha_log(modelo, '[ENVIO_RESPOSTA]')
        Genericos.gravar_linha_log(modelo, json.dumps(resposta, ensure_ascii=False))
        return resposta

    @staticmethod
    def consultar_status_processamento(modelo, cons_status_processamento_req):
        global urlConsulta
        if modelo == '63':
            urlConsulta = Endpoints.BPeConsStatusProcessamento
        elif modelo == '67' or modelo == '57':
            urlConsulta = Endpoints.CTeConsStatusProcessamento
        elif modelo == '58':
            urlConsulta = Endpoints.MDFeConsStatusProcessamento
        elif modelo == '55':
            urlConsulta = Endpoints.NFeConsStatusProcessamento
        else:
            raise Exception('Não definido endpoint para o modelo ' + modelo)

        data = cons_status_processamento_req.__dict__
        Genericos.gravar_linha_log(modelo, '[CONSULTA_DADOS]')
        Genericos.gravar_linha_log(modelo, json.dumps(data, ensure_ascii=False))

        resposta = NSSuite.__envia_conteudo_para_api(json.dumps(data), urlConsulta, 'json')

        Genericos.gravar_linha_log(modelo, '[CONSULTA_RESPOSTA]')
        Genericos.gravar_linha_log(modelo, json.dumps(resposta, ensure_ascii=False))

        return resposta

    @staticmethod
    def dowload_documento(modelo, dowload_req):
        global url_download
        if modelo == '63':
            url_download = Endpoints.BPeDownload
        elif modelo == '57' or modelo == '67':
            url_download = Endpoints.CTeDownload
        elif modelo == '58':
            url_download = Endpoints.MDFeDownload
        elif modelo == '65':
            url_download = Endpoints.NFCeDownload
        elif modelo == '55':
            url_download = Endpoints.NFeDownload
        else:
            raise Exception('Não definido endpoint para o modelo ' + modelo)
        data = dowload_req.__dict__
        Genericos.gravar_linha_log(modelo, '[DOWNLOAD_DADOS]')
        Genericos.gravar_linha_log(modelo, json.dumps(data, ensure_ascii=False))

        resposta = NSSuite.__envia_conteudo_para_api(json.dumps(data), url_download, 'json')

        status = resposta['status']

        if not status == 200 and status == 100:
            Genericos.gravar_linha_log(modelo, '[DOWNLOAD_RESPOSTA]')
            Genericos.gravar_linha_log(modelo, json.dumps(resposta, ensure_ascii=False))
        else:
            Genericos.gravar_linha_log(modelo, '[DOWNLOAD_STATUS]')
            Genericos.gravar_linha_log(modelo, str(status))
        return resposta

    @staticmethod
    def dowload_documento_e_salvar(modelo, download_req, caminho, nome, exibe_na_tela):
        resposta = NSSuite.dowload_documento(modelo, download_req)
        status = resposta['status']

        if status == 200 or status == 100:
            try:
                if not caminho[len(caminho) - 1] is '\\':
                    caminho += '\\'
                if os.path.exists(caminho) is False:
                    os.mkdir(caminho)
                    mensagem = '[DIRETORIO PARA DOWNLOADS CRIADO COM SUCESSO]'
                else:
                    mensagem = '[DIRETORIO PARA DOWNLOADS JÁ CRIADO ANTERIORMENTE]'
                Genericos.gravar_linha_log(modelo, mensagem)

            except '':
                Genericos.gravar_linha_log(modelo,
                                           '[NAO FOI POSSIVEL CRIAR UM DIRETORIO PARA SALVAR OS DOWNLOADS]' + caminho)

            if not modelo == '65':
                if download_req.tpDown.upper().count('X') is 1:
                    xml = resposta['xml']
                    Genericos.salvar_xml(xml, caminho, nome)

                if download_req.tpDown.upper().count('P') is 1:
                    pdf = resposta['pdf']
                    Genericos.salvar_pdf(pdf, caminho, nome)
                    if exibe_na_tela:
                        webbrowser.open(caminho + nome + '.pdf')
            else:
                xml = resposta['nfeProc']['xml']
                Genericos.salvar_xml(xml, caminho, nome)

                pdf = resposta['pdf']
                Genericos.salvar_pdf(pdf, caminho, nome)

                if exibe_na_tela:
                    webbrowser.open(caminho + nome + '.pdf')
        else:
            print('Ocorreu um erro, veja o retorno da API para mais informaçõe')

        return resposta

    @staticmethod
    def download_evento(modelo, download_evento_req):
        global url_download_evento
        if modelo == '63':
            url_download_evento = Endpoints.BPeDownloadEvento
        elif modelo == '57' or modelo == '67':
            url_download_evento = Endpoints.CTeDownloadEvento
        elif modelo == '58':
            url_download_evento = Endpoints.MDFeDownloadEvento
        elif modelo == '65':
            url_download_evento = Endpoints.NFCeDownload
        elif modelo == '55':
            url_download_evento = Endpoints.NFeDownloadEvento
        else:
            raise Exception('Não definido endpoint para o modelo ' + modelo)

        data = download_evento_req.__dict__
        Genericos.gravar_linha_log(modelo, '[DOWNLOAD_EVENTO_DADOS')
        Genericos.gravar_linha_log(modelo, json.dumps(data, ensure_ascii=False))

        resposta = NSSuite.__envia_conteudo_para_api(json.dumps(data), url_download_evento, 'json')

        status = resposta['status']

        if not status == 200 and status == 100:
            Genericos.gravar_linha_log(modelo, '[DOWNLOAD_EVENTO_RESPOSTA]')
            Genericos.gravar_linha_log(modelo, json.dumps(resposta, ensure_ascii=False))
        else:
            Genericos.gravar_linha_log(modelo, '[DOWNLOAD_EVENTO_STATUS]')
            Genericos.gravar_linha_log(modelo, str(status))
        return resposta

    @staticmethod
    def download_evento_e_salvar(modelo, download_evento_req, caminho, chave, n_seq_evento, exibe_na_tela):
        tp_evento_salvar = ''
        resposta = NSSuite.download_evento(modelo, download_evento_req)
        status = resposta['status']

        if status == 200 or status == 100:
            try:
                if not caminho[len(caminho) - 1] is '\\':
                    caminho += '\\'
                if os.path.exists(caminho) is False:
                    os.mkdir(caminho)
                    mensagem = '[DIRETORIO PARA DOWNLOADS CRIADO COM SUCESSO]'
                else:
                    mensagem = '[DIRETORIO PARA DOWNLOADS JÁ CRIADO ANTERIORMENTE]'
                Genericos.gravar_linha_log(modelo, mensagem)

            except '':
                Genericos.gravar_linha_log(modelo,
                                           '[NAO FOI POSSIVEL CRIAR UM DIRETORIO PARA SALVAR OS DOWNLOADS]' + caminho)
            if not modelo == '65':
                if download_evento_req.tpEvento.upper() == 'CANC':
                    tp_evento_salvar = '110111'
                elif download_evento_req.tpEvento.upper() == 'ENC':
                    tp_evento_salvar = '110110'
                else:
                    tp_evento_salvar = '110115'

                if download_evento_req.tpDown.upper().count('X') is 1:
                    xml = resposta['xml']
                    Genericos.salvar_xml(xml, caminho, tp_evento_salvar + chave + n_seq_evento + '-procEven')
                if download_evento_req.tpDown.upper().count('P') is 1:
                    pdf = resposta['pdf']
                    if not pdf == '' or pdf is None:
                        Genericos.salvar_pdf(pdf, caminho, tp_evento_salvar + chave + n_seq_evento + '-procEven')
                    if exibe_na_tela:
                        webbrowser.open(caminho + tp_evento_salvar + chave + n_seq_evento + '-procEven.pdf')
            else:
                xml = resposta['nfeProc']['xml']
                Genericos.salvar_xml(xml, caminho, tp_evento_salvar + chave + n_seq_evento + "-procEven")

                pdf = resposta['pdfCancelamento']
                Genericos.salvar_pdf(pdf, caminho, tp_evento_salvar + chave + n_seq_evento + "-procEven")

                if exibe_na_tela:
                    webbrowser.open(caminho + tp_evento_salvar + chave + n_seq_evento + "-procEven.´df")
        else:
            print('Ocorreu um erro, veja o retorno da API para mais informaçõe')

        return resposta

    @staticmethod
    def cancelar_documento(modelo, cancelar_req):
        global url_cancelamento
        if modelo == '63':
            url_cancelamento = Endpoints.BPeCancelamento
        elif modelo == '57' or modelo == '67':
            url_cancelamento = Endpoints.CTeCancelamento
        elif modelo == '58':
            url_cancelamento = Endpoints.MDFeCancelamento
        elif modelo == '65':
            url_cancelamento = Endpoints.NFCeCancelamento
        elif modelo == '55':
            url_cancelamento = Endpoints.NFeCancelamento
        else:
            raise Exception('Não definido endpoint para o modelo ' + modelo)

        data = cancelar_req.__dict__
        Genericos.gravar_linha_log(modelo, '[CANCELAMENTO_DADOS')
        Genericos.gravar_linha_log(modelo, json.dumps(data, ensure_ascii=False))

        resposta = NSSuite.__envia_conteudo_para_api(json.dumps(data), url_cancelamento, 'json')

        Genericos.gravar_linha_log(modelo, '[CANCELAMENTO_RESPOSTA')
        Genericos.gravar_linha_log(modelo, json.dumps(resposta, ensure_ascii=False))

        return resposta

    @staticmethod
    def cancelar_documento_e_salvar(modelo, cancelar_req, download_evento_req, caminho, chave, exibe_na_tela):
        resposta = NSSuite.cancelar_documento(modelo, cancelar_req)
        status = resposta['status']
        if status == 200 or status == 135:
            c_stat = resposta['cStat']
            if c_stat == 135:
                resposta_download = NSSuite.download_evento_e_salvar(modelo, download_evento_req, caminho, chave, '1',
                                                                     exibe_na_tela)
        else:
            print('Ocorreu um erro ao cancelar, veja o retorno da API para mais informações')
        return resposta

    @staticmethod
    def corrigir_documento(modelo, corrigir_req):
        global url_cce
        if modelo == '67' or modelo == '57':
            url_cce = Endpoints.CTeCCe
        elif modelo == '55':
            url_cce = Endpoints.NFeCCe
        else:
            raise Exception('Não definido endpoint para o modelo ' + modelo)
        data = corrigir_req.__dict__
        Genericos.gravar_linha_log(modelo, '[CCE_DADOS')
        Genericos.gravar_linha_log(modelo, json.dumps(data, ensure_ascii=False))

        resposta = NSSuite.__envia_conteudo_para_api(json.dumps(data), url_cce, 'json')

        Genericos.gravar_linha_log(modelo, '[CCE_RESPOSTA')
        Genericos.gravar_linha_log(modelo, json.dumps(resposta, ensure_ascii=False))

        return resposta

    @staticmethod
    def corrigir_documento_e_salvar(modelo, corrigir_req, download_evento_req, caminho, chave, n_seq_evento,  exibe_na_tela):
        resposta = NSSuite.corrigir_documento(modelo, corrigir_req)
        status = resposta['status']
        if status == 200:
            resposta_download = NSSuite.download_evento_e_salvar(modelo, download_evento_req, caminho, chave,
                                                                 n_seq_evento, exibe_na_tela)
        else:
            print('Ocorreu um erro ao corrigir, veja o retorno da API para mais informações')
        return resposta

    @staticmethod
    def inutilizar_numeracao(modelo, inutilizar_req):
        global url_inut
        if modelo == '57' or modelo == '67':
            url_inut = Endpoints.CTeInutilizacao
        elif modelo == '65':
            url_inut = Endpoints.NFCeInutilizacao
        elif modelo == '55':
            url_inut = Endpoints.NFeInutilizacao
        else:
            raise Exception('Não definido endpoint para o modelo ' + modelo)
        data = inutilizar_req.__dict__
        Genericos.gravar_linha_log(modelo, '[INUTILIZACAO_DADOS')
        Genericos.gravar_linha_log(modelo, json.dumps(data, ensure_ascii=False))

        resposta = NSSuite.__envia_conteudo_para_api(json.dumps(data), url_inut, 'json')

        Genericos.gravar_linha_log(modelo, '[INUTILIZACAO_RESPOSTA')
        Genericos.gravar_linha_log(modelo, json.dumps(resposta, ensure_ascii=False))

        return resposta

    @staticmethod
    def inutilizar_numeracao_e_salvar(modelo, inutilizar_req, caminho):
        resposta = NSSuite.inutilizar_numeracao(modelo, inutilizar_req)
        status = resposta['status']
        xml = None
        chave = None

        if status == 102 or status == 200:
            c_stat = resposta['c_stat']
            if c_stat == 102:
                if modelo == '67' or modelo == '57':
                    xml = resposta['retornoInutCTe']['xmlInut']
                    chave = resposta['retornoInutCTe']['chave']
                elif modelo == '65':
                    xml = resposta['retInutNFe']['xml']
                    chave = resposta['retInutNFe']['chave']
                elif modelo == '55':
                    xml = resposta['retornoInutNFe']['xmlInut']
                    chave = resposta['retornoInutNFe']['chave']
                else:
                    raise Exception('Nao existe inutilização para este modelo ' + modelo)
        else:
            print('Ocorreu um erro ao corrigir, veja o retorno da API para mais informações')

        if not xml is None:
            if not caminho[len(caminho) - 1] is '\\':
                caminho += '\\'
            if os.path.exists(caminho) is False:
                os.mkdir(caminho)
            Genericos.salvar_xml(xml, caminho, chave + '-Inut')

        return resposta

    @staticmethod
    def consulta_cadastro_contribuinte(modelo, cons_cad_req):
        global url_cons_cad
        if modelo == '57' or modelo == '67':
            url_cons_cad = Endpoints.CTeConsCad
        elif modelo == '55':
            url_cons_cad = Endpoints.NFeConsCad
        else:
            raise Exception('Não definido endpoint de consulta de cadastro para o modelo ' + modelo)

        data = cons_cad_req.__dict__
        Genericos.gravar_linha_log(modelo, '[CONS_CAD_DADOS')
        Genericos.gravar_linha_log(modelo, json.dumps(data, ensure_ascii=False))

        resposta = NSSuite.__envia_conteudo_para_api(json.dumps(data), url_cons_cad, 'json')

        Genericos.gravar_linha_log(modelo, '[CONS_CAD_RESPOSTA')
        Genericos.gravar_linha_log(modelo, json.dumps(resposta, ensure_ascii=False))

        return resposta

    @staticmethod
    def consultar_situacao_documento(modelo, cons_sit_req):
        global url_cons_sit
        if modelo == '63':
            url_cons_sit = Endpoints.BPeConsSit
        elif modelo == '67' or modelo == '57':
            url_cons_sit = Endpoints.CTeConsSit
        elif modelo == '58':
            url_cons_sit = Endpoints.MDFeConsSit
        elif modelo == '65':
            url_cons_sit = Endpoints.NFCeConsSit
        elif modelo == '55':
            url_cons_sit = Endpoints.NFeConsSit
        else:
            raise Exception("Não definido endpoint de consulta de situação para o modelo " + modelo)

        data = cons_sit_req.__dict__
        Genericos.gravar_linha_log(modelo, '[CONS_SIT_DADOS')
        Genericos.gravar_linha_log(modelo, json.dumps(data, ensure_ascii=False))

        resposta = NSSuite.__envia_conteudo_para_api(json.dumps(data), url_cons_sit, 'json')

        Genericos.gravar_linha_log(modelo, '[CONS_SIT_RESPOSTA')
        Genericos.gravar_linha_log(modelo, json.dumps(resposta, ensure_ascii=False))

        return resposta

    @staticmethod
    def listarNSNRecs(modelo, listar_nsnrecs):
        global url_listar_nsnrecs
        if modelo == '57' or modelo == '67':
            url_listar_nsnrecs = Endpoints.CTeListarNSNRecs
        elif modelo == '58':
            url_listar_nsnrecs = Endpoints.MDFeListarNSNRecs
        elif modelo == '55':
            url_listar_nsnrecs = Endpoints.NFeListarNSNRecs
        else:
            raise Exception("Não definido endpoint de listagem de nsNRec para o modelo " + modelo)

        data = listar_nsnrecs.__dict__
        Genericos.gravar_linha_log(modelo, '[LISTAR_NSNRECS_DADOS')
        Genericos.gravar_linha_log(modelo, json.dumps(data, ensure_ascii=False))

        resposta = NSSuite.__envia_conteudo_para_api(json.dumps(data), url_listar_nsnrecs, 'json')

        Genericos.gravar_linha_log(modelo, '[LISTAR_NSNRECS_RESPOSTA')
        Genericos.gravar_linha_log(modelo, json.dumps(resposta, ensure_ascii=False))

        return resposta

    @staticmethod
    def enviar_email_documento(modelo, envia_email_req):
        global url_envia_email
        if modelo == '57' or modelo == '67':
            url_envia_email = Endpoints.CTeListarNSNRecs
        elif modelo == '58':
            url_envia_email = Endpoints.MDFeListarNSNRecs
        elif modelo == '55':
            url_envia_email = Endpoints.NFeListarNSNRecs
        else:
            raise Exception("Não definido endpoint de envio de e-mail para o modelo " + modelo)

        data = envia_email_req.__dict__
        Genericos.gravar_linha_log(modelo, '[ENVIAR_EMAIL_DADOS')
        Genericos.gravar_linha_log(modelo, json.dumps(data, ensure_ascii=False))

        resposta = NSSuite.__envia_conteudo_para_api(json.dumps(data), url_envia_email, 'json')

        Genericos.gravar_linha_log(modelo, '[ENVIAR_EMAIL_RESPOSTA')
        Genericos.gravar_linha_log(modelo, json.dumps(resposta, ensure_ascii=False))

        return resposta
