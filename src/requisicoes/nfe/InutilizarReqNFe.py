from src.requisicoes._genericos.InutilizarReq import InutilizarReq


class InutilizarReqNFe(InutilizarReq):
    def __init__(self, n_nf_ini, n_nf_fin, c_uf, ano, tp_amb, cnpj, serie, x_just):
        super().__init__(c_uf, ano, tp_amb, cnpj, serie, x_just)
        self.nNFIni = n_nf_ini
        self.nNFFin = n_nf_fin