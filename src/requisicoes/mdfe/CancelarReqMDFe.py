from src.requisicoes._genericos.CancelarReq import CancelarReq


class CancelarReqMDFe(CancelarReq):
    def __init__(self, ch_mdfe, tp_amb, dh_evento, n_prot, x_just):
        super().__init__(tp_amb, dh_evento, n_prot, x_just)
        self.chMDFe = ch_mdfe