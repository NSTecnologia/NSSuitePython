from src.requisicoes._genericos.DownloadEventoReq import DownloadEventoReq


class DownloadEventoReqNFe(DownloadEventoReq):
    def __init__(self, ch_nfe, tp_amb, tp_down, tp_evento, n_seq_evento):
        super().__init__(tp_amb, tp_down, tp_evento, n_seq_evento)
        self.chNFe = ch_nfe