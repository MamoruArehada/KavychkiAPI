# KavychkiAPI

Инструкция для запуска в PyCharm на Windows

Установка необходимых всех библиотек
ввести в терминале PyCharm
```
pip install -r requirements.txt
```
Запуск всех тестов api
ввести в терминале PyCharm
```
python -m pytest --alluredir=C:\Users\User
```

или изменить запуск файлов в PyCharm на pytest
```File| Settings| Tools| Python Integrated Tools``` и измените средство запуска тестов по умолчанию на py.test и запустить один из тестов,
чтобы получить отчеты нужно добавить аргументы запуска, для этого в окне Run/Debug Configuration в Additionak Arguments добавить ``` --alluredir=C:\Users\User```

Гайд по установки allure в для генерации отчетов
https://docs.qameta.io/allure/

Выполнить в PowerShell
```
allure serve C:\Users\User
```
после отчет откроется в браузере, который по умолчанию
