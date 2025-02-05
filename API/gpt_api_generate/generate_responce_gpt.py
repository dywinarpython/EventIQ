import os
from mistralai import Mistral
from dotenv import load_dotenv
import environ
env = environ.Env()
environ.Env.read_env()

def get_api_mistralai(message: str) -> str:
    load_dotenv()
    api_key = env('MISTRAL_API_KEY')
    model = "ministral-8b-latest"

    client = Mistral(api_key=api_key)
    try:
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": message,
                },
            ]
        )
        assert chat_response, 'API не выдал нужный ответ'
        return chat_response.choices[0].message.content
    except Exception as e:
        print(f'Возникла ошибка: {e}')


def request_in_a_clear_way(event: str, event_info: dict, wish: str) -> list:
    st = f"Выполни следующие задачи, касающиеся мероприятия {event} и пожеланий: {wish}. Ответь на каждый пункт по порядку, не добавляя лишней информации, а также не повторяя мои слова. \
    1. Сколько человек примет участие в данном мероприятии? Количество человек: \
    2. Построить полный бюджет мероприятия в рублях, включая все нужные расходы (не подсчитывай итоговую сумму). Бюджет мероприятия: \
    3. Как долго будет длиться это мероприятие? Длительность: \
    4. Что уникального будет в этом мероприятии? Уникальная фишка: \
    5. Предложи программу мероприятия, то есть что там будет и как это все будет проходить. План мероприятия: \
    Простой и точный ответ на эти вопросы без лишних комментариев. Не переписывай запрос, просто ответь на каждый пункт - обязательное условие."
    try:
        text = get_api_mistralai(st)
        return text.strip()
    except Exception as e:
        print(f'Возникла ошибка: {e}')


if __name__ == '__main__':
    print(request_in_a_clear_way('Вечеринка в стиле 90',
          event_info=None, wish='Сделай по современному'))
