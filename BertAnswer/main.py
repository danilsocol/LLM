import pika
import json
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

nlp = pipeline("question-answering", model="cointegrated/rut5-base-multitask")

def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        user_id = message['user_id']
        context = message['context']
        question = message['question']
        question_id = message['question_id']

        result1 = nlp(question=question, context=context)
        answer = result1['answer']

        logger.info(f"Context: {context}")
        logger.info(f"Question: {question}")
        logger.info(f"Answer: {answer}")

        ch.basic_ack(delivery_tag=method.delivery_tag)
        send_request(answer, question_id)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def send_request(answer, question_id):
    connection1 = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))

    try:
        logger.info("Sending answer")
        channel1 = connection1.channel()
        message = {
            'answer': answer,
            'question_id': question_id
        }
        channel1.queue_declare(queue='request_queue', durable=True, passive=True)
        channel1.basic_publish(
            exchange='',
            routing_key='request_queue',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=1,
            )
        )
        logger.info("Answer sent successfully")
    except Exception as e:
        logger.error(f"Error sending answer: {e}")
    finally:
        if connection1:
            connection1.close()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
try:
    channel = connection.channel()
    channel.queue_declare(queue='question_queue')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='question_queue', on_message_callback=callback)

    logger.info("[*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
except Exception as e:
    logger.error(f"Error in consumer: {e}")
finally:
    if connection:
        connection.close()
