from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	x = 'bonjegrgegour'
	return f"Hello, {x}"

if __name__ == "__main__":
    app.run()