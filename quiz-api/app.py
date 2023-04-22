from flask import Flask, request
from flask_cors import CORS
import jwt_utils
import hashlib
from models import Question, Participation, Player, PossibleAnswer
from http import HTTPStatus
# source venv/Scripts/activate
app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    x = 'bonjegrgegour'
    return f"Hello, {x}"


@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    scores = []
    players: list[Player] = Player.get_all_player()

    for player in players:
        scores.append({"playerName": player.name,"score": player.score})

    return {"size": Question.get_nb_questions(), "scores": scores}, 200


@app.route('/login', methods=['POST'])
def login():
    payload: dict = request.get_json()
    password = payload['password'].encode('UTF-8')
    hashed = hashlib.md5(password).digest()

    if hashed != b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@':
        return 'Unauthorized', 401

    return {"token": jwt_utils.build_token()}, HTTPStatus.OK.value

# QUESTIONS

@app.route('/questions', methods=['POST'])
def create_new_question():
    authorization = request.headers.get('Authorization')
    if not authorization or not authorization.startswith('Bearer '):
        return HTTPStatus.UNAUTHORIZED.description, HTTPStatus.UNAUTHORIZED.value

    token = authorization.split(" ")[1]
    try:
        jwt_utils.decode_token(token)
    except Exception as e:
        return HTTPStatus.UNAUTHORIZED.description, HTTPStatus.UNAUTHORIZED.value

    try:
        question_data = request.get_json()
        question = Question.from_json(question_data)
        question.save()
        return question.to_json()
    except Exception as e:
        return HTTPStatus.BAD_REQUEST.description, HTTPStatus.BAD_REQUEST.value


@app.route('/questions/<id_question>', methods=['GET'])
def get_question_by_id(id_question):
    try:
        myQuestion = Question.get_by_id(id_question)
        return myQuestion.to_json()
    except Exception as e:
        return HTTPStatus.NOT_FOUND.description, HTTPStatus.NOT_FOUND.value


@app.route('/questions', methods=['GET'])
def get_question_by_position():
    try:
        position = request.args.get('position')
        myQuestion = Question.get_by_position(position)
        return myQuestion.to_json()
    except Exception as e:
        return HTTPStatus.NOT_FOUND.description, HTTPStatus.NOT_FOUND.value


@app.route('/questions/<id_question>', methods=['DELETE'])
def delete_question_by_id(id_question):
    try:
        myQuestion = Question.get_by_id(id_question)
        myQuestion.delete()
        return HTTPStatus.NO_CONTENT.description, HTTPStatus.NO_CONTENT.value
    except Exception as e:
        return HTTPStatus.UNAUTHORIZED.description, HTTPStatus.UNAUTHORIZED.value


@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions():
    try:
        Question.delete_all()
        return HTTPStatus.NO_CONTENT.description, HTTPStatus.NO_CONTENT.value
    except Exception as e:
        return HTTPStatus.UNAUTHORIZED.description, HTTPStatus.UNAUTHORIZED.value


# PARTICIPATIONS
@app.route('/participations', methods=['POST'])
def post_participations():
    body = request.get_json()

    player = Player(None, body['playerName'], 0)

    possible_answers_position: list = body['answers']

    # TO DO RECUP TOUTE les questions pour compter leur nombres ou faire une méthode permettant de les compter
    nb_questions_in_bdd = Question.get_nb_questions()
    if len(possible_answers_position) != nb_questions_in_bdd:
        return HTTPStatus.BAD_REQUEST.description, HTTPStatus.BAD_REQUEST.value

    player.save()

    # Pour chaque re
    for i in range(0, len(possible_answers_position)):
        possible_answer_position = possible_answers_position[i]
        position_question = i + 1
        # TO DO VERIF REPONSE
        question = Question.get_by_position(position_question)
        participation = Participation(player.id_player, question.id_question)
        possible_answer: PossibleAnswer = question.possible_answers[possible_answer_position - 1]

        if possible_answer.is_correct:
            player.score += 1

        participation.save()

    player.save()

    return {"playerName": player.name, "score": player.score}
        


if __name__ == "__main__":
    app.run()
