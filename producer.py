import pika
import json
import random
import time
import os
import sys

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))

def main():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT
            )
        )
    except pika.exceptions.AMQPConnectionError:
        print(f"Erro: não foi possível conectar ao RabbitMQ em {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        print("Verifique se o RabbitMQ está em execução (docker compose up -d)")
        sys.exit(1)

    channel = connection.channel()

    channel.queue_declare(
        queue="iot",
        durable=True
    )

    print(f"Sensor IoT iniciado (conectado a {RABBITMQ_HOST}:{RABBITMQ_PORT})...")

    try:
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
                body=mensagem,
                properties=pika.BasicProperties(
                    delivery_mode=2  # mensagem persistente
                )
            )

            print(f"Enviado: {mensagem}")

            time.sleep(3)

    except KeyboardInterrupt:
        print("\nEncerrando producer...")
    finally:
        connection.close()

if __name__ == "__main__":
    main()