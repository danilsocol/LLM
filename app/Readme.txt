Для запуска проекта требуется

1) pip install --upgrade pip


2)зависит от того в какой директории находитесь
pip install -r /app/requirements.txt
или
pip install -r /requirements.txt

3) Сам запуск
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
