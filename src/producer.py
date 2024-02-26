import json
import random
import redis
import logging


#  Генерация случайного 10-значного номера счета
#  *(В нашем примере номер счета состоит из 10
#  одинаковых цифр для простоты проверки)
def generate_account_number():
    return str(random.randint(1, 9)) * 10


# Генерация случайного сообщения
def generate_message():
    message = {
        "metadata": {
            "from": generate_account_number(),
            "to": generate_account_number()
        },
        "amount": random.randint(-10000, 10000)
    }
    return message


# Публикация сообщения в Redis pubsub
def publish_message(message):
    # Подключение к Redis
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    # Публикация в канал 'transactions'
    r.publish('transactions', json.dumps(message))


def main():
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)

    for _ in range(10):
        # Сгенерировать тестовое сообщение
        message = generate_message()
        # Логирование сгенерированного сообщения
        logging.info(f"Produced message: {message}")
        # Публикация сообщения
        publish_message(message)


if __name__ == "__main__":
    main()
