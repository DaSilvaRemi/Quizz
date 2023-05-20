from flask import Flask, request, Response
from flask_cors import CORS
import jwt_utils
import hashlib
from models import Question, Participation, Player, PossibleAnswer
from utils import ConnectionManager
from http import HTTPStatus
# source venv/Scripts/activate
app = Flask(__name__)
CORS(app)

# UTILS ENDPOINTS
@app.route('/quiz-info', methods=['GET'])
def get_quiz_info() -> Response:
    """
    Get the quiz information including the size of questions and player scores.

    Returns:
        Response: The quiz information including the size of questions and player scores.
    """

    scores = []
    players: list[Player] = Player.get_all_player()

    for player in players:
        scores.append({"playerName": player.name,"score": player.score})

    return {"size": Question.get_nb_questions(), "scores": scores}, HTTPStatus.OK.value

@app.route('/login', methods=['POST'])
def login() -> Response:
    """
    Log in a user by checking the password.

    Returns:
        Response: The login result including the token if successful or UNAUTHORIZED status if unsuccessful.
    """

    payload: dict = request.get_json()
    password = payload['password'].encode('UTF-8')
    hashed = hashlib.md5(password).digest()

    if hashed != b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@':
        return HTTPStatus.UNAUTHORIZED.description, HTTPStatus.UNAUTHORIZED.value

    return {"token": jwt_utils.build_token()}, HTTPStatus.OK.value

@app.route('/rebuild-db', methods=['POST'])
def rebuild_db() -> Response:
    """
    Rebuild the database.

    Returns:
        Response: The result of the database rebuild or UNAUTHORIZED status if the authorization fails.
    """

    authorization = request.headers.get('Authorization')
    if not authorization or not authorization.startswith('Bearer '):
        return HTTPStatus.UNAUTHORIZED.description, HTTPStatus.UNAUTHORIZED.value

    token = authorization.split(" ")[1]
    try:
        jwt_utils.decode_token(token)
    except Exception as e:
        return HTTPStatus.UNAUTHORIZED.description, HTTPStatus.UNAUTHORIZED.value

    ConnectionManager().create()
    return "Ok", HTTPStatus.OK.value

# QUESTIONS

@app.route('/questions', methods=['POST'])
def create_new_question() -> Response:
    """
    Create a new question.

    Returns:
        Response: The newly created question or UNAUTHORIZED status if the authorization fails,
        or BAD_REQUEST status if the request data is invalid.
    """

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
        print(question_data)
        question = Question.from_json(question_data)
        question.save()
        return question.to_json()
    except Exception as e:
        return HTTPStatus.BAD_REQUEST.description, HTTPStatus.BAD_REQUEST.value


@app.route('/questions/<id_question>', methods=['GET'])
def get_question_by_id(id_question: int) -> Response:
    """
    Get a question by its ID.

    Args:
        id_question (int): The ID of the question.

    Returns:
        Response: The question data if found or NOT_FOUND status if the question is not found.
    """

    try:
        myQuestion = Question.get_by_id(id_question)
        return myQuestion.to_json()
    except Exception as e:
        return HTTPStatus.NOT_FOUND.description, HTTPStatus.NOT_FOUND.value

@app.route('/questions', methods=['GET'])
def get_question_by_position() -> Response:
    """
    Get a question by its position.

    Returns:
        Response: The question data if found or NOT_FOUND status if the question is not found.
    """

    try:
        position = request.args.get('position')
        myQuestion = Question.get_by_position(position)
        return myQuestion.to_json()
    except Exception as e:
        return HTTPStatus.NOT_FOUND.description, HTTPStatus.NOT_FOUND.value
    
@app.route('/questions/all', methods=['GET'])
def get_all_question() -> Response:
    """
    Get all questions.

    Returns:
        Response: The list of all questions.
    """

    try:
        questions_json = {"questions": []}
        questions = Question.get_all_questions()

        for question in questions:
            questions_json['questions'].append(question.to_json())

        return questions_json
    except Exception as e:
        return HTTPStatus.INTERNAL_SERVER_ERROR.description, HTTPStatus.INTERNAL_SERVER_ERROR.value
    
@app.route('/questions/<id_question>', methods=['PUT'])
def update_question_by_id(id_question: int) -> Response:
    """
    Update a question by its ID.

    Args:
        id_question (int): The ID of the question to update.

    Returns:
        Response: The result of the question update or NOT_FOUND status if the question is not found,
        or BAD_REQUEST status if the request data is invalid.
    """
     
    try:
        myQuestion = Question.get_by_id(id_question)
    except Exception as e:
        return HTTPStatus.NOT_FOUND.description, HTTPStatus.NOT_FOUND.value
    
    try:
        new_data = request.get_json()
        myQuestion.image    = new_data['image']
        myQuestion.position = new_data['position']
        myQuestion.text     = new_data['text']
        myQuestion.title    = new_data['title']

        myQuestion.delete_possible_answers()
        for new_possible_answer in new_data['possibleAnswers']:
            newPossibleAnswer = PossibleAnswer.from_json(new_possible_answer)
            newPossibleAnswer.id_possible_answer = None
            newPossibleAnswer.id_question = id_question
            newPossibleAnswer.save()

        myQuestion.save()
        return HTTPStatus.NO_CONTENT.description, HTTPStatus.NO_CONTENT.value
    except Exception as e:
        return HTTPStatus.NOT_FOUND.description, HTTPStatus.NOT_FOUND.value

