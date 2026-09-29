import pika
import json
import random
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

channel.queue_declare(
    queue="iot",
    durable=True
)

print("Sensor IoT iniciado...")

while True:

    temperatura = round(random.uniform(20, 35), 2)
    umidade = round(random.uniform(40, 80), 2)

    dados = {
        "sensor": "sensor-01",
        "temperatura": temperatura,
        "umidade": umidade
    }

    mensagem = json.dumps(dados)

    channel.basic_publish(
        exchange="",
        routing_key="iot",
        body=mensagem
    )

    print(f"Enviado: {mensagem}")

    time.sleep(3)