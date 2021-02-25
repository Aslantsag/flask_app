import hashlib
import random
from models import *


@app.route('/')
def index():
    if not request.cookies.get('secret_key'):
        secret_key = hashlib.md5(str(datetime.now).encode()).hexdigest()
        secret_key = secret_key + str(random.randint(0, 999999))
        res = make_response("")
        res.set_cookie('secret_key', secret_key, max_age=60 * 60 * 24)
        res.headers['location'] = url_for('index')
        return res, 302
    else:
        posts = Posts.query.order_by(Posts.id.asc()).all()
        return render_template("index.html", posts=posts)

@app.route('/login', methods=['POST', 'GET'])
def login():

    LOGIN = 'BarberAdmin'
    PASSWORD = 'UpasWs143'

    if request.method == 'POST':
        login = request.form['login']
        passw = request.form['passw']

        if login == LOGIN and passw == PASSWORD:
            if not request.cookies.get('isAdmin'):
                res = make_response("")
                res.set_cookie('isAdmin', 'True', max_age=60 * 60 * 24 * 365 * 2)
                res.headers['location'] = url_for('index')
                return res, 302
            else:
                return redirect('/')
        else:
            err_text = 'Incorrect data!'
            return render_template('login.html', err_text=err_text)
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    res = make_response("")
    res.set_cookie('isAdmin', 'True', max_age=0)
    res.headers['location'] = url_for('index')
    return res, 302

@app.route('/create_post', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        u_name = request.form['u_name']
        u_phone = request.form['u_phone']
        secret_key = request.cookies.get('secret_key')
        if not u_name: u_name = 'Без имени'
        posts = Posts(u_name=u_name, u_phone=u_phone, secret_key=secret_key)

        try:
            db.session.add(posts)
            db.session.commit()
            return redirect('/')
        except:
            return "DB Error!"
    else:
        return render_template('index.html')

@app.route('/post/delete/<int:id>')
def delete_post(id):
    post = Posts.query.get(id)

    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/')
    except:
        return "DB Error!"

if __name__ == "__main__":
    app.run(debug=True)