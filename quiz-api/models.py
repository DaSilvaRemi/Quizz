from utils import ConnectionManager

class Question(ConnectionManager):
    def __init__(self, title: str, text: str, image: str) -> None:
        self.id: int = None
        self.title = title
        self.text = text
        self.image = image

    def save(self):
        if self.id is None:
            query = "INSERT INTO question (title, text, image) VALUES (?, ?, ?)"
            result = self.execute(query, self.title, self.text, self.image)
            self.id = result.lastrowid
        else:
            query = "UPDATE question SET title=?, text=?, image=? WHERE id=?"
            self.execute(query, self.title, self.text, self.image, self.id)   

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "image": self.image
        }
    
    @staticmethod
    def from_json(json: dict) -> 'Question':
        return Question(json['title'], json['text'], json['image'])