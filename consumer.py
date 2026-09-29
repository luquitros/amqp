import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

channel.queue_declare(
    queue="iot",
    durable=True
)

def receber_mensagem(ch, method, properties, body):

    dados = json.loads(body)

    print(
        f"Sensor: {dados['sensor']} | "
        f"Temperatura: {dados['temperatura']}°C | "
        f"Umidade: {dados['umidade']}%"
    )

channel.basic_consume(
    queue="iot",
    on_message_callback=receber_mensagem,
    auto_ack=True
)

print("Aguardando dados do sensor...")

channel.start_consuming()