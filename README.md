# NSSuitePYTHON

Utilizando a NS API, este exemplo - criado em Python - possui funcionalidades para consumir documentos fiscais eletrônicos em geral, como por exemplo: 
+ NFe; 
+ CTe; 
+ NFCe;
+ MDFe;
+ BPe;

Simplificando todos os projetos utilizados em um único exemplo, deixando mais pratica e facil a integração com a NS API.

## Primeiros passos:

### Integrando ao sistema:

Para utilizar as funções de comunicação com a API, você precisa realizar os seguintes passos:

1. Extraia o conteúdo da pasta compactada que você baixou;
2. Copie para sua aplicação a pasta src, na qual contem todos as classes que serão utilizadas;
3. Abra o seu projeto e importe a pasta copiada.

**Pronto!** Agora, você já pode consumir a NS Suite API através do seu sistema. Todas as funcionalidades de comunicação foram implementadas na classe NSSuite.py.

------

## Emissão Sincrona:

### Realizando uma Emissão Sincrona:

Para realizar uma emissão completa de uma NFe (utilizada para exemplo), você poderá utilizar a função emitirNFeSincrono da classe NSSuite. Veja abaixo sobre os parâmetros necessários, e um exemplo de chamada do método.

##### Parâmetros:

**ATENÇÃO:** o **token** também é um parâmetro necessário e você deve, primeiramente, defini-lo na classe **NSSuite.py**.

Parametros     | Descrição
:-------------:|:-----------
conteudo       | Conteúdo de emissão do documento.
tpConteudo     | Tipo de conteúdo que está sendo enviado. Valores possíveis: json, xml, txt
CNPJ           | CNPJ do emitente do documento.
tpDown         | Tipo de arquivos a serem baixados.Valores possíveis: <ul> <li>**X** - XML</li> <li>**J** - JSON</li> <li>**P** - PDF</li> <li>**XP** - XML e PDF</li> <li>**JP** - JSON e PDF</li> </ul> 
tpAmb          | Ambiente onde foi autorizado o documento.Valores possíveis:<ul> <li>1 - produção</li> <li>2 - homologação</li> </ul>
caminho        | Caminho onde devem ser salvos os documentos baixados.
exibeNaTela    | Se for baixado, exibir o PDF na tela após a autorização.Valores possíveis: <ul> <li>**True** - será exibido</li> <li>**False** - não será exibido</li> </ul> 

##### Exemplo de chamada:

Após ter todos os parâmetros listados acima, você deverá fazer a chamada da função. Veja o código de exemplo abaixo:
           
    retorno = NSSuite.emitir_nfe_sincrono(conteudo, tp_conteudo, cnpj_emit, tp_down, tp_amb, caminho, exibe_na_tela)
    print str(retorno)

A função emitir_nfe_sincrono fará o envio, a consulta e download do documento, utilizando as funções emitir_documento, consultar_status_processamento e download_documento_e_salvar, presentes na classe NSSuite.py. Por isso, o retorno será um JSON com os principais campos retornados pelos métodos citados anteriormente. No exemplo abaixo, veja como tratar o retorno da função emitir_nfe_sincrono:

##### Exemplo de tratamento de retorno:

O JSON retornado pelo método terá os seguintes campos: statusEnvio, statusConsulta, statusDownload, cStat, chNFe, nProt, motivo, nsNRec, erros. Veja o exemplo abaixo:

    {
        "statusEnvio": "200",
        "statusConsulta": "200",
        "statusDownload": "200",
        "cStat": "100",
        "chNFe": "43181007364617000135550000000119741004621864",
        "nProt": "143180007036833",
        "motivo": "Autorizado o uso da NF-e",
        "nsNRec": "313022",
        "erros": ""
    }
      
Confira um código para tratamento do retorno, no qual pegará as informações dispostas no JSON de Retorno disponibilizado:


resposta = NSSuite.emitir_nfe_sincrono(conteudo, tp_conteudo, cnpj_emit, tp_down, tp_amb, caminho, exibe_na_tela)
 
    status_envio = resposta['statusEnvio']
    status_consulta = resposta['statusConsulta']
    status_download = resposta['statusDownload']
    c_stat = str(resposta['cStat'])
    ch_nfe = resposta['chNFe']
    n_prot = resposta['nProt']
    motivo = resposta['motivo']
    ns_nrec = resposta['nsNRec']
    erros = resposta['erros']

    if status_envio == 200 or status_envio == -6:
        if status_consulta == 200:
            if c_stat == '100':
                print(motivo)
                if not status_download == 200:
                    print('Erro Download')
            else:
                print(motivo)
        else:
            print(motivo + '\n' + erros)
    else:
        print(motivo + '\n' + erros) 

-----

## Cancelamento de Documento:

### Realizando um Cancelamento:

tilizando NFe como exemplo para o cancelamento deve-se ter em mente que você deverá usar a função cancelarDocumentoESalvar da classe NSSuite. Veja abaixo sobre os parâmetros necessários, e um exemplo de chamada do método.

##### Parâmetros:

**ATENÇÃO:** o **token** também é um parâmetro necessário e você deve, primeiramente, defini-lo na classe **NSSuite.py**.

