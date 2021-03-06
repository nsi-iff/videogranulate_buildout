VideoGranulate Buildout
=======================

Sistema operacional
-------------------

Todos os serviços são desenvolvidos sob o sistema operacional Debian 6 (Squeeze) 64 bits e seu funcionamento só
é garantido em tal sistema operacional.

Dependências do sistema
-----------------------

Para o funcionamento do serviço, é necessário que os seguintes pacotes estejam instalados no sistema: python-dev, python-setuptools,
python-webunit, python-docutils, gnuplot, python-imaging, python-argparse, libcv4, libhighgui4, python-opencv, libxslt1.1, libxslt1-dev,
libxml2-dev

Durante a instalação do serviço, ao executar o comando *make*, todas essas dependências serão devidamente instaladas.

Arquitetura
-----------

Como pode ser visto no pacote **nsi.videogranulate** o sistema consiste em um **webservice RESTful** hostiado por padrão na porta 8885
na url **http://localhost:8885/**. Ele responde aos verbos POST e GET. Cada verbo correspondendo a uma ação do serviço de granularização:
POST para submeter um vídeo, GET para verificar o estado da granularização. Todos os verbos recebem parâmetros no formato **json**,
para melhor interoperabilidade com qualquer outra ferramenta. Para melhor entendimento da arquitetura, verificar diagrama na pasta
``docs``.


POST
    Recebe em um parâmetro **video** o vídeo a ser granularizado codificado em **base64**, para evitar problemas de encoding.
    E um parâmetro **filename**, muito importante para o armazenamento temporário e definição do codec usado para granularizar o vídeo.
    Responde a requisição com as chaves onde estarão o vídeos e os grãos correspondentes a ele no SAM, **video_key** e **grains_key**.
    É possível enviar uma URL para receber um **callback** assim que o vídeo for granularizado. Caso o parêmtro **callback**
    seja fornecido, ao término da granularização, um dos granularizadores realizará uma requisição para tal URL com o verbo
    POST, (se for necessário utilizar outro verbo, o mesmo deve ser informado no parâmetro **verb**) fornecendo no corpo 
    dela uma chave **done** com valor verdadeiro e a chave **key**, com a chave para acesso aos grãos.

GET
    Também é possível receber se os grãos de um vídeo já foram gerados fazendo uma requisição do tipo **GET** para o servidor,
    passando como parâmetro **key** o valor na chave **grains_key** que é retornada pelo método **POST**. O retorno será uma chave
    **done**, com valor verdadeiro caso os grão estejam prontos, e falso para o contrário.

Bibliotecas
-----------

- Cyclone
Cyclone é um fork do Tornado, um webserver criado originalmente pelo FriendFeed,
que foi comprado pelo Facebook mais tarde e teve seu código aberto. É baseado no
Twisted e tem suporte a bancos noSQL, como MongoDB e Redis, XMLRPC e JsonRPC,
além de um cliente HTTP assíncrono.

- txredisapi
É uma API que promove acesso assíncrono ao banco de dados Redis, feita em cima do Twisted.

- nsi.videogranulate
Pacote que contém a implementação das funções do serviço propriamente dito.

- nsi.granulate
Pacote que implementa a granularização de vídeo propriamente dita.

Instalação
----------

Assumindo que os serviços de armazenamento (SAM) e de conversão de vídeo já estão devidamente configurados e instalados,
criar um ambiente ``python 2.6 virtual`` (sem a opção ``--no-site-packages``), ativá-lo e executar o **make**.

**IMPORTANTE**: lembrar de configurar o SAM e o serviço de conversão de vídeos no arquivo ``buildout.cfg``.

Executando
----------

Basta executar o comando ``bin/videogranulate_ctl start`` que o serviço já estará online para o uso. Lembrando que ele depende
do **SAM** o do buildout do **sistema de filas **para funcionar corretamente. Para adicionar usuários ao serviço
``bin/add-user.py usuario senha`` e para deletar ``bin/del-user.py usuario``.

Para instalar o serviço de filas basta baixar o ``servicequeue_buildout`` e rodar o utilitário ``make`` contido nele. Depois,
basta executar o comando ``bin/rabbitmq-server -detached`` para ativar o serviço de filas.

Para executar a interface web de testes, executar ``bin/test_server_ctl start``. Isso colocará um servidor web na porta 8886, na
máquina local, com uma simples interface para envio de vídeos para o serviço.

Rodando os testes
-----------------

Com o **serviço de armazenamento (SAM)** rodando e com o usuário "test", com senha "test", adicionado, executar o comando
``make test``. Os testes serão rodados e o resultado será mostrado na tela.

Lembrando, novamente, que para que o serivço funcione é necessário que o sistema de filas esteja funcionando e ativado.

Testes de carga
---------------

Com o **serviço de armazenamento (SAM)** rodando e com o usuário "test", com senha "test", basta executar
``make load_test`` para rodar os testes de carga. Automaticamente, depois que o teste terminar, um **relatório em HTML**
será gerado na pasta ``tests/funkload_report`` com informações e gráficos relevantes sobre o teste.

Para alterar configurações do servidor de granularização e do teste de carga, ver arquivo ``tests/VideoGranulateBench.conf``.
