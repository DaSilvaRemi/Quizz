from flask import Flask, request
from flask_cors import CORS
import jwt_utils
import hashlib
from models import Question, Participation
# source venv/Scripts/activate
app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    x = 'bonjegrgegour'
    return f"Hello, {x}"


@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    return {"size": 0, "scores": []}, 200


@app.route('/login', methods=['POST'])
def login():
    payload: dict = request.get_json()
    password = payload['password'].encode('UTF-8')
    hashed = hashlib.md5(password).digest()

    if hashed != b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@':
        return 'Unauthorized', 401

    return {"token": jwt_utils.build_token()}, 200


@app.route('/questions', methods=['POST'])
def post_questions():
    authorization = request.headers.get('Authorization')
    if not authorization or not authorization.startswith('Bearer '):
        return 'Unauthorized', 401

    token = authorization.split(" ")[1]
    try:
        jwt_utils.decode_token(token)
    except Exception as e:
        return 'Unauthorized', 401

    try:
        question_data = request.get_json()
        question = Question.from_json(question_data)
        question.save()
        return question.to_json()
    except Exception as e:
        return 'Bad Request', 400

@app.route('/questions/<id_question>', methods=['GET'])
def get_question_by_id(id_question):
    try:
      myQuestion: Question = Question.get_by_id(id_question)
      return myQuestion.to_json()
    except Exception as e:
        return 'Request respond Not Found', 404

@app.route('/participations', methods=['POST'])
def post_participations():
      body = request.get_json()

      #get player by his name

      id_player = 0

      position_answers = body['answers']
      #get questions
      for i in range(0, len(position_answers)):
          position_answer = position_answers[i]
          Participation(id_player, i + 1)
          #TO DO VERIF REPONSE

if __name__ == "__main__":
    app.run()
