from concurrent.futures import ThreadPoolExecutor, TimeoutError
from API.gpt_api_generate.generate_responce_gpt import request_in_a_clear_way
from API.yandex_search.search_yandex import main_search


def searh_place_with_responce_gpt(event, where_event, wish):
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_search_task, event, where_event, wish)
        try:
            return future.result(timeout=60)
        except TimeoutError:
            return {'text': 'Слишком большое ожидание', 'result': 'Возникли проблемы с сервером или на данный момент слишком большая очередь. Пожалуйста, повторите запрос через несколько минут.'}


def _search_task(event, where_event, wish):
    try:
        event_info = main_search(event, where_event)
        assert event_info, 'Поиск был не успешен'
        response_gpt = request_in_a_clear_way(event, event_info, wish)
        assert response_gpt, 'Нейросеть не дала ответ'
        return {'event_name': event, 'event': event_info, 'response_gpt': response_gpt}
    except Exception as e:
        print(f'Возникла ошибка: {e}')
        return {"text": "Запрос некоррекен", "result": "По вашему запросу ничего не найдено. Возможно, введены некорректные данные или указанное мероприятия мы пока не можем создать 😔."}


if __name__ == '__main__':
    content = searh_place_with_responce_gpt(
        'Масленица', 'Шахты', wish=None)
    print(content)
