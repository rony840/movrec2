from flask import Flask




# Init app
app = Flask(__name__)

app.config['SECRET_KEY'] = '4c99e0361905b9f941f17729187afdb9'

from movie_rec import routes