Parametros     | Descrição
:-------------:|:-----------
**modelo**            | Conteúdo de emissão do documento.<ul> <li>"63" (BPe);</li> <li>"57" (CTe);</li> <li>"67" (CTeOS);</li> <li>"58" (MDFe);</li> <li>"65" (NFCe);</li> <li>"55" (NFe);</li> </ul>
**CancelarReq**       | JSON contendo as informações de uma requisição de cancelamento de documento
**DownloadEventoReq** | JSON contendo as informações de uma requisição de Download de Evento
**caminho**           | Caminho onde devem ser salvos os documentos baixados.
**chave**             | Ambiente onde foi autorizado o documento.Valores possíveis:<ul> <li>1 - produção</li> <li>2 - homologação</li> </ul> 
**exibeNaTela**       | Se for baixado, exibir o PDF na tela após a autorização.Valores possíveis: <ul> <li>**True** - será exibido</li> <li>**False** - não será exibido</li> </ul> 

##### Exemplo de chamada:

Após ter todos os parâmetros listados acima, você deverá fazer a chamada da função. Veja o código de exemplo abaixo:

    cancelar_nfe = CancelarReqNFe(
                            ch_nfe='43190307364617000135550000000130621004621863',
                            tp_amb='2',
                            dh_evento='2019-03-15T15:37:14-03:00',
                            n_prot='143190000501923',
                            x_just='TESTE DE CANCELAMENTO INTEGRAÇÃO NS'
    )

    down = new DownloadEventoReqNFe(
                            ch_nfe='43190307364617000135550000000130621004621863',
                            tp_amb='2',
                            tp_down='XP',
                            tp_evento='CANC',
                            n_seq_evento='1'
    )

    retorno = NSSuite.cancelar_documento_e_salvar('55', cancelarReqNFe, down, './Notas', '43190307364617000135550000000130621004621863', True)
    
A função **cancelar_documento_e_salvar** fará o cancelamento de qualquer documento que possa ser cancelado e fazendo o download do evento feito, neste caso hipotético, uma NFe, utilizando as funções cancelar_documento e download_evento_e_salvar, presentes na classe NSSuite.py. Dessa forma, o retorno será um JSON com os principais campos retornados pelos métodos citados anteriormente. No exemplo abaixo, veja o retorno da nossa API em um cancelamento::

##### Exemplo de retorno de cancelamento:

    {
      "status": 135,
      "motivo": "NF-e cancelada com sucesso",
      "retEvento": {
        "cStat": 135,
        "xMotivo": "Evento registrado e vinculado a NF-e",
        "chNFe": "43190307364617000135550000000130621004621863",
        "dhRegEvento": "2019-03-15T15:37:14-03:00",
        "nProt": "143190000501923"
      }
    }

-----

## Carta de Correção(CC):

### Realizando uma Correção de Documento:

Utilizando NFe como exemplo para a criação de uma carta de correção, deve-se ter em mente que você deverá usar a função corrigirDocumentoESalvar da classe NSSuite. Veja abaixo sobre os parâmetros necessários, e um exemplo de chamada do método.

##### Parâmetros:

**ATENÇÃO:** o **token** também é um parâmetro necessário e você deve, primeiramente, defini-lo na classe **NSSuite.py**.

Parametros     | Descrição
:-------------:|:-----------
**modelo**            | Conteúdo de emissão do documento.<ul> <li>"63" (BPe);</li> <li>"57" (CTe);</li> <li>"67" (CTeOS);</li> <li>"58" (MDFe);</li> <li>"65" (NFCe);</li> <li>"55" (NFe);</li> </ul>
**CorrigirReq**       | JSON contendo as informações de uma requisição de carta de correção
**DownloadEventoReq** | JSON contendo as informações de uma requisição de Download de Evento
**caminho**           | Caminho onde devem ser salvos os documentos baixados.
**chave**             | Ambiente onde foi autorizado o documento.Valores possíveis:<ul> <li>1 - produção</li> <li>2 - homologação</li> </ul> 
**nSeqEvento**        | Número sequencial do evento
**exibeNaTela**       | Se for baixado, exibir o PDF na tela após a autorização.Valores possíveis: <ul> <li>**True** - será exibido</li> <li>**False** - não será exibido</li> </ul> 

##### Exemplo de chamada:

Após ter todos os parâmetros listados acima, você deverá fazer a chamada da função. Veja o código de exemplo abaixo:

    cce_teste = CorrigirReqNFe(
                            ch_nfe='43190207364617000135550000000129281004621862',
                            x_correcao='CC-e realizada para teste de integração',
                            tp_amb='2',
                            dh_evento='2019-03-06T12:00:00-03:00',
                            n_seq_evento='1'
    )

    down_teste = DownloadEventoReqNFe(
                            ch_nfe='143190207364617000135550000000129281004621862',
                            tp_amb='2',
                            tp_down='XP',
                            tp_evento='CCE',
                            n_seq_evento='1'
    )

    retorno = NSSuite.corrigir_documento_e_salvar('55', cce_teste, down_teste, './Notas', '43190207364617000135550000000129281004621862', '1', True)
    
A função **corrigir_documento_e_salvar** irá vincular um CCe (carta de correção) ao projeto selecionado, neste caso hipotético, à uma NFe, utilizando as funções corrigir_documento e download_evento_e_salvar, presentes na classe NSSuite.py. Dessa forma, o retorno será um JSON com os principais campos retornados pelos métodos citados anteriormente. No exemplo abaixo, veja o retorno da nossa API em uma CCe:

##### Exempo de retorno de correção de documento:

    {
      "status": 200,
      "motivo": "CC-e vinculada com sucesso",
      "retEvento": {
        "cStat": 135,
        "xMotivo": "Evento registrado e vinculado a NF-e",
        "chNFe": "43190207364617000135550000000129281004621862",
        "dhRegEvento": "2019-03-06T12:00:50-03:00",
        "nProt": "143190000330112"
      }
    }

![Ns](https://nstecnologia.com.br/blog/wp-content/uploads/2018/11/ns%C2%B4tecnologia.png) | Obrigado pela atenção!
