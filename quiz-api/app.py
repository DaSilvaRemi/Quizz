from flask import Flask, request
from flask_cors import CORS
import jwt_utils
import hashlib
from models import Question
#source venv/Scripts/activate
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	x = 'bonjegrgegour'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
      return { "size": 0, "scores": [] }, 200

@app.route('/login', methods=['POST'])
def login():
      payload: dict = request.get_json()
      password = payload['password'].encode('UTF-8')
      hashed = hashlib.md5(password).digest()

      if hashed != b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@':
            return 'Unauthorized', 401

      return {"token": jwt_utils.build_token()}, 200

@app.route('/questions', methods=['POST'])
def postQuestions():
      authorization = request.headers.get('Authorization')
      authorization = authorization.split(" ")[1]
      try:
            jwt_utils.decode_token(authorization)
      except Exception as e:
            return 'Unauthorized', 401

      body = request.get_json()
      print('body : ', body)
      question: Question = Question.from_json(body)
      question.save()

      return question.to_json()


if __name__ == "__main__":
    app.run()