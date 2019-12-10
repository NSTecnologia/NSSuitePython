from src.requisicoes._genericos.DownloadEventoReq import DownloadEventoReq


class DownloadEventoReqMDFe(DownloadEventoReq):
    def __init__(self, ch_mdfe, tp_amb, tp_down, tp_evento, n_seq_evento):
        super().__init__(tp_amb, tp_down, tp_evento, n_seq_evento)
        self.chMDFe = ch_mdfe