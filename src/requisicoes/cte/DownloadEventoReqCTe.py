from src.requisicoes._genericos.DownloadEventoReq import DownloadEventoReq


class DownloadEventoReqCTe(DownloadEventoReq):
    def __init__(self, ch_cte, tp_amb, tp_down, tp_evento, n_seq_evento):
        super().__init__(tp_amb, tp_down, tp_evento, n_seq_evento)
        self.chCTe = ch_cte
