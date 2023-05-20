from utils import ConnectionManager
import json


class Question():
    def __init__(self, id_question: int, title: str, text: str, image: str, position: int, possible_answers: list['PossibleAnswer']) -> None:
        """
        Initializes a Question object with the given parameters.

        Args:
            id_question (int): The ID of the question.
            title (str): The title of the question.
            text (str): The text of the question.
            image (str): The image associated with the question.
            position (int): The position of the question.
            possible_answers (list['PossibleAnswer']): List of PossibleAnswer objects associated with the question.
        """
        self.id_question = id_question
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.possible_answers = possible_answers

    def save(self) -> None:
        """
        Adds or modifies an existing question.

        If the position of the question already exists:
            - If the question exists:
                - new_pos > old_pos, decrement the positions between (old_pos, new_pos]
                - new_pos < old_pos, increment the positions between [new_pos, old_pos)
            - Otherwise, increment all positions above the position to be inserted.
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

                if self.position > res[0]:
                    query = "UPDATE question SET position=position-1 WHERE position > ? AND position <= ?"
                    ConnectionManager().execute(query, res[0], self.position)
                elif self.position < res[0]:
                    query = "UPDATE question SET position=position+1 WHERE position >= ? AND position < ?"
                    ConnectionManager().execute(query, self.position, res[0])

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
        """
        Deletes all possible answers associated with the question.
        """
        PossibleAnswer.delete_by_id_question(self.id_question)

    def delete(self) -> None:
        """
        Deletes the question and its associated possible answers.
        """
        self.delete_possible_answers()
        query = "DELETE FROM question WHERE id_question=?"
        ConnectionManager().execute(query, self.id_question)

        query = "UPDATE question SET position=position-1 WHERE position > ?"
        ConnectionManager().execute(query, self.position)

    @staticmethod
    def delete_all() -> None:
        """
        Deletes all questions and their associated possible answers.
        """
        PossibleAnswer.delete_all()
        query = "DELETE FROM question"
        ConnectionManager().execute(query)

    @staticmethod
    def get_nb_questions() -> int:
        """
        Retrieves the number of questions in the database.

        Returns:
            int: The number of questions.
        """
        query = "SELECT COUNT(*) FROM question"
        query_result = ConnectionManager().execute(query)
        return query_result.fetchone()[0]

    @staticmethod
    def get_all_questions() -> list['Question']:
        """
        Retrieves all the questions from the database.

        Returns:
            list['Question']: A list of Question objects.
        """

        questions = []

        query = "SELECT * FROM question ORDER BY question.position;"
        results = ConnectionManager().execute(query).fetchall()

        if results is None:
            return None

        for res in results:
            id, title, text, image, position = res
            question = Question(id, title, text, image,
                                position, PossibleAnswer.get_by_id_question(id))
            questions.append(question)

        return questions

    @staticmethod
    def get_by_id(id_question) -> 'Question':
        """
        Retrieves a question from the database by its ID.

        Args:
            id_question: The ID of the question.

        Returns:
            'Question': The Question object if found, otherwise None.
        """

        query = "SELECT * FROM question WHERE id_question=?"
        result = ConnectionManager().execute(query, id_question)
        res = result.fetchone()

        if res is None:
            return None

        id, title, text, image, position = res
        return Question(id, title, text, image, position, PossibleAnswer.get_by_id_question(id))

    @staticmethod
    def get_by_position(position_question) -> 'Question':
        """
        Retrieves a question from the database by its position.

        Args:
            position_question: The position of the question.

        Returns:
            'Question': The Question object if found, otherwise None.
        """

        query = "SELECT * FROM question WHERE question.position=?"
        result = ConnectionManager().execute(query, position_question)
        res = result.fetchone()

        if res is None:
            return None

        id, title, text, image, position = res
        return Question(id, title, text, image, position, PossibleAnswer.get_by_id_question(id))

    def to_json(self) -> dict:
        """
        Converts the Question object to a JSON-compatible dictionary.

        Returns:
            dict: The JSON representation of the Question object.
        """

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
        """
        Creates a Question object from a JSON dictionary.

        Args:
            json (dict): The JSON dictionary representing a Question object.

        Returns:
            'Question': The created Question object.
        """

        possibleAnswers = []
        for possibleAnswer in json['possibleAnswers']:
            possibleAnswers.append(PossibleAnswer.from_json(possibleAnswer))

        return Question(json.get("id", None), json['title'], json['text'], json['image'], json['position'], possibleAnswers)


class PossibleAnswer():
    def __init__(self, id_possible_answer: int, text: str, isCorrect: bool, id_question: int) -> None:
        """
        Initializes a PossibleAnswer object.

        Args:
            id_possible_answer (int): The ID of the possible answer.
            text (str): The text of the possible answer.
            isCorrect (bool): Indicates whether the possible answer is correct.
            id_question (int): The ID of the question associated with the possible answer.
        """
        self.id_possible_answer = id_possible_answer
        self.text = text
        self.is_correct = isCorrect == 1
        self.id_question = id_question

    def save(self) -> None:
        """
        Saves the possible answer to the database.
        If the possible answer is new, it is inserted. Otherwise, it is updated.
        """

        if self.id_possible_answer is None:
            query = "INSERT INTO possibleAnswer (text, isCorrect, id_question) VALUES (?, ?, ?)"
            result = ConnectionManager().execute(
                query, self.text, self.is_correct, self.id_question)
            self.id_possible_answer = result.lastrowid
        else:
            query = "UPDATE possibleAnswer SET text = ?, isCorrect = ?, id_question = ? WHERE id_possible_answer = ?"
            ConnectionManager().execute(query, self.text, self.is_correct,
                                        self.id_question, self.id_possible_answer)

    def delete(self) -> None:
        """
        Deletes the possible answer from the database.
        """

        query = "DELETE FROM possibleAnswer WHERE id_possible_answer = ?"
        ConnectionManager().execute(query, self.id_possible_answer)

    @staticmethod
    def delete_by_id_question(id_question: int) -> None:
        """
        Deletes all possible answers associated with a specific question from the database.

        Args:
            id_question (int): The ID of the question.
        """

        query = "DELETE FROM possibleAnswer WHERE id_question = ?"
        ConnectionManager().execute(query, id_question)

    @staticmethod
    def delete_all() -> None:
        """
        Deletes all possible answers from the database.
        """

        query = "DELETE FROM possibleAnswer"
        ConnectionManager().execute(query)

    @staticmethod
    def get_by_id(id_possible_answer: int) -> 'PossibleAnswer':
        """
        Retrieves a possible answer from the database by its ID.

        Args:
            id_possible_answer (int): The ID of the possible answer.

        Returns:
            'PossibleAnswer': The PossibleAnswer object if found, otherwise None.
        """

        connexionManager = ConnectionManager()
        query = "SELECT * FROM possibleAnswer WHERE id_possible_answer=?"
        query_result = connexionManager.execute(query, id_possible_answer)
        elements = query_result.fetchone()

        if elements is None:
            return None

        return PossibleAnswer(elements[0], elements[1], elements[2], elements[3])

    @staticmethod
    def get_by_id_question(id_question: int) -> list['PossibleAnswer']:
        """
        Retrieves all possible answers associated with a specific question from the database.

        Args:
            id_question (int): The ID of the question.

        Returns:
            list['PossibleAnswer']: A list of PossibleAnswer objects.
        """

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
        """
        Converts the PossibleAnswer object to a JSON-compatible dictionary.

        Returns:
            dict: The JSON representation of the PossibleAnswer object.
        """

        return {
            "id": self.id_possible_answer,
            "text": self.text,
            "isCorrect": self.is_correct,
            "id_question": self.id_question
        }

    def __str__(self) -> str:
        """
        Returns a string representation of the PossibleAnswer object.

        Returns:
            str: The string representation of the PossibleAnswer object.
        """

        return str(self.to_json())

    @staticmethod
    def from_json(json: dict) -> 'PossibleAnswer':
        """
        Creates a PossibleAnswer object from a JSON dictionary.

        Args:
            json (dict): The JSON dictionary representing a PossibleAnswer object.

        Returns:
            'PossibleAnswer': The created PossibleAnswer object.
        """
        return PossibleAnswer(json.get("id", None), json['text'], json['isCorrect'], json.get("id_question", None))


class Participation:
    def __init__(self, id_player: int, id_question: int) -> None:
        """
        Initializes a Participation object.

        Args:
            id_player (int): The ID of the player participating.
            id_question (int): The ID of the question the player participated in.
        """

        self.id_player = id_player
        self.id_question = id_question

    def save(self) -> None:
        """
        Saves the participation record to the database.
        If the participation record is new, it is inserted. Otherwise, it is updated.
        """

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
        """
        Deletes the participation record from the database.
        The associated player record is also deleted.
        """

        query = "DELETE FROM participation WHERE id_player=? AND id_question=?"
        ConnectionManager().execute(query, self.id_player, self.id_question)

        player = Player.get_by_id(self.id_player)
        player.delete()

    @staticmethod
    def delete_all() -> None:
        """
        Deletes all participation records from the database.
        All associated player records are also deleted.
        """

        query = "DELETE FROM participation"
        ConnectionManager().execute(query)

        Player.delete_all()

    def delete_by_id_player(self) -> None:
        """
        Deletes all participation records associated with the current player from the database.
        """

        query = "DELETE FROM participation WHERE id_player=?"
        ConnectionManager().execute(query, self.id_player)

    @staticmethod
    def delete_by_id_question(self) -> None:
        """
        Deletes all participation records associated with the current question from the database.
        """

        query = "DELETE FROM participation WHERE id_question=?"
        ConnectionManager().execute(query, self.id_question)

    @staticmethod
    def get_by_id_player_and_question(id_player: int, id_question: int) -> 'Participation':
        """
        Retrieves a participation record from the database by player ID and question ID.

        Args:
            id_player (int): The ID of the player.
            id_question (int): The ID of the question.

        Returns:
            'Participation': The Participation object if found, otherwise None.
        """
        connexionManager = ConnectionManager()
        query = "SELECT * FROM participation WHERE id_player=? AND id_question=?"
        query_result = connexionManager.execute(query, id_player, id_question)
        elements = query_result.fetchone()

        if elements is None:
            return None

        return Participation(elements[0], elements[1])

    @staticmethod
    def get_by_id_player(id_player: int) -> list['Participation']:
        """
        Retrieves all participation records associated with a player from the database.

        Args:
            id_player (int): The ID of the player.

        Returns:
            list['Participation']: A list of Participation objects if found, otherwise None.
        """

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
        """
        Retrieves all participation records associated with a question from the database.

        Args:
            id_question (int): The ID of the question.

        Returns:
            list['Participation']: A list of Participation objects if found, otherwise None.
        """

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
        """
        Converts the Participation object to a JSON-compatible dictionary.

        Returns:
            dict: The JSON representation of the Participation object.
        """

        return {
            "id_player": self.id_player,
            "id_question": self.id_question
        }

    def __str__(self) -> str:
        """
        Returns the string representation of the Participation object.

        Returns:
            str: The string representation of the Participation object.
        """

        return str(self.to_json())

    @staticmethod
    def from_json(json: dict) -> 'Participation':
        """
        Creates a Participation object from a JSON-compatible dictionary.

        Args:
            json (dict): The JSON representation of the Participation object.

        Returns:
            'Participation': The created Participation object.
        """

        return Participation(json.get("id_player", None), json.get("id_question", None))

# Player


class Player():
    def __init__(self, id_player: int, name: str, score: str) -> None:
        """
        Initializes a Player object.

        Args:
            id_player (int): The ID of the player.
            name (str): The name of the player.
            score (str): The score of the player.
        """

        self.id_player = id_player
        self.name = name
        self.score = score

    def save(self) -> None:
        """
        Saves the player record to the database.
        If the player record is new, it is inserted. Otherwise, it is updated.
        """

        if self.id_player is None:
            query = "INSERT INTO player(name, score) VALUES (?, ?)"
            result = ConnectionManager().execute(query, self.name, self.score)
            self.id_player = result.lastrowid
        else:
            query = "UPDATE player SET name = ?, score = ? WHERE id_player = ?"
            ConnectionManager().execute(query, self.name, self.score, self.id_player)

    def delete(self) -> None:
        """
        Deletes the player record from the database.
        """

        query = "DELETE FROM player WHERE id_player = ? "
        ConnectionManager().execute(query, self.id_player)

    @staticmethod
    def delete_all() -> None:
        """
        Deletes all player records from the database.
        """

        query = "DELETE FROM player"
        ConnectionManager().execute(query)

    @staticmethod
    def get_all_player() -> list['Player']:
        """
        Retrieves all player records from the database.

        Returns:
            list['Player']: A list of Player objects if found, otherwise an empty list.
        """

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
    def get_by_id(id_player: int) -> 'Player':
        """
        Retrieves a player record by ID from the database.

        Args:
            id_player (int): The ID of the player.

        Returns:
            'Player': The retrieved Player object if found, otherwise None.
        """

        query = "SELECT * FROM player WHERE id_player = ? "
        result = ConnectionManager().execute(query, id_player)
        res = result.fetchone()

        if res is None:
            return None

        id, name, score = res
        return Player(id, name, score)

    @staticmethod
    def get_by_name(name: str) -> 'Player':
        """
        Retrieves a player record by name from the database.

        Args:
            name (str): The name of the player.

        Returns:
            'Player': The retrieved Player object if found, otherwise None.
        """

        query = "SELECT * FROM player WHERE name = ? "
        result = ConnectionManager().execute(query, name)
        res = result.fetchone()

        if res is None:
            return None

        id, name, score = res
        return Player(id, name, score)

    def to_json(self) -> dict:
        """
        Converts the Player object to a JSON-compatible dictionary.

        Returns:
            dict: The JSON representation of the Player object.
        """

        return {
            "id_player": self.id_player,
            "name": self.name,
            "score": self.score
        }

    def __str__(self):
        """
        Returns the string representation of the Player object.

        Returns:
            str: The string representation of the Player object.
        """

        return str(self.to_json())

    @staticmethod
    def from_json(json: dict) -> 'Player':
        """
        Creates a Player object from a JSON-compatible dictionary.

        Args:
            json (dict): The JSON representation of the Player object.

        Returns:
            'Player': The created Player object.
        """

        return Player(json.get("id_player", None), json.get("name", None), json.get("score", None))
