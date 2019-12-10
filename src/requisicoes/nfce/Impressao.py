class Impressao:
    def __init__(self, tipo='PDF', ecologica=False, item_linhas='1', item_desconto=True, largura_papel='80mm', mod_mini_impressora=None):
        self.tipo = tipo
        self.ecologica = ecologica
        self.itemLinhas = item_linhas
        self.itemDesconto = item_desconto
        self.larguraPapel = largura_papel
        self.modMiniImpressora= mod_mini_impressora