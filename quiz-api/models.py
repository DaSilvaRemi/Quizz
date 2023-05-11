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
        """
        Ajoute ou modifie une ligne existante

        Si la position de la question existe déjà
            - Si la question existe
                - new_pos > old_pos, on décrémente toute les positions entre ]old_pos; new_pos]
                - new_pos < old_pos, on incrémente toute les positions entre [position; position]
            - Sinon
                On incrémente toute les position au dessus de la position qui sera insérée
        """
        position_already_exists = len(ConnectionManager().execute(
            "SELECT question.position FROM question WHERE question.position=?", self.position).fetchall()) != 0

        if position_already_exists:
            if self.id_question is None:
                query = "UPDATE question SET position=position+1 WHERE position >= ?"
                ConnectionManager().execute(query, self.position)
            else:
                query = "SELECT question.position FROM question WHERE question.id_question=?"
                res = ConnectionManager().execute(query, self.id_question).fetchone()

                # Si new_pos > old_pos, on décrémente toute les positions entre ]old_pos; new_pos]
                # Si new_pos < old_pos, on incrémente toute les positions entre [position; position] . 
                if self.position > res[0]:
                    query = "UPDATE question SET position=position-1 WHERE position > ? AND position <= ?"
                    ConnectionManager().execute(query, res[0], self.position)
                elif self.position < res[0]:
                    query = "UPDATE question SET position=position+1 WHERE position >= ? AND position < ?"
                    ConnectionManager().execute(query, self.position, res[0])

        # Insertion uniquement si l'id de la question est vide puis modifications des possible answers
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

    def delete_possible_answers(self) -> None:
        for possibleAnswer in self.possible_answers:
            possibleAnswer.delete()

    def delete(self) -> None:
        self.delete_possible_answers()
        query = "DELETE FROM question WHERE id_question=?"
        ConnectionManager().execute(query, self.id_question)

        query = "UPDATE question SET position=position-1 WHERE position > ?"
        ConnectionManager().execute(query, self.position)

    @staticmethod
    def delete_all() -> None:
        PossibleAnswer.delete_all()
        query = "DELETE FROM question"
        ConnectionManager().execute(query)

    @staticmethod
    def get_nb_questions() -> int:
        query = "SELECT COUNT(*) FROM question"
        query_result = ConnectionManager().execute(query)
        return query_result.fetchone()[0]

    @staticmethod
    def get_all_questions() -> list['Question']:
        query = "SELECT * FROM question;"
        result = ConnectionManager().execute(query).fetchall()

        # TIPS : PREND EXEMPLE DE LA METHODE get_all_player de Player

        return result

    @staticmethod
    def get_by_id(id_question) -> 'Question':
        query = "SELECT * FROM question WHERE id_question=?"
        result = ConnectionManager().execute(query, id_question)
        res = result.fetchone()

        if res is None:
            return None

        id, title, text, image, position = res
        return Question(id, title, text, image, position, PossibleAnswer.get_by_id_question(id))

    @staticmethod
    def get_by_position(position_question) -> 'Question':
        query = "SELECT * FROM question WHERE question.position=?"
        result = ConnectionManager().execute(query, position_question)
        res = result.fetchone()

        if res is None:
            return None

        id, title, text, image, position = res
        return Question(id, title, text, image, position, PossibleAnswer.get_by_id_question(id))

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
        self.is_correct = isCorrect == 1
        self.id_question = id_question

    def save(self) -> None:
        if self.id_possible_answer is None:
            query = "INSERT INTO possibleAnswer (text, isCorrect, id_question) VALUES (?, ?, ?)"
            result = ConnectionManager().execute(
                query, self.text, self.is_correct, self.id_question)
            self.id_possible_answer = result.lastrowid
        else:
            query = "UPDATE possibleAnswer SET text=?, isCorrect=?, id_question=? WHERE id_possible_answer=?"
            ConnectionManager().execute(query, self.text, self.is_correct,
                                        self.id_question, self.id_possible_answer)

    def delete(self) -> None:
        query = "DELETE FROM possibleAnswer WHERE id_possible_answer=?"
        ConnectionManager().execute(query, self.id_possible_answer)

    @staticmethod
    def delete_all() -> None:
        query = "DELETE FROM possibleAnswer"
        ConnectionManager().execute(query)

    @staticmethod
    def get_by_id(id_possible_answer) -> 'PossibleAnswer':
        connexionManager = ConnectionManager()
        query = "SELECT * FROM possibleAnswer WHERE id_possible_answer=?"
        query_result = connexionManager.execute(query, id_possible_answer)
        elements = query_result.fetchone()

        if elements is None:
            return None

        return PossibleAnswer(elements[0], elements[1], elements[2], elements[3])

    @staticmethod
    def get_by_id_question(id_question) -> list['PossibleAnswer']:
        connexionManager = ConnectionManager()
        query = "SELECT * FROM possibleAnswer WHERE possibleAnswer.id_question=?"
        query_result = connexionManager.execute(query, id_question)
        elements = query_result.fetchall()

        possiblesAnswers = []

        if elements is None:
            return possiblesAnswers

        for element in elements:
            id, text, isCorrect, id_question = element
            possiblesAnswers.append(PossibleAnswer(
                id, text, isCorrect, id_question))

        return possiblesAnswers

    def to_json(self) -> dict:
        return {
            "id": self.id_possible_answer,
            "text": self.text,
            "isCorrect": self.is_correct,
            "id_question": self.id_question
        }

    def __str__(self):
        return str(self.to_json())

    @staticmethod
    def from_json(json: dict) -> 'PossibleAnswer':
        return PossibleAnswer(json.get("id", None), json['text'], json['isCorrect'], json.get("id_question", None))


class Participation:
    def __init__(self, id_player: int, id_question: int) -> None:
        self.id_player = id_player
        self.id_question = id_question

    def save(self) -> None:
        if self.id_player is not None and self.id_question is not None:
            query = "INSERT INTO participation (id_player, id_question) VALUES (?, ?)"
            ConnectionManager().execute(query, self.id_player, self.id_question)
        elif self.id_player is not None and self.id_question is None:
            query = "UPDATE participation SET id_question=? WHERE id_player=?"
            ConnectionManager().execute(query, self.id_question, self.id_player)
        else:
            query = "UPDATE participation SET id_player=? WHERE id_question=?"
            ConnectionManager().execute(query, self.id_player, self.id_question)

    def delete(self) -> None:
        query = "DELETE FROM participation WHERE id_player=? AND id_question=?"
        ConnectionManager().execute(query, self.id_player, self.id_question)

        player = Player.get_by_id(self.id_player)
        player.delete()

    @staticmethod
    def delete_all() -> None:
        query = "DELETE FROM participation"
        ConnectionManager().execute(query)

        Player.delete_all()

    def delete_by_id_player(self) -> None:
        query = "DELETE FROM participation WHERE id_player=?"
        ConnectionManager().execute(query, self.id_player)

    def delete_by_id_question(self) -> None:
        query = "DELETE FROM participation WHERE id_question=?"
        ConnectionManager().execute(query, self.id_question)

    @staticmethod
    def get_by_id_player_and_question(id_player: int, id_question: int) -> 'Participation':
        connexionManager = ConnectionManager()
        query = "SELECT * FROM participation WHERE id_player=? AND id_question=?"
        query_result = connexionManager.execute(query, id_player, id_question)
        elements = query_result.fetchone()

        if elements is None:
            return None

        return Participation(elements[0], elements[1])

    @staticmethod
    def get_by_id_player(id_player: int) -> list['Participation']:
        connexionManager = ConnectionManager()
        query = "SELECT * FROM participation WHERE id_player=?"
        query_result = connexionManager.execute(query, id_player)
        elements = query_result.fetchall()

        if elements is None:
            return None

        participations = []

        for element in elements:
            id_player, id_question = element
            participations.append(Participation(id_player, id_question))

        return participations

    @staticmethod
    def get_by_id_question(id_question) -> list['Participation']:
        connexionManager = ConnectionManager()
        query = "SELECT * FROM participation WHERE id_question=?"
        query_result = connexionManager.execute(query, id_question)
        elements = query_result.fetchall()

        if elements is None:
            return None

        participations = []

        for element in elements:
            id_player, id_question = element
            participations.append(Participation(id_player, id_question))

        return participations

    def to_json(self) -> dict:
        return {
            "id_player": self.id_player,
            "id_question": self.id_question
        }

    def __str__(self):
        return str(self.to_json())

    @staticmethod
    def from_json(json: dict) -> 'Participation':
        return Participation(json.get("id_player", None), json.get("id_question", None))

# Admin


class Admin():
    def __init__(self, id_admin: int, password: str) -> None:
        self.id_admin = id_admin
        self.password = password

    def save(self) -> None:
        if self.id_admin is None:
            query = "INSERT INTO admin(password) VALUES (?)"
            result = ConnectionManager().execute(query, self.password)
            self.id_admin = result.lastrowid
        else:
            query = "UPDATE admin SET password = ? WHERE id_admin = ?"
            ConnectionManager().execute(query, self.password, self.id_admin)

    def delete(self) -> None:
        query = "DELETE FROM admin WHERE id_admin = ? "
        ConnectionManager().execute(query, self.id_admin)

    @staticmethod
    def get_by_id(id_admin) -> 'Admin':
        query = "SELECT * FROM admin WHERE id_admin = ? "
        result = ConnectionManager().execute(query, id_admin)
        res = result.fetchone()

        if res is None:
            return None

        id, password = res
        return Admin(id, password)

    def to_json(self) -> dict:
        return {
            "id_admin": self.id_admin,
            "id_password": self.password
        }

    def __str__(self):
        return str(self.to_json())

    @staticmethod
    def from_json(json: dict) -> 'Admin':
        return Admin(json.get("id_admin", None), json.get("id_password", None))


# Player
class Player():
    def __init__(self, id_player: int, name: str, score: str) -> None:
        self.id_player = id_player
        self.name = name
        self.score = score

    def save(self) -> None:
        if self.id_player is None:
            query = "INSERT INTO player(name, score) VALUES (?, ?)"
            result = ConnectionManager().execute(query, self.name, self.score)
            self.id_player = result.lastrowid
        else:
            query = "UPDATE player SET name = ?, score = ? WHERE id_player = ?"
            ConnectionManager().execute(query, self.name, self.score, self.id_player)

    def delete(self) -> None:
        query = "DELETE FROM player WHERE id_player = ? "
        ConnectionManager().execute(query, self.id_player)

    @staticmethod
    def delete_all() -> None:
        query = "DELETE FROM player"
        ConnectionManager().execute(query)


    @staticmethod
    def get_all_player() -> list['Player']:
        query = "SELECT * FROM player ORDER BY score DESC"
        query_result = ConnectionManager().execute(query)
        elements = query_result.fetchall()

        players = []

        if elements is None:
            return players

        for element in elements:
            id, name, score = element
            players.append(Player(id, name, score))

        return players

    @staticmethod
    def get_by_id(id_player) -> 'Player':
        query = "SELECT * FROM player WHERE id_player = ? "
        result = ConnectionManager().execute(query, id_player)
        res = result.fetchone()

        if res is None:
            return None

        id, name, score = res
        return Player(id, name, score)

    @staticmethod
    def get_by_name(name) -> 'Player':
        query = "SELECT * FROM player WHERE name = ? "
        result = ConnectionManager().execute(query, name)
        res = result.fetchone()

        if res is None:
            return None

        id, name, score = res
        return Player(id, name, score)

    def to_json(self) -> dict:
        return {
            "id_player": self.id_player,
            "name": self.name,
            "score": self.score
        }

    def __str__(self):
        return str(self.to_json())

    @staticmethod
    def from_json(json: dict) -> 'Player':
        return Player(json.get("id_player", None), json.get("name", None), json.get("score", None))
