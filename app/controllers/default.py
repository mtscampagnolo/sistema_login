from app import app
from bottle import request, template, static_file
from app.models.default import insert_user


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


@app.route('/') # @get('/')
def login():
	return template('login')

def check_login(username, password):
	d = {'marcos':'python', 'joao':'java', 'pedro':'go'}
	if username in d.keys() and d[username] == password:
		return True
	return False

@app.route('/', method='POST') # @post('/')
def acao_login():
	username = request.forms.get('username')
	password = request.forms.get('password')
	return template('verificacao_login', sucesso=True)

@app.route('/cadastro')
def cadastro():
	return template('cadastro')
@app.route('/cadastro', method='POST')
def acao_cadastro():
	username = request.forms.get('username')
	password = request.forms.get('password')
	insert_user(username, password)
	return template('verificacao_cadastro', nome=username)

@app.error(404)
def error404(error):
	return template('pagina404')