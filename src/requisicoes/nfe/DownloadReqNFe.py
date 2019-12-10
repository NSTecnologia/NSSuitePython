from src.requisicoes._genericos.DownloadReq import DownloadReq


class DownloadReqNFe(DownloadReq):
    def __init__(self, ch_nfe, print_cean, tp_down, tp_amb):
        super().__init__(tp_down, tp_amb)
        self.chNFe = ch_nfe
        self.printCEAN = print_cean