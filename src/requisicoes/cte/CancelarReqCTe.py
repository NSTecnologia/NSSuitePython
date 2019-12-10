from src.requisicoes._genericos.CancelarReq import CancelarReq


class CancelarReqCTe(CancelarReq):
    def __init__(self, ch_cte, tp_amb, dh_evento, n_prot, x_just):
        super().__init__(tp_amb, dh_evento, n_prot, x_just)
        self.chCTe = ch_cte
