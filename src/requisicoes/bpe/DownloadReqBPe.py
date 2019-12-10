from src.requisicoes._genericos.DownloadReq import DownloadReq

class DownloadReqBPe(DownloadReq):
    def __init__(self, ch_bpe, tp_down, tp_amb):
        super().__init__(tp_down, tp_amb)
        self.chBPe = ch_bpe
