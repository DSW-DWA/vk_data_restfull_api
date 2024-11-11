# vk_data_restfull_api

Нужно сделать виртуальное окружение
```bash
python -m venv .venv
```
Открыть окружение
```bash
.venv\Scripts\activate
```
Установить зависимости
```bash
pip install -r .\requirements.txt
```

Учтите тесты проводятся на чистой бд и данные из вашей бд будут удаленны. Тесты запускают из корневой папки командой:
```bash
pytest
```

Перед запуском api
1) В этом приложении нужно задать правильный токен (например, "secret-token") в .env, поэтому В headers запросов должно быть поле Authorization: Bearer secret-token 
2) Укажите ваш абсолютный путь до папки src в .env
3) Укажите подключение к бд в .env

Запустить api нужно из папки src
```bash
cd src
uvicorn main:app --reload
```