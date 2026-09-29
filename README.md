# AMQP + RabbitMQ + Python

Projeto acadêmico desenvolvido para demonstrar o funcionamento do
protocolo **AMQP (Advanced Message Queuing Protocol)** aplicado a um
cenário de **Internet das Coisas (IoT)**.

A aplicação utiliza **Python**, a biblioteca **Pika**, **RabbitMQ** como
broker de mensagens e **Docker** para executar o RabbitMQ.

## Objetivo

Demonstrar, de forma prática, como uma aplicação pode produzir uma
mensagem, enviá-la através do AMQP para um broker RabbitMQ e permitir
que outra aplicação consuma essa mensagem.

O fluxo principal do projeto é:

``` text
Producer (Python)
       |
       | AMQP
       v
    RabbitMQ
       |
       v
    Exchange
       |
       v
     Queue
       |
       | AMQP
       v
Consumer (Python)
```

## Tecnologias utilizadas

-   Python
-   Pika
-   RabbitMQ
-   Docker / Docker Desktop
-   AMQP
-   VS Code

## Estrutura do projeto

``` text
amqp/
├── .venv/
├── producer.py
├── consumer.py
└── requirements.txt
```

### `producer.py`

É responsável por atuar como **Producer**.

Ele estabelece uma conexão com o RabbitMQ e publica uma mensagem. No
contexto do projeto, a mensagem representa um dado que poderia ser
produzido por um dispositivo IoT, como um sensor de temperatura.

Exemplo:

``` text
Temperatura: 28°C
```

### `consumer.py`

É responsável por atuar como **Consumer**.

Ele se conecta ao RabbitMQ, aguarda mensagens disponíveis na fila e
processa o conteúdo recebido.

### `requirements.txt`

Contém as dependências Python utilizadas pelo projeto, principalmente a
biblioteca Pika.

## Como funciona o AMQP no projeto

O AMQP é o protocolo responsável pela comunicação de mensagens entre as
aplicações e o broker.

O RabbitMQ funciona como intermediário entre quem produz e quem consome
as mensagens.

### 1. Producer

O Producer gera uma mensagem.

``` text
Python
  |
  | publica mensagem
  v
RabbitMQ
```

### 2. Exchange

No modelo utilizado pelo RabbitMQ, o Producer publica a mensagem em um
**Exchange**.

O Exchange é responsável pelo roteamento da mensagem.

``` text
Producer
   |
   v
Exchange
```

### 3. Queue

Depois do roteamento, a mensagem é direcionada para uma **Queue
(fila)**.

A fila mantém a mensagem até que um Consumer esteja pronto para
recebê-la.

``` text
Exchange
   |
   v
Queue
```

### 4. Consumer

O Consumer recebe a mensagem da fila e realiza o processamento.

``` text
Queue
  |
  v
Consumer
```

Portanto, o fluxo completo é:

``` text
Producer
   ↓
Exchange
   ↓
Queue
   ↓
Consumer
```

## Aplicação em IoT

Para relacionar o projeto à Internet das Coisas, podemos considerar o
Producer como um dispositivo ou gateway responsável por enviar dados de
sensores.

Por exemplo:

``` json
{
  "sensor": "temperatura-01",
  "temperatura": 28.5,
  "umidade": 64
}
```

O dispositivo envia os dados para o RabbitMQ através do AMQP.

Outro sistema pode consumir essas informações e utilizá-las para:

-   monitoramento;
-   armazenamento;
-   geração de alertas;
-   dashboards;
-   análise dos dados.

A principal vantagem é que o sensor não precisa conhecer diretamente o
sistema que irá processar a informação. O RabbitMQ faz a intermediação
das mensagens.

## RabbitMQ no Docker

O RabbitMQ é executado em um container Docker.

A arquitetura pode ser representada como:

``` text
┌───────────────────────────────┐
│         Docker                │
│                               │
│  ┌─────────────────────────┐  │
│  │       RabbitMQ           │  │
│  │                          │  │
│  │ Exchange → Queue         │  │
│  └─────────────────────────┘  │
└───────────────────────────────┘
              ▲
              │ AMQP
              ▼
       Aplicações Python
```

O Docker facilita a execução do broker sem a necessidade de instalar o
RabbitMQ diretamente no sistema operacional.

## Ambiente virtual Python

O projeto utiliza uma virtual environment para manter as dependências
isoladas.

No Windows PowerShell:

``` powershell
.\.venv\Scripts\Activate.ps1
```

Depois da ativação, o terminal deve apresentar algo semelhante a:

``` text
(.venv) PS C:\Users\...\amqp>
```

## Instalação

Com a virtual environment ativada:

``` powershell
python -m pip install -r requirements.txt
```

Caso o arquivo `requirements.txt` contenha Pika, a biblioteca será
instalada no ambiente virtual.

