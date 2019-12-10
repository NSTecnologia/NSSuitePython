class EmitirSincronoRet:
    def __init__(self, status_envio, status_consulta, status_download, c_stat, n_prot, motivo, ns_nrec, erros):
        self.statusEnvio = status_envio
        self.statusConsulta = status_consulta
        self.statusDownload = status_download
        self.cStat = c_stat
        self.nProt = n_prot
        self.motivo = motivo
        self.nsNRec = ns_nrec
        self.erros = erros
