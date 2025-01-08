import pika
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_message_to_rabbitmq(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    try:
        logger.info("Sending message to RabbitMQ")
        channel = connection.channel()
        channel.queue_declare(queue='question_queue')
        channel.basic_publish(
            exchange='',
            routing_key='question_queue',
            body=json.dumps(message),
        )
        logger.info("Message sent successfully")
    except Exception as e:
        logger.error(f"Error sending message: {e}")
    finally:
        if connection:
            connection.close()

def process_query(user_id: int, context: str, question: str, question_id: int):
    message = {
        'user_id': user_id,
        'context': context,
        'question': question,
        'question_id': question_id
    }
    send_message_to_rabbitmq(message)
