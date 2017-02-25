from app import app
from app.models.default import User
from bottle import request, template, static_file, redirect
import bcrypt


# static routes
@app.get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='app/static/css')


@app.get('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='app/static/js')


@app.get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='app/static/img')


@app.get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root='app/static/fonts')


@app.route('/')  # @get('/')
def login():
    return template('login', sucesso=True)


@app.route('/', method='POST')  # @post('/')
def acao_login(db, session):
    username = request.forms.get('username')
    password = request.forms.get('password')
    password_bytes = str.encode(password)
    try:
        user = db.query(User).filter(User.username == username).one()
        existe_username = True
    except:
        existe_username = False

    if existe_username:
        salt_bytes = str.encode(user.salt)
        hashed_bytes = bcrypt.hashpw(password_bytes, salt_bytes)
        hashed = hashed_bytes.decode()
        if user.hashed == hashed:
            session['name'] = username
            return redirect('/usuarios')
    return template('login', sucesso=False)



@app.route('/cadastro')
def cadastro():
    return template('cadastro', existe_username=False)


@app.route('/cadastro', method='POST')
def acao_cadastro(db, session):
    username = request.forms.get('username')
    password = request.forms.get('password')
    try:
        db.query(User).filter(User.username == username).one()
        existe_username = True
    except:
        existe_username = False
    if not existe_username:
        password_bytes = str.encode(password)
        salt_bytes = bcrypt.gensalt()
        salt = salt_bytes.decode()
        hashed_bytes = bcrypt.hashpw(password_bytes, salt_bytes)
        hashed = hashed_bytes.decode()
        new_user = User(username, hashed, salt)
        db.add(new_user)
        session['name'] = username
        return redirect('/usuarios')
    return template('cadastro', existe_username=True)


@app.route('/usuarios')
def usuarios(db, session):
    if session.get('name'):
        acesso = True
    else:
        acesso = False
    usuarios = db.query(User).all()
    return template('lista_usuarios', usuarios=usuarios, acesso=acesso)


@app.error(404)
def error404(error):
    return template('pagina404')
