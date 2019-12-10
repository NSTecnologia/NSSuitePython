from src.requisicoes._genericos.ConsSitReq import ConsSitReq


class ConsSitReqNFe(ConsSitReq):
    def __init__(self, ch_nfe, versao, licenca_cnpj, tp_amb):
        super().__init__(licenca_cnpj, tp_amb)
        self.chNFe = ch_nfe
        self.versao = versao
