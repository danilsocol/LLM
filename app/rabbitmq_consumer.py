import asyncio
import aio_pika
import json
import logging
from sqlalchemy.orm import Session
from fastapi import Depends
from database.database import get_session
from models.query import Query

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def callback(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            session_generator = get_session()
            session = next(session_generator)

            # Получение сессии БД
            data = json.loads(message.body)
            answer = data['answer']
            question_id = data['question_id']

            logger.info('Message received')

            query = session.query(Query).filter(Query.id == question_id).first()
            if query:
                query.answer = answer
                session.commit()
            else:
                logger.warning(f'No query found for id {question_id}')

            logger.info('Message processed')
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await message.nack(requeue=False)

async def start_consume():
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue('request_queue', durable=True)
        await queue.consume(callback, no_ack=False)
        logger.info('Consumer started')
        await asyncio.Future()  # Run forever
