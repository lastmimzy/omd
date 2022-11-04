import json
from keyword import iskeyword


class ColorizeMixin:
    """Класс, позволяющий назначать цвет через repr_color_code и
    выводить текстом объекты класса Advert: только ключи первого уровня
    в формате string(value1) | string(value2) ..."""

    repr_color_code = 33  # orange

    def color_text(self, code=repr_color_code):
        return "\33[{code}m".format(code=code)

    def __str__(self):
        return f"{self.color_text()}{self.__repr__()}\33[0m"


class JsonConverter:
    """Динамически создает атрибуты экземпляра класса из атрибутов JSON-объекта.
    Через _check_keyword к названию атрибутов, являющихся ключевыми
    словами python, добавляется _. """

    def __init__(self, dic: dict) -> None:
        for key, value in dic.items():
            key = key + "_" if iskeyword(key) else key
            self.__setattr__(key, self.JsonAttr2ClassAttr(value))

    def JsonAttr2ClassAttr(self, value):
        if isinstance(value, dict):
            return JsonConverter(value)
        elif isinstance(value, list):
            return [JsonConverter(element) if isinstance(element, dict)
                    else element for element in value]
        else:
            return value


class Advert(ColorizeMixin, JsonConverter):
    """Класс проверяет наличие и значение полей 'Price' и 'Title'.
    Через super обращается к методам других классов, помогающих
    конвертировать атрибуты JSON-объекта в атрибуты экземпляра класса"""

    def __init__(self, dic: dict) -> None:
        if "title" not in dic.keys():
            raise ValueError("provide title, please")
        if "price" not in dic.keys():
            self._price = 0
        super(Advert, self).__init__(dic)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if price < 0:
            raise ValueError("Price must be >=0")
        else:
            self._price = price

    def __repr__(self):
        return f"{self.title} | {self.price}"


if __name__ == "__main__":
    lesson_str = """
    {
        "title": "python",
        "price": 5,
        "class": "education",
        "location": {
            "address": "город Москва, Лесная, 7",
            "metro_stations": ["Белорусская"]
            }
    }"""
    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)

    # обращаемся к атрибуту location.address
    print('Check 1: "обращаться ĸ атрибутам можно через точĸу"')
    print(lesson_ad.location.address)

    # к названия атрибутов, являющихся ключевыми словами python,
    # в конце название добавляем _
    print('\nCheck 2: "к атрибутам - ключевым словам добавлилось _"')
    print(lesson_ad.class_)

    # проверяет, что значение цены не отрицательное и при
    # создании объекта и при присваивании
    print('\nCheck 3: "ошибка при присваивании отрицательной цены"')
    try:
        lesson_ad.price = -1
    except ValueError:
        print("Error! Price must be >=0")

    # проверяет, что возможно вывести в нужном формате объект класса
    print('\nCheck 4: "цветной вывод"')
    iphone_ad = Advert({"title": "iPhone X", "price": 100})
    print(iphone_ad)
