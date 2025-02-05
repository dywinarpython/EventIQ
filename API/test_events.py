from gpt_api_generate.generate_responce_gpt import request_in_a_clear_way
from yandex_search.search_yandex import main_search
from faker import Faker
import pytest


fake = Faker('ru_RU')
random_city = [fake.city() for i in range(50)]
event_types = [
    'Новый год', 'Свадьба', 'День рождения', 'Корпоратив', 'Конференция',
    'Выставка', 'Концерт', 'Мастер-класс', 'Фестиваль', 'Тренинг',
    'Тимбилдинг', 'Флешмоб', 'Благотворительное событие', 'Спортивные соревнования',
    'Гала-ужин', 'Рождество', 'Праздничный обед', 'Презентация', 'Воркшоп',
    'Кинопоказ', 'Выездной пикник', 'Караоке-вечеринка', 'День семьи',
    'Тематическая вечеринка', 'Турнир по настольным играм', 'Тренинг по личной эффективности',
    'Гриль-вечеринка', 'Флористический мастер-класс', 'Мода и стиль', 'Барбекю',
    'Чаепитие', 'Прогулка на природе', 'День благодарности', 'Фестиваль уличной еды',
    'Театральная премьера', 'Уроки танцев', 'Научная лекция', 'Творческая встреча',
    'Кулинарный мастер-класс', 'Интервью с экспертом', 'Сетевой маркетинг', 'Плавание в бассейне',
    'Йога-курс', 'Вечер настольных игр', 'Ночь искусств', 'Мастер-класс по фотографии',
    'Показы мод', 'Танцевальная вечеринка', 'Экологическая акция', 'Фото-сессия'
]


@pytest.mark.parametrize('event, where_event', list(zip(event_types, random_city)))
def test_searh_place_with_responce_gpt(event, where_event):
    event_info = main_search(event, where_event)
    assert event_info, 'Поиск был не успешен'
    responce_gpt = request_in_a_clear_way(event, event_info)
    assert responce_gpt, 'Нейросеть не дала ответ'
