from src.requisicoes._genericos.CancelarReq import CancelarReq

class CancelarReqBPe(CancelarReq):
    def __init__(self, ch_bpe, tp_amb, dh_evento, n_prot, x_just):
        super().__init__(tp_amb, dh_evento, n_prot, x_just)
        self.chBPe = ch_bpe