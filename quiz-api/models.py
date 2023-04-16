from utils import ConnectionManager
import json


class Question():
    def __init__(self, id_question: int, title: str, text: str, image: str, position: int, possible_answers: list['PossibleAnswer']) -> None:
        self.id_question = id_question
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.possible_answers = possible_answers

    def save(self) -> None:
        if self.id_question is None:
            query = "INSERT INTO question (title, text, image, position) VALUES (?, ?, ?, ?)"
            result = ConnectionManager().execute(
                query, self.title, self.text, self.image, self.position)
            self.id_question = result.lastrowid
        else:
            query = "UPDATE question SET title=?, text=?, image=?, position=? WHERE id_question=?"
            ConnectionManager().execute(query, self.title, self.text,
                                        self.image, self.position, self.id_question)

        for possible_answer in self.possible_answers:
            possible_answer.id_question = self.id_question
            possible_answer.save()

    def delete(self):
        # N'oublie pas d'appeler la méthode delete de chaque PossibleAnswer avant de delete ton objet (à cause des clés étrangères)
        pass

    @staticmethod
    def get_by_id(id_question) -> 'Question':
        connexionManager = ConnectionManager()
        query = "SELECT * FROM question WHERE id_question=?"
        result = connexionManager.execute(query, id_question)
        res = result.fetchone()

        if res is None:
            return None

        id, title, text, image, position = res
        return Question(id, title, text, image, position, PossibleAnswer.getByIdQuestion(id))

    @staticmethod
    def get_by_position() -> 'Question':
        pass

    def to_json(self) -> dict:
        return {
            "id": self.id_question,
            "title": self.title,
            "text": self.text,
            "image": self.image,
            "position": self.position,
            "possibleAnswers": [possible_answer.to_json() for possible_answer in self.possible_answers]
        }

    @staticmethod
    def from_json(json: dict) -> 'Question':
        possibleAnswers = []
        for possibleAnswer in json['possibleAnswers']:
            possibleAnswers.append(PossibleAnswer.from_json(possibleAnswer))

        return Question(json.get("id", None), json['title'], json['text'], json['image'], json['position'], possibleAnswers)

    # finir R & D

class PossibleAnswer():
    def __init__(self, id_possible_answer: int, text: str, isCorrect: bool, id_question: int) -> None:
        self.id_possible_answer = id_possible_answer
        self.text = text
        self.isCorrect = isCorrect == 1
        self.id_question = id_question

    def save(self) -> None:
        if self.id_possible_answer is None:
            query = "INSERT INTO possibleAnswer (text, isCorrect, id_question) VALUES (?, ?, ?)"
            result = ConnectionManager().execute(
                query, self.text, self.isCorrect, self.id_question)
            self.id_possible_answer = result.lastrowid
        else:
            query = "UPDATE possibleAnswer SET text=?, isCorrect=?, id_question=? WHERE id_possible_answer=?"
            ConnectionManager().execute(query, self.text, self.isCorrect,
                                        self.id_question, self.id_possible_answer)

    def delete(self) -> None:
        query = "DELETE FROM WHERE id_possible_answer=?"
        ConnectionManager().execute(query, self.id_possible_answer)

    @staticmethod
    def getById(id_possible_answer) -> 'PossibleAnswer':
        connexionManager = ConnectionManager()
        query = "SELECT * FROM possibleAnswer WHERE id_possible_answer=?"
        query_result = connexionManager.execute(query, id_possible_answer)
        elements = query_result.fetchone()

        if elements is None:
            return None

        return PossibleAnswer(elements[0], elements[1], elements[2], elements[3])

    @staticmethod
    def getByIdQuestion(id_question) -> list['PossibleAnswer']:
        connexionManager = ConnectionManager()
        query = "SELECT * FROM possibleAnswer WHERE possibleAnswer.id_question=?"
        query_result = connexionManager.execute(query, id_question)
        elements = query_result.fetchall()

        if elements is None:
            return None

        possiblesAnswers = []

        for element in elements:
            id, text, isCorrect, id_question = element
            possiblesAnswers.append(PossibleAnswer(id, text, isCorrect, id_question))

        return possiblesAnswers

    def to_json(self) -> dict:
        return {
            "id": self.id_possible_answer,
            "text": self.text,
            "isCorrect": self.isCorrect,
            "id_question": self.id_question
        }

    def __str__(self):
        return str(self.to_json())

    @staticmethod
    def from_json(json: dict) -> 'PossibleAnswer':
        return PossibleAnswer(json.get("id", None), json['text'], json['isCorrect'], json.get("id_question", None))

    # finir CRUD
