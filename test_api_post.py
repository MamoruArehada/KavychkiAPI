import requests
import json
import allure
from check_api import CheckApi


class TestApiPost:

    format_json = {
        'id': 101
    }

    @allure.suite('Тесты API')
    @allure.title('Тест API POST')
    def test_post(self):
        self.api_post('http://jsonplaceholder.typicode.com/posts')
        self.check_keys_in_response_json()

    def api_post(self, url):
        self.data = {
            'int': 5,
            'float': 5.5,
            'str': 'str',
            'list': [1, 2],
            'dict': {'dict': 'dict'},
            'bool': False,
            'none': None,
        }

        response = requests.post(url, json=self.data)
        assert CheckApi.check_status_code(response), f'Код ответа {response.status_code}'
        assert CheckApi.validate_json_response(response.text), f'В ответе от сервера невалидный json'
        self.response_json = json.loads(response.text)

    @staticmethod
    def add_default_json_response_post(data):
        data.update({'id': 101})

    @allure.step(f"Проверка модели из ответа с моделью отправленной")
    def check_keys_in_response_json(self):
        assert type(self.response_json) == dict, \
            f'В ответе от сервера в элементе массива не dict, а {type(self.response_json)}'
        self.add_default_json_response_post(self.data)
        response_keys = list(self.response_json.keys())
        send_json_keys = list(self.data.keys())
        assert CheckApi.check_keys_in_json(response_keys, send_json_keys), \
            f'Ответ от сервера с полями: {", ".join(response_keys)}' \
            f' не содержит всех необходимых полей: {", ".join(send_json_keys)}'
        new_key = CheckApi.chek_new_keys_in_json(response_keys, send_json_keys)
        assert not new_key, f'В ответе от сервер есть новые поля: {" ".join(new_key)}'
        for response_key in response_keys:
            self.check_model_element(response_key)

    @allure.step("Проверка модели элементов json")
    def check_model_element(self, response_key):
        if response_key != 'bool' and response_key != 'none':
            self.check_empty_value(self.response_json[response_key])
        self.check_type_values(type(self.response_json[response_key]), type(self.data[response_key]))
        self.check_values(self.response_json[response_key], self.data[response_key])

    @allure.step("Проверка что значение поля не null")
    def check_empty_value(self, response_value):
        assert response_value, f'Поле пустое'

    @allure.step("Проверка на соотвествие типов отправленых и полученных полей")
    def check_type_values(self, response_type, send_type):
        assert response_type == send_type,\
            f'Тип {response_type} не совпадают c {send_type}'

    @allure.step("Проверка на соотвествие значений отправленых и полученных полей")
    def check_values(self, response_value, send_value):
        assert response_value == send_value,\
            f'Значения {response_value} и {send_value}не совпадают.'
