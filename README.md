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
-   Docker / Docker Compose
-   AMQP
-   VS Code

## Estrutura do projeto

``` text
amqp/
├── consumer.py          # Consumer — recebe mensagens da fila
├── producer.py          # Producer — publica mensagens na fila
├── docker-compose.yml   # Configuração do RabbitMQ no Docker
├── requirements.txt     # Dependências Python
├── .env.example         # Exemplo de variáveis de ambiente
├── .gitignore           # Arquivos ignorados pelo Git
└── README.md            # Documentação do projeto
```

### `producer.py`

É responsável por atuar como **Producer**.

Ele estabelece uma conexão com o RabbitMQ e publica mensagens em loop.
No contexto do projeto, as mensagens representam dados que poderiam ser
produzidos por um dispositivo IoT, como um sensor de temperatura e
umidade.

Exemplo de mensagem publicada:

``` json
{
  "sensor": "sensor-01",
  "temperatura": 28.5,
  "umidade": 64.3
}
```

### `consumer.py`

É responsável por atuar como **Consumer**.

Ele se conecta ao RabbitMQ, aguarda mensagens disponíveis na fila e
processa o conteúdo recebido. Utiliza confirmação manual de mensagens
(`auto_ack=False`) para garantir que mensagens não sejam perdidas.

### `docker-compose.yml`

Configura o container do RabbitMQ com a interface de gerenciamento
(Management UI) e volume persistente.

### `requirements.txt`

Contém as dependências Python utilizadas pelo projeto:

-   `pika` — biblioteca Python para comunicação AMQP com o RabbitMQ.

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
  "sensor": "sensor-01",
  "temperatura": 28.5,
  "umidade": 64.3
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

O RabbitMQ é executado em um container Docker utilizando o arquivo
`docker-compose.yml` incluído no projeto.

A arquitetura pode ser representada como:

``` text
┌───────────────────────────────┐
│         Docker                │
│                               │
│  ┌─────────────────────────┐  │
│  │       RabbitMQ           │  │
│  │                          │  │
│  │ Exchange → Queue         │  │
│  │                          │  │
│  │ Management UI :15672     │  │
│  └─────────────────────────┘  │
└───────────────────────────────┘
              ▲
              │ AMQP (:5672)
              ▼
       Aplicações Python
```

O Docker facilita a execução do broker sem a necessidade de instalar o
RabbitMQ diretamente no sistema operacional.

## Pré-requisitos

-   [Python 3.8+](https://www.python.org/downloads/)
-   [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Instalação e Execução

### 1. Clonar o repositório

``` powershell
git clone <URL_DO_REPOSITORIO>
cd amqp
```

### 2. Subir o RabbitMQ com Docker

``` powershell
docker compose up -d
```

Aguarde alguns segundos para o RabbitMQ inicializar. Verifique se está
rodando:

``` powershell
docker compose ps
```

A Management UI estará disponível em: http://localhost:15672
(login: `guest` / senha: `guest`)

### 3. Criar e ativar o ambiente virtual Python

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Depois da ativação, o terminal deve apresentar algo semelhante a:

``` text
(.venv) PS C:\Users\...\amqp>
```

### 4. Instalar as dependências

``` powershell
pip install -r requirements.txt
```

### 5. Executar o Consumer

``` powershell
python consumer.py
```

### 6. Executar o Producer (em outro terminal)

``` powershell
.\.venv\Scripts\Activate.ps1
python producer.py
```

### Saída esperada

**Producer:**
``` text
Sensor IoT iniciado (conectado a localhost:5672)...
Enviado: {"sensor": "sensor-01", "temperatura": 28.53, "umidade": 64.21}
Enviado: {"sensor": "sensor-01", "temperatura": 22.17, "umidade": 55.89}
```

**Consumer:**
``` text
Aguardando dados do sensor (conectado a localhost:5672)...
Sensor: sensor-01 | Temperatura: 28.53°C | Umidade: 64.21%
Sensor: sensor-01 | Temperatura: 22.17°C | Umidade: 55.89%
```

Para encerrar, pressione `Ctrl+C` em cada terminal.

### Parar o RabbitMQ

``` powershell
docker compose down
```

Para remover também os dados persistidos:

``` powershell
docker compose down -v
```

## Configuração de Host

Por padrão, os scripts conectam em `localhost:5672`. Para alterar o
host (por exemplo, ao conectar de outro computador na rede):

**Opção 1 — Variável de ambiente:**

``` powershell
$env:RABBITMQ_HOST = "192.168.1.100"
python producer.py
```

**Opção 2 — Criar arquivo `.env`:**

Copie o `.env.example` para `.env` e altere os valores:

``` powershell
Copy-Item .env.example .env
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

No notebook remoto, configure o host antes de executar:

``` powershell
$env:RABBITMQ_HOST = "IP_DO_NOTEBOOK_COM_RABBITMQ"
python producer.py
```

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
