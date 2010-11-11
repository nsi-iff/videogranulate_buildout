VideoGranulate Buildout

Arquitetura
-----------

Como pode ser visto no pacote "nsi.vidoegranulate" o sistema consiste em um webservice (xmlrpc) hostiado por padrão na porta 8885 na url "http://usuario:senha@localhost:8885/xmlrpc". O serviço contém uma função "granulate" que é reponsável por converter o vídeo para formato livre (utilizando o VideoConvert Buildout) e então colocar seu UID em uma fila de vídeos a serem granularizados, juntamente com o UID onde os grãos ficarão, além de retornar o último para o usuário para que ele possa saber se os grãos já foram gerados ou não.
Então os slaves procuram por itens na fila, recuperam o vídeos, geram os grãos e guardam eles no SAM. Ao perguntar para o servidor se os grãos já estão gerados, ele verifica se há uma flag no valor correspondente á aquele UID, se não houver retorna True, caso contrário False.

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

Instalação
----------

Assumindo que os serviços de armazenamento (SAM) e de conversão de vídeo já estão devidamente configurados e instalados, criar um ambiente python virtual (sem a opção --no-site-packages), ativá-lo e executar o "make"

Executando
----------
TERMINAR.

