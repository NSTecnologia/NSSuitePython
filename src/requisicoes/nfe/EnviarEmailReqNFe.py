from src.requisicoes._genericos.EnviarEmailReq import EnviarEmailReq


class EnviarEmailReqNFe(EnviarEmailReq):
    def __init__(self, ch_nfe, envia_email_doc, email):
        super().__init__(envia_email_doc, email)
        self.chNFe = ch_nfe