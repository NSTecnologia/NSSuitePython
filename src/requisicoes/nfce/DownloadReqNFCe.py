from src.requisicoes._genericos.DownloadReq import DownloadReq

class DownloadReqNFCe(DownloadReq):
    def __init__(self, ch_nfe, impressao, tp_down, tp_amb):
        super().__init__(tp_down, tp_amb)
        self.chNFe = ch_nfe
        self.impressao = impressao