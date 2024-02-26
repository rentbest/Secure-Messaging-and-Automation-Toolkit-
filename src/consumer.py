import json
import argparse
import redis
import logging


# Подписка на сообщения из канала 'transactions' в Redis pubsub
def consume_messages(bad_guys):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    pubsub = r.pubsub()
    pubsub.subscribe('transactions')
    for item in pubsub.listen():
        if item['type'] == 'message':
            message = json.loads(item['data'])
            logging.info(f"Received message: {message}")
            process_message(message, bad_guys)


# Обработка сообщения: замена отправителя и получателя при необходимости
def process_message(message, bad_guys):
    sender = message['metadata']['from']
    receiver = message['metadata']['to']
    if receiver in bad_guys and message['amount'] >= 0:
        message['metadata']['from'], message['metadata']['to'] = receiver, sender
    print(json.dumps(message))


# Тестовая функция для запуска из командной строки
def test():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--bad_guys", required=True,
                        help="List of bad guys' account numbers")
    args = parser.parse_args()

    bad_guys = args.bad_guys.split(',')
    consume_messages(bad_guys)


if __name__ == "__main__":
    test()
