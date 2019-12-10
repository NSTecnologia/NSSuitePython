from src.requisicoes._genericos.CorrigirReq import CorrigirReq


class CorrigirReqNFe(CorrigirReq):
    def __init__(self, ch_nfe, x_correcao, tp_amb, dh_evento, n_seq_evento):
        super().__init__(tp_amb, dh_evento, n_seq_evento)
        self.chNFe = ch_nfe
        self.xCorrecao = x_correcao



