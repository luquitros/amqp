import pika
import json
import os
import sys

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))

def receber_mensagem(ch, method, properties, body):
    try:
        dados = json.loads(body)

        print(
            f"Sensor: {dados['sensor']} | "
            f"Temperatura: {dados['temperatura']}°C | "
            f"Umidade: {dados['umidade']}%"
        )

    except (json.JSONDecodeError, KeyError) as e:
        print(f"Erro ao processar mensagem: {e}")

    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

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

    channel.basic_consume(
        queue="iot",
        on_message_callback=receber_mensagem,
        auto_ack=False
    )

    print(f"Aguardando dados do sensor (conectado a {RABBITMQ_HOST}:{RABBITMQ_PORT})...")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nEncerrando consumer...")
        channel.stop_consuming()
    finally:
        connection.close()

if __name__ == "__main__":
    main()