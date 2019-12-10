from src.requisicoes._genericos.InutilizarReq import InutilizarReq


class InutilizarReqCTe(InutilizarReq):
    def __init__(self, mod, n_ct_ini, n_ct_fin, c_uf, ano, tp_amb, cnpj, serie, x_just):
        super().__init__(c_uf, ano, tp_amb, cnpj, serie, x_just)
        self.mod = mod
        self.nCTIni = n_ct_ini
        self.nCTFin = n_ct_fin