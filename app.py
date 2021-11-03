from flask import Flask, request, render_template, session
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(20).hex()


users = []

@app.route("/")
def main_page():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1 # обновление данных сессии
    else:
        session['visits'] = 1
    return f'<center><h3>Main page</center></h3><p>Пользователи:{users}<p>Количество посещений:{session["visits"]}'


@app.route("/login",methods = ['POST','GET'])
def login_page():
    if request.method == 'GET':
        if 'user' in session:
            return f'<h3>Вы зашли в систему как {session["user"]}<h3>'
        return render_template('form.html')

    if request.method == 'POST':
        if request.form["username"] not in users:
            users.append(request.form["username"])
            session['user'] = request.form["username"]
            session['visits'] = 0
            return f'<h3>Вы зашли в систему как {request.form["username"]}</h3>'
        return '<h3>Такой пользователь уже существует,попробуйте снова</h3>'


@app.route('/logout')
def logout():
    if 'user' in session:
        session['visits'] = 0
        users.remove(session['user'])
        session.pop('user')

        return '<h3>Вы успешно вышли<h3>'
    return f'<h3>Вы еще не авторизовались<h3>'


if __name__ == "__main__":
    app.run(debug=True)