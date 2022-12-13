from flask import Flask, request, jsonify
import sqlite3
import hashlib
import datetime

app = Flask(__name__)



@app.route('/users', methods=['GET'])
def run_users():
    with sqlite3.connect('user.db') as con:
        #with con:
         #   con.execute("""
          #      CREATE TABLE user1 (
           #        user_name VARCHAR(40),
            #       password VARCHAR(40),
             #      date varchar(10)

       # );
        #    """)
        cur = con.cursor()
        cur.execute('select * from user1')
        list_of_users = cur.fetchall() #Метод cursor.fetchall() выбирает все оставшиеся строки результата запроса, возвращая список.
        return jsonify(list_of_users)


@app.route('/users', methods=['POST'])
def registr():
    if not (request.json and 'user_name' in request.json and 'password' in request.json):
        return '', 400 #Если неправильный формат введенный данных, пример: {"user_name": "m", "password": "m"}
    with sqlite3.connect('user.db') as con:
        cur = con.cursor()
        cur.execute('select user_name from user1 where user_name = ?', (request.json['user_name'],)) #ищем совпадения введенных данных с тем, что уже есть
        result = cur.fetchone() #Метод cursor.fetchone() извлекает следующую строку из набора результатов запроса, возвращая одну последовательность или None, если больше нет доступных данных.
        if result is not None: #если fetchone возвращает не нан, получается уже есть такой пользователь
            return jsonify({'результат':'такой пользователь уже существует!'}), 400
        userinfo = request.json['user_name']+request.json['password']
        userinfo = hashlib.md5(userinfo.encode()).hexdigest() #хешируем
        date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        cur.execute('insert into user1 values (?,?,?)', (request.json['user_name'], userinfo, date))
        return jsonify({'результат':'пользователь добавлен!'})



@app.route('/')
def start_page():
    return 'Привет! Введите /users, чтобы получить список всех пользователей, или отправьте метод POST через postman, чтобы зарегестрироваться!'


if __name__ == '__main__':
    app.run()
