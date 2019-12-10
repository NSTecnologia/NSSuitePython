from src.requisicoes._genericos.ConsStatusProcessamentoReq import ConsStatusProcessamentoReq


class ConsStatusProcessamentoReqNFe(ConsStatusProcessamentoReq):
    def __init__(self, cnpj, ns_nrec, tp_amb):
        super().__init__(cnpj, ns_nrec, tp_amb)