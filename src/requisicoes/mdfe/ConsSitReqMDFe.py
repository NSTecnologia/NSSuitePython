from src.requisicoes._genericos.ConsSitReq import ConsSitReq


class ConsSitReqMDFe(ConsSitReq):
    def __init__(self, ch_mdfe, licenca_cnpj, tp_amb):
        super().__init__(licenca_cnpj, tp_amb)
        self.chMDFe = ch_mdfe