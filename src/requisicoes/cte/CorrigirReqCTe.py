class CorrigirReqCTe:
    def __init__(self, ch_cte, inf_correcao):
        self.chCTe = ch_cte
        self.infCorrecao = inf_correcao


class InfCorrecao:
    def __init__(self, grupo_alterado, campo_alterado, valor_alterado, nro_item_alterado):
        self.grupoAlterado = grupo_alterado
        self.campoAlterado = campo_alterado
        self.valorAlterado = valor_alterado
        self.nroItemAlterado = nro_item_alterado
