from src.requisicoes._genericos.DownloadReq import DownloadReq


class DownloadReqMDFe(DownloadReq):
    def __init__(self, ch_mdfe, tp_down, tp_amb):
        super().__init__(tp_down, tp_amb)
        self.chMDFe = ch_mdfe
