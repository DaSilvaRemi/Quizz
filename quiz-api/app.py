from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
	x = 'bonjegrgegour'
	return f"Hello, {x}"

if __name__ == "__main__":
    app.run()