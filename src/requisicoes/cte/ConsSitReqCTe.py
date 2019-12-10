from src.requisicoes._genericos.ConsSitReq import ConsSitReq


class ConsSitReqCTe(ConsSitReq):
    def __init__(self, ch_cte, licenca_cnpj, tp_amb):
        super().__init__(licenca_cnpj, tp_amb)
        self.chCTe = ch_cte
