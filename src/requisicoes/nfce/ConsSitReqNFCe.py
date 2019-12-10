from src.requisicoes._genericos.ConsSitReq import ConsSitReq


class ConsSitReqNFCe(ConsSitReq):
    def __init__(self, ch_nfe, licenca_cnpj, tp_amb):
        super().__init__(licenca_cnpj, tp_amb)
        self.chNFe = ch_nfe