from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Путь к файлу базы данных
db_file = 'db.json'

# Чтение данных из базы данных
def read_db():
    try:
        with open(db_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": {}}

# Запись данных в базу данных
def write_db(data):
    with open(db_file, 'w') as file:
        json.dump(data, file, indent=4)

# Главная страница, отдаём index.html
@app.route('/')
def home():
    return render_template('index.html')

# Обработка запроса для увеличения кликов
@app.route('/increment', methods=['POST'])
def increment():
    # Получаем user_id из запроса
    data = request.get_json()
    user_id = data.get('user_id')

    # Читаем текущие данные из базы данных
    db = read_db()

    # Если пользователь не найден, создаем его запись
    if user_id not in db["users"]:
        db["users"][user_id] = {"clicks": 0}

    # Увеличиваем количество кликов
    db["users"][user_id]["clicks"] += 1

    # Записываем обновленные данные в базу
    write_db(db)

    # Возвращаем обновленные данные
    return jsonify({"clicks": db["users"][user_id]["clicks"]})

if __name__ == '__main__':
    app.run(debug=True)
