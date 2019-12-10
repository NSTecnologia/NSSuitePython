from src.requisicoes._genericos.ConsNaoEncerradosReq import ConsNaoEncerradosReq


class ConsNaoEncerradosReqMDFe(ConsNaoEncerradosReq):
    def __init__(self, tp_amb, c_uf, cnpj):
        super().__init__(tp_amb, c_uf, cnpj)