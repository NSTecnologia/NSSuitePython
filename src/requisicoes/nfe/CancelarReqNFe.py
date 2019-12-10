from src.requisicoes._genericos.CancelarReq import CancelarReq


class CancelarReqNFe(CancelarReq):
    def __init__(self, ch_nfe, tp_amb, dh_evento, n_prot, x_just):
        super().__init__(tp_amb, dh_evento, n_prot, x_just)
        self.chNFe = ch_nfe