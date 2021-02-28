import requests
import json
import allure
from check_api import CheckApi


class TestApiGet:

    format_json = {
        'userId': int,
        'id': int,
        'title': str,
        'body': str,
    }

    FIELD_TITLE_MIN_LEN = 12  # 12
    FIELD_BODY_MIN_LEN = 102  # 102

    @allure.suite('Тесты API')
    @allure.title('Тест API GET')
    def test_get(self):

        response_json = self.api_get('http://jsonplaceholder.typicode.com/posts')
        self.check_element_json(response_json)

    @staticmethod
    def api_get(url):
        response = requests.get(url)
        assert CheckApi.check_status_code(response), f'Код ответа {response.status_code}'
        assert CheckApi.validate_json_response(response.text), f'В ответе от сервера невалидный json'
        response_json = json.loads(response.text)
        assert type(response_json) == list, f'В ответе от сервера не массив'
        assert response_json, f'В ответе от сервера пустой массив'
        return response_json

    @allure.step('Проверка элементов массива json')
    def check_element_json(self, response_json):
        self.format_json_keys = list(self.format_json.keys())
        self.count = 1
        for element in response_json:
            self.check_model_element_json(element)
            self.count += 1

    @allure.step(f"Проверка модели элемента на соответствие")
    def check_model_element_json(self, element):
        assert type(element) == dict, f'В ответе от сервера в элементе массива не dict, а {type(element)}'
        element_json_keys = list(element.keys())
        assert CheckApi.check_keys_in_json(element_json_keys, self.format_json_keys), \
            f'Ответ от сервера с полями: {", ".join(element_json_keys)}' \
            f' не содержит всех необходимых полей: {", ".join(self.format_json_keys)}'
        new_key = CheckApi.chek_new_keys_in_json(element_json_keys, self.format_json_keys)
        assert not new_key, f'В ответе от сервер есть новые поля: {new_key}'
        for format_json_key in self.format_json_keys:
            self.check_values(element, format_json_key)

    def check_values(self, element, format_json_key):
        self.keys_value = element[format_json_key]
        self.check_empty_value(self.keys_value)
        assert type(self.keys_value) == self.format_json[format_json_key], \
            f'Типы полей не совпадают, поле {format_json_key} имеет тип {type(self.keys_value)},' \
            f' а не {self.format_json[format_json_key]}'
        if type(self.keys_value) == str:
            if format_json_key == 'title':
                assert self.check_field_title(), f'Поле title c id = {element["id"]} короче 12 символов'
            if format_json_key == 'body':
                assert self.check_field_body(), f'Поле body c id = {element["id"]} короче 100 символов'
        if type(self.keys_value) == int:
            if format_json_key == 'userId':
                assert self.check_field_user_id(), f'Поле userId c id = {element["id"]} равно нулю'
            if format_json_key == 'id':
                assert self.check_field_id(), f'Поле id не равно порядковуму числу {self.count},' \
                                              f' а равно {self.keys_value}'

    @allure.step("Проверка что значение поля не null")
    def check_empty_value(self, response_value):
        assert response_value, f'Поле пустое'

    @allure.step(f"Проверка что в поле 'title' больше {FIELD_TITLE_MIN_LEN} символов")
    def check_field_title(self):
        if len(self.keys_value) >= self.FIELD_TITLE_MIN_LEN:
            return True
        else:
            return False

    @allure.step(f"Проверка что в поле 'body' больше {FIELD_BODY_MIN_LEN} символов")
    def check_field_body(self):
        if len(self.keys_value) >= self.FIELD_BODY_MIN_LEN:
            return True
        else:
            return False

    @allure.step("Проверка что поле 'userId' больше или равно 1 и меньше или равно 10")
    def check_field_user_id(self):
        if 1 <= self.keys_value <= 10:
            return True
        else:
            return False

    @allure.step("Проверка что поле 'id' равно порядковуму числу")
    def check_field_id(self):
        if self.keys_value == self.count:
            return True
        else:
            return False