@app.route('/questions/<id_question>', methods=['DELETE'])
def delete_question_by_id(id_question: int) -> Response:
    """
    Delete a question by its ID.

    Args:
        id_question (int): The ID of the question to delete.

    Returns:
        Response: The result of the question deletion or NOT_FOUND status if the question is not found,
        or UNAUTHORIZED status if the authorization fails.
    """

    authorization = request.headers.get('Authorization')
    if not authorization or not authorization.startswith('Bearer '):
        return HTTPStatus.UNAUTHORIZED.description, HTTPStatus.UNAUTHORIZED.value

    token = authorization.split(" ")[1]
    try:
        jwt_utils.decode_token(token)
    except Exception as e:
        return HTTPStatus.UNAUTHORIZED.description, HTTPStatus.UNAUTHORIZED.value


    myQuestion = Question.get_by_id(id_question)
    if not myQuestion:
        return HTTPStatus.NOT_FOUND.description, HTTPStatus.NOT_FOUND.value

    try:
        myQuestion.delete()
        return HTTPStatus.NO_CONTENT.description, HTTPStatus.NO_CONTENT.value
    except Exception as e:
        return HTTPStatus.INTERNAL_SERVER_ERROR.description, HTTPStatus.INTERNAL_SERVER_ERROR.value


@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions() -> Response:
    """
    Delete all questions.

    Returns:
        Response: The result of the question deletion or UNAUTHORIZED status if the authorization fails.
    """

    authorization = request.headers.get('Authorization')
    if not authorization or not authorization.startswith('Bearer '):
        return HTTPStatus.UNAUTHORIZED.description, HTTPStatus.UNAUTHORIZED.value

    token = authorization.split(" ")[1]
    try:
        jwt_utils.decode_token(token)
    except Exception as e:
        return HTTPStatus.UNAUTHORIZED.description, HTTPStatus.UNAUTHORIZED.value

    try:
        Question.delete_all()
        return HTTPStatus.NO_CONTENT.description, HTTPStatus.NO_CONTENT.value
    except Exception as e:
        return HTTPStatus.INTERNAL_SERVER_ERROR.description, HTTPStatus.INTERNAL_SERVER_ERROR.value


# PARTICIPATIONS
@app.route('/participations', methods=['POST'])
def post_participations() -> Response:
    """
    Post the participations and calculate the player's score.

    Returns:
        Response: The player's score if successful or BAD_REQUEST status if the request data is invalid.
    """

    body = request.get_json()

    player = Player(None, body['playerName'], 0)

    possible_answers_position: list = body['answers']

    # Verifie si le joueur a bien repondu a toute les questions
    nb_questions_in_bdd = Question.get_nb_questions()
    if len(possible_answers_position) != nb_questions_in_bdd:
        return HTTPStatus.BAD_REQUEST.description, HTTPStatus.BAD_REQUEST.value

    player.save()

    # Pour chaque reponse on verifie si le joueur a bien répondu et dans ce cas on lui ajoute un point
    for i in range(0, len(possible_answers_position)):
        possible_answer_position = possible_answers_position[i]
        position_question = i + 1

        question = Question.get_by_position(position_question)
        participation = Participation(player.id_player, question.id_question)
        possible_answer: PossibleAnswer = question.possible_answers[possible_answer_position - 1]

        if possible_answer.is_correct:
            player.score += 1

        participation.save()

    player.save()

    return {"playerName": player.name, "score": player.score}, HTTPStatus.OK.value
        
@app.route('/participations/all', methods=['DELETE'])
def delete_all_participations() -> Response:
    """
    Delete all participations.

    Returns:
        Response: The result of the participation deletion or UNAUTHORIZED status if the authorization fails.
    """
     
    authorization = request.headers.get('Authorization')
    if not authorization or not authorization.startswith('Bearer '):
        return HTTPStatus.UNAUTHORIZED.description, HTTPStatus.UNAUTHORIZED.value

    token = authorization.split(" ")[1]
    try:
        jwt_utils.decode_token(token)
    except Exception as e:
        return HTTPStatus.UNAUTHORIZED.description, HTTPStatus.UNAUTHORIZED.value

    try:
        Participation.delete_all()
        return HTTPStatus.NO_CONTENT.description, HTTPStatus.NO_CONTENT.value
    except Exception as e:
        return HTTPStatus.INTERNAL_SERVER_ERROR.description, HTTPStatus.INTERNAL_SERVER_ERROR.value


if __name__ == "__main__":
    app.run()