class InfGTVReqCTe:
    def __init__(self, ch_cte, tp_amb, dh_evento, n_seq_evento, inf_gtv):
        self.chCTe = ch_cte
        self.tpAmb = tp_amb
        self.dhEvento = dh_evento
        self.nSeqEvento = n_seq_evento
        self.infGTV = inf_gtv


class InfEspecie:
    def __init__(self, tp_especie, v_especie):
        self.tpEspecie = tp_especie
        self.vEspecie = v_especie


class InfGTV:
    def __init__(self, n_doc, id, serie, subserie, d_emi, n_dv, q_carga, placa, uf, rntrc, inf_especie, rem, dest):
        self.nDoc = n_doc
        self.id = id
        self.serie = serie
        self.subserie = subserie
        self.dEmi = d_emi
        self.nDV = n_dv
        self.qCarga = q_carga
        self.placa = placa
        self.UF = uf
        self.RNTRC = rntrc
        self.infEspecie = inf_especie
        self.rem = rem
        self.dest = dest


class Dest:
    def __init__(self, cnpj, cpf, ie, uf, x_nome):
        self.CNPJ = cnpj
        self.CPF = cpf
        self.IE = ie
        self.UF = uf
        self.xNome = x_nome


class Rem:
    def __init__(self, cnpj, cpf, ie, uf, x_nome):
        self.CNPJ = cnpj
        self.CPF = cpf
        self.IE = ie
        self.UF = uf
        self.xNome = x_nome