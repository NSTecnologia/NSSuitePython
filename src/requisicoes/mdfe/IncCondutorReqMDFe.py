from src.requisicoes._genericos.IncCondutorReq import IncCondutorReq


class IncCondutorReqMDFe(IncCondutorReq):
    def __init_s_(self, ch_mdfe, tp_amb, dh_evento, x_nome, cpf):
        super().__init__(tp_amb, dh_evento, x_nome, cpf)
        self.chMDFe = ch_mdfe
