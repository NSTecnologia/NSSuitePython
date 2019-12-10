from src.requisicoes._genericos.DownloadEventoReq import DownloadEventoReq


class DownloadEventoReqBPe(DownloadEventoReq):
    def __init__(self, ch_bpe, tp_amb, tp_down, tp_evento, n_seq_evento):
        super().__init__(tp_amb, tp_down, tp_evento, n_seq_evento)
        self.chBPe = ch_bpe