Também é possível instalar diretamente:

``` powershell
python -m pip install pika
```

## Executando o projeto

Primeiro, confirme que o RabbitMQ está em execução.

``` powershell
docker ps
```

Depois, com a virtual environment ativada, execute o Consumer:

``` powershell
python consumer.py
```

Em outro terminal, execute o Producer:

``` powershell
python producer.py
```

O Consumer ficará aguardando mensagens.

Quando o Producer enviar uma mensagem, ela deverá ser recebida pelo
Consumer.

Exemplo:

``` text
Producer:
Mensagem enviada!

Consumer:
Mensagem recebida:
Temperatura: 28°C
```

## Demonstração entre dois notebooks

Para a apresentação da disciplina, o projeto pode ser executado entre
dois computadores na mesma rede.

``` text
┌───────────────────┐
│    Notebook 1     │
│                   │
│  producer.py      │
└─────────┬─────────┘
          │
          │ AMQP / TCP
          │
          v
┌───────────────────┐
│     RabbitMQ      │
│       Docker      │
│                   │
│ Exchange → Queue  │
└─────────┬─────────┘
          │
          │ AMQP / TCP
          │
          v
┌───────────────────┐
│    Notebook 2     │
│                   │
│  consumer.py      │
└───────────────────┘
```

Nesse cenário, o computador que executa o RabbitMQ precisa permitir
conexões pela porta AMQP utilizada pelo broker, normalmente **5672**
para AMQP sem TLS.

O endereço utilizado pelo outro notebook deve ser o IP do computador que
executa o RabbitMQ, e não `localhost`.

## Verificando a rede

No computador que executa o RabbitMQ:

``` powershell
ipconfig
```

Identifique o endereço IPv4.

No outro notebook:

``` powershell
ping IP_DO_NOTEBOOK
```

Também é possível verificar a porta AMQP:

``` powershell
Test-NetConnection IP_DO_NOTEBOOK -Port 5672
```

O resultado esperado é:

``` text
TcpTestSucceeded : True
```

## Evidência de rede com Wireshark

Durante a demonstração, o Wireshark pode ser utilizado para observar o
tráfego entre as máquinas.

O objetivo é mostrar que a comunicação realmente ocorre pela rede:

``` text
Producer
   |
   | TCP
   v
RabbitMQ
   |
   | TCP
   v
Consumer
```

A comunicação AMQP utiliza TCP como transporte no cenário apresentado.

A captura de pacotes serve como evidência de que as mensagens estão
trafegando entre as aplicações e o broker.

## Por que utilizar um broker?

Sem um broker, uma aplicação poderia precisar conhecer diretamente o
endereço e as regras de comunicação de cada consumidor.

Com o RabbitMQ:

``` text
          RabbitMQ
         /    |    \
        /     |     \
       v      v      v
   Sistema  Dashboard  Alertas
```

O produtor publica a mensagem e os consumidores podem recebê-la conforme
as regras de roteamento configuradas.

Isso ajuda a criar sistemas desacoplados e facilita a comunicação entre
diferentes aplicações.

## Quando utilizar AMQP

AMQP pode ser interessante quando o sistema precisa de recursos de
mensageria mais completos, como:

-   filas;
-   roteamento de mensagens;
-   confirmação de entrega;
-   comunicação assíncrona;
-   desacoplamento entre produtores e consumidores;
-   integração entre diferentes aplicações e serviços.

## Quando considerar outra tecnologia

Em dispositivos IoT extremamente limitados em processamento, memória,
energia ou largura de banda, protocolos mais leves, como **MQTT**, podem
ser considerados.

A escolha do protocolo depende dos requisitos do sistema, da capacidade
dos dispositivos, do modelo de comunicação e dos requisitos de
confiabilidade.

## Resumo

O projeto demonstra o seguinte fluxo:

``` text
1. Python Producer gera uma mensagem
              ↓
2. Mensagem é publicada utilizando AMQP
              ↓
3. RabbitMQ recebe a mensagem
              ↓
4. Exchange realiza o roteamento
              ↓
5. Queue armazena a mensagem
              ↓
6. Python Consumer recebe a mensagem
              ↓
7. Aplicação processa o dado
```

No contexto de IoT, esse mecanismo permite que dados produzidos por
sensores sejam encaminhados para sistemas responsáveis por
processamento, armazenamento, monitoramento ou geração de alertas.

## Referências

-   RabbitMQ --- AMQP Concepts:
    https://www.rabbitmq.com/docs/amqp-concepts

-   RabbitMQ --- Documentation: https://www.rabbitmq.com/docs

-   Pika --- Python AMQP Client: https://pika.readthedocs.io/

-   OASIS --- AMQP: https://www.oasis-open.org/standards/
