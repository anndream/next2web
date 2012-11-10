next2web
========

Web2py CMS to Small Bussiness Applications

##O que é o Next2Web?##

O Next2Web é um CMS em desenvolvimento sobre web2py, focado no desenvolvimento de aplicações para gestão de pequenos negócios, para isto ele segue os padrões formais da Gestão e Documentos, Fluxos de Trabalho e Regras de Negócio.

##A gestão e os documentos##

Quando falamos no conceito de "gestão empresarial", é impossível não remeter a ideia de documentos. 
A gestão de uma empresa, está estritamente ligada a documentos, sejam documentos internos, como uma circular, um pedido, uma ficha de registro de funcionário, ou a documentos externos, uma nota fiscal do fornecedor, um contrato com outra companhia, um imposto, uma taxa. 
São nestas bases que está fundamentado o projeto Next2Web.

##O que são os documentos no Next2Web?##

Nada mais são, que uma forma de armazenar os dados dos documentos que a empresa lida diariamente.
São no conceito mais nativo do web2py, tabelas, porém que possuem funcionalidades estendidas.

##Fluxos de Trabalho:##

Em uma organização, há também os Fluxos de Trabalho, que estão representados pela interação entre determinados departamentos, com base em um Documento, em exemplo, os departamentos do Almoxarifado e Financeiro, que se integram pelas Notas Fiscais de Fornecedor, sendo que:
Logo depois de receber um lote de produtos o Almoxarife deve conferir e dar as devidas entradas no estoque, e encaminhar a nota ao departamento financeiro. 
Já no departamento financeiro, esta nota inicia tarefas como a contabilidade e o agendamento de contas a pagar.

##Regras de Negócio:##

Quando falamos de Fluxos de Trabalho, é impossível descartar as regras que compõem estes fluxos, seguindo o exemplo anterior, surge a seguinte regra:
o Almoxarife deve conferir se as quantidades de cada produto, reportadas na nota coincidem com as quantidades de produtos recebidas, e caso haja alguma divergência o mesmo deve recusar a entrega da nota, encerrando neste ponto o Fluxo de Trabalho do Documento.

Com base nestes aspectos o Next2Web permite o desenvolvimento de aplicações, de uma forma ágil e pratica, pois o programador deve apenas desenvolver apenas as rotinas mais fundamentais a existência de determinado documento, como por exemplo:

    Para facilitar a programação de uma entrega o "Agendador" deve visualizar na tela, a quantidade de produtos na nota e o peso total dos produtos.
    (Isto remete ao conceito criacional de Virtual Fields no Web2Py).
    
    Para que isto ocorra, o programador deve definir um manipulador (handler) para cada uma das contagens no escopo do documento, e adicionar aos campos do documento, 2 registros do tipo "computed" e relacionar estes registros aos seus respectivos handlers.
    
E automaticamente ao exibir a tela o "Agendador" visualizará os dados necessários.

Em relação ao funcionamento do sistema, as configurações de inúmeros cálculos, e regras são definidas nas Regras de Negócio, por meio de uma linguagem de programação interna do Next2Web em idioma nativo.

Um exemplo é o cálculo do valor de comissão de uma venda, a regra para isto ficaria da seguinte forma:

    se document.status == 'CREATED' entao document.comissao = document.total * 0.06

A linha acima calcula uma comissão de 6% e salva a informação no registro do documento, para que ela possa ser utilizada no futuro e em relatórios.

Para isto o Documento possui os seguintes gatinhos:

    antes da validação
    durante a validação
    após a validação
    após a validação ser bem sucedida
    após a validação falhar

E tais regras são definidas dentro de um escopo do Fluxo de Trabalho, especificamente em Transições de Estado, ou seja, antes de um documento passar de um estado para outro estas regras são executadas e validadas. 

Por exemplo:

    No instante em que o Vendedor inicia um pedido, o Documento Pedido, está no estado de "rascunho", a transição é de "rascunho" para "salvo", no momento em que o Vendedor tentar salvar o documento, os gatilhos serão iniciados na ordem acima, e caso haja uma regra violada o documento não será salvo, e retornará a condição imediata antes a tentativa de salvamento, para que o Vendedor faça as devidas correções.

Caso todas as regras seja bem sucedidas o documento entrará em um novo estado, o "Salvo" e a Transição neste estado é de "salvo" para "liberado".
Dentro destes escopos há também as condições de Permissão e Participação. Por exemplo, no caso do documento Pedido como rascunho e salvo, a Participação é do Vendedor.
Já na transição de "salvo" para "liberado" a Participação é do Supervisor de Vendas.

Obrigado à:
    
Massimo Di Piero [1] , pelo Web2Py [2]

Bruno Rocha [3], pelo Movuca [4]
    
WebNotes [5] pelo wnframework [6]

Links:

[1] https://github.com/mdipierro

[2] http://web2py.com

[3] https://github.com/rochacbruno/

[4] https://github.com/rochacbruno/Movuca

[5] https://github.com/webnotes/

[6] https://github.com/webnotes/wnframework

### Layout com os recursos e widgets a serem implementados ###

[7] https://dl.dropbox.com/u/16453418/bootstrap/index.html 
