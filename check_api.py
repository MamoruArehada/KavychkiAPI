import json
import allure


class CheckApi:

    @staticmethod
    def check_status_code(response):
        if response.status_code == 200 or response.status_code == 201:
            return True
        else:
            return False

    @staticmethod
    @allure.step("Проверка валидности json в ответе от сервера")
    def validate_json_response(response_text):
        try:
            json.loads(response_text)
            return True
        except ValueError as e:
            print(e)
            return False

    @staticmethod
    @allure.step("Проверка наличия необходимых полей в модели")
    def check_keys_in_json(element_json_keys, required_keys):
        for required_key in required_keys:
            if required_key in element_json_keys:
                return True
            else:
                return False

    @staticmethod
    @allure.step("Проверка наличия новых полей в модели")
    def chek_new_keys_in_json(element_json_keys, required_keys):
        return list(set(element_json_keys) - set(required_keys))
