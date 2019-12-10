# !/usr/bin/env python
# coding: utf-8

class Endpoints():
    
    #BP-e
    BPeEnvio = 'https://bpe.ns.eti.br/v1/bpe/issue'
    BPeConsStatusProcessamento = 'https://bpe.ns.eti.br/v1/bpe/issue/status'
    BPeDownload = 'https://bpe.ns.eti.br/v1/bpe/get'
    BPeDownloadEvento = 'https://bpe.ns.eti.br/v1/bpe/get/event'
    BPeCancelamento = 'https://bpe.ns.eti.br/v1/bpe/cancel'
    BPeNaoEmb = 'https://bpe.ns.eti.br/v1/bpe/naoemb'
    BPeConsSit = 'https://bpe.ns.eti.br/v1/bpe/status'

    #CT-e
    CTeEnvio = 'https://cte.ns.eti.br/cte/issue'
    CTeOSEnvio = 'https://cte.ns.eti.br/cte/issueos'
    CTeConsStatusProcessamento = 'https://cte.ns.eti.br/cte/issueStatus/300'
    CTeDownload = 'https://cte.ns.eti.br/cte/get/300'
    CTeDownloadEvento = 'https://cte.ns.eti.br/cte/get/event/300'
    CTeCancelamento = 'https://cte.ns.eti.br/cte/cancel/300'
    CTeCCe = 'https://cte.ns.eti.br/cte/cce/300'
    CTeConsCad = 'https://cte.ns.eti.br/util/conscad'
    CTeConsSit = 'https://cte.ns.eti.br/cte/stats/300'
    CTeInfGTV = 'https://cte.ns.eti.br/cte/gtv'
    CTeInutilizacao = 'https://cte.ns.eti.br/cte/inut'
    CTeListarNSNRecs = 'https://cte.ns.eti.br/util/list/nsnrecs'

    #DDF-e
    DDFeDesacordo = 'https://ddfe.ns.eti.br/events/cte/disagree'
    DDFeDownloadUnico = 'https://ddfe.ns.eti.br/dfe/unique'
    DDFeDownloadLote = 'https://ddfe.ns.eti.br/dfe/bunch'
    DDFeManifestacao = 'https://ddfe.ns.eti.br/events/manif'

    #MDF-e
    MDFeEnvio = 'https://mdfe.ns.eti.br/mdfe/issue'
    MDFeConsStatusProcessamento = 'https://mdfe.ns.eti.br/mdfe/issue/status'
    MDFeDownload = 'https://mdfe.ns.eti.br/mdfe/get'
    MDFeDownloadEvento = 'https://mdfe.ns.eti.br/mdfe/get/event'
    MDFeCancelamento = 'https://mdfe.ns.eti.br/mdfe/cancel'
    MDFeEncerramento = 'https://mdfe.ns.eti.br/mdfe/closure'
    MDFeIncCondutor = 'https://mdfe.ns.eti.br/mdfe/adddriver'
    MDFeConsNaoEncerrados = 'https://mdfe.ns.eti.br/util/consnotclosed'
    MDFeConsSit = 'https://mdfe.ns.eti.br/mdfe/stats'
    MDFePrevia = 'https://mdfe.ns.eti.br/util/preview/mdfe'
    MDFeListarNSNRecs = 'https://mdfe.ns.eti.br/util/list/nsnrecs'

    #NFC-e
    NFCeEnvio = 'https://nfce.ns.eti.br/v1/nfce/issue'
    NFCeDownload = 'https://nfce.ns.eti.br/v1/nfce/get'
    NFCeCancelamento = 'https://nfce.ns.eti.br/v1/nfce/cancel'
    NFCeConsSit = 'https://nfce.ns.eti.br/v1/nfce/status'
    NFCeEnvioEmail = 'https://nfce.ns.eti.br/v1/util/resendemail'
    NFCeInutilizacao = 'https://nfce.ns.eti.br/v1/nfce/inut'


    #NF-e
    NFeEnvio = 'https://nfe.ns.eti.br/nfe/issue'
    NFeConsStatusProcessamento = 'https://nfe.ns.eti.br/nfe/issue/status'
    NFeDownload = 'https://nfe.ns.eti.br/nfe/get'
    NFeDownloadEvento = 'https://nfe.ns.eti.br/nfe/get/event'
    NFeCancelamento = 'https://nfe.ns.eti.br/nfe/cancel'
    NFeCCe = 'https://nfe.ns.eti.br/nfe/cce'
    NFeConsStatusSefaz = 'https://nfe.ns.eti.br/util/wssefazstatus'
    NFeConsCad = 'https://nfe.ns.eti.br/util/conscad'
    NFeConsSit = 'https://nfe.ns.eti.br/nfe/stats'
    NFeEnvioEmail = 'https://nfe.ns.eti.br/util/resendemail'
    NFeInutilizacao = 'https://nfe.ns.eti.br/nfe/inut'
    NFeListarNSNRecs = 'https://nfe.ns.eti.br/util/list/nsnrecs'
    NFePrevia = 'https://nfe.ns.eti.br/util/preview/nfe'