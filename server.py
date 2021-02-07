import flask


app = flask.Flask(__name__, 
                 static_url_path='',
                 static_folder='public/')
app.run(port=8081)