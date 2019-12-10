from src.requisicoes._genericos.DownloadReq import DownloadReq


class DownloadReqCTe(DownloadReq):
    def __init__(self, ch_cte, cnpj, tp_down, tp_amb):
        super().__init__(tp_down, tp_amb)
        self.chCTe = ch_cte
        self.CNPJ = cnpj