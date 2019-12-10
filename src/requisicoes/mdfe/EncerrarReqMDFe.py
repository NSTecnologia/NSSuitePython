from src.requisicoes._genericos.EncerrarReq import EncerrarReq


class EncerrarReqMDFe(EncerrarReq):
    def __init__(self, ch_mdfe, n_prot, tp_amb, dh_evento, dt_enc, c_uf, c_mun):
        super().__init__(n_prot, tp_amb, dh_evento, dt_enc, c_uf, c_mun)
        self.chMDFe = ch_mdfe