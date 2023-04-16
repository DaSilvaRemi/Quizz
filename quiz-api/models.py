from utils import ConnectionManager

class Question(ConnectionManager):
    def __init__(self, id_question: int, title: str, text: str, image: str, position: int) -> None:
        self.id_question = id_question
        self.title = title
        self.text = text
        self.image = image
        self.position = position

    def save(self):
        if self.id_question is None:
            query = "INSERT INTO question (title, text, image, position) VALUES (?, ?, ?, ?)"
            result = self.execute(query, self.title, self.text, self.image, self.position)
            self.id_question = result.lastrowid
        else:
            query = "UPDATE question SET title=?, text=?, image=?, position=? WHERE id_question=?"
            self.execute(query, self.title, self.text, self.image, self.position, self.id_question)

    @staticmethod
    def get_by_id(id_question) -> 'Question':
        connexionManager = ConnectionManager()
        query = "SELECT * FROM question WHERE id_question=?"
        result = connexionManager.execute(query, id_question)
        res = result.fetchone()

        return Question(res[0], res[1], res[2], res[3], res[4])


    @staticmethod
    def get_by_position():
        pass

    def to_json(self) -> dict:
        return {
            "id_question": self.id_question,
            "title": self.title,
            "text": self.text,
            "image": self.image,
            "position": self.position
        }

    @staticmethod
    def from_json(json: dict) -> 'Question':
        return Question(None, json['title'], json['text'], json['image'], json['position'])

    # finir R & D


class PossibleAnswer(ConnectionManager):
    def __init__(self, id_possible_answer: int, text: str, isCorrect: bool, id_question: int) -> None:
        self.id_possible_answer = id_possible_answer
        self.text = text
        self.isCorrect = isCorrect
        self.id_question = id_question

    def save(self):
        if self.id_possible_answer is None:
            query = "INSERT INTO possibleAnswer (text, isCorrect, id_question) VALUES (?, ?, ?)"
            result = self.execute(query, self.text, self.isCorrect, self.id_question)
            self.id_possible_answer = result.lastrowid
        else:
            query = "UPDATE possibleAnswer SET text=?, isCorrect=?, id_question=? WHERE id_possible_answer=?"
            self.execute(query, self.text, self.isCorrect, self.id_question, self.id_possible_answer)

    def to_json(self) -> dict:
        return {
            "id_possible_answer": self.id_possible_answer,
            "text": self.text,
            "isCorrect": self.isCorrect,
            "id_question": self.id_question
        }

    @staticmethod
    def from_json(json: dict) -> 'Question':
        return Question(None, json['text'], json['isCorrect'], json['id_question'])

    # finir CRUD
