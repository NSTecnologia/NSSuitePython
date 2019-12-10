from src.retornos._genericos.EmitirSincronoRet import EmitirSincronoRet


class EmitirSincronoRetMDFe(EmitirSincronoRet):
    def __init__(self, ch_mdfe, status_envio, status_consulta, status_download, c_stat, n_prot, motivo, ns_nrec, erros):
        super().__init__(status_envio, status_consulta, status_download, c_stat, n_prot, motivo, ns_nrec, erros)
        self.chMDFe = ch_mdfe