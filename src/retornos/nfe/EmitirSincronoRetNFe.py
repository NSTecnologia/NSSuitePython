from src.retornos._genericos.EmitirSincronoRet import EmitirSincronoRet


class EmitirSincronoRetNFe(EmitirSincronoRet):
    def __init__(self, ch_nfe, status_envio, status_consulta, status_download, c_stat, n_prot, motivo, ns_nrec, erros):
        super().__init__(status_envio, status_consulta, status_download, c_stat, n_prot, motivo, ns_nrec, erros)
        self.chNFe = ch_nfe