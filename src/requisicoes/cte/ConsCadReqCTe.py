from src.requisicoes._genericos.ConsCadReq import ConsCadReq


class ConsCadReqCTe(ConsCadReq):
    def __init__(self, cnpj_cont, uf, ie, cnpj, cpf):
        super().__init__(cnpj_cont, uf, ie, cnpj, cpf)