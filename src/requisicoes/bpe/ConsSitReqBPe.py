from src.requisicoes._genericos.ConsSitReq import ConsSitReq


class ConsSitReqBPe(ConsSitReq):
    def __init__(self, ch_bpe, licenca_cnpj, tp_amb):
        super().__init__(licenca_cnpj, tp_amb)
        self.chBPe = ch_bpe