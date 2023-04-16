BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "admin" (
	"id_admin"	INTEGER NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id_admin" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "player" (
	"id_player"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"score"	INTEGER NOT NULL,
	PRIMARY KEY("id_player" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "possibleAnswer" (
	"id_possible_answer"	INTEGER NOT NULL,
	"text"	TEXT NOT NULL,
	"isCorrect"	BLOB NOT NULL,
	"id_question"	INTEGER NOT NULL,
	FOREIGN KEY("id_question") REFERENCES "question",
	PRIMARY KEY("id_possible_answer" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "question" (
	"id_question"	INTEGER NOT NULL,
	"text"	TEXT NOT NULL,
	"title"	TEXT NOT NULL,
	"image"	TEXT NOT NULL,
	"position"	INTEGER NOT NULL,
	PRIMARY KEY("id_question" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "participation" (
	"id_player"	INTEGER NOT NULL,
	"id_question"	INTEGER NOT NULL,
	FOREIGN KEY("id_player") REFERENCES "player",
	FOREIGN KEY("id_question") REFERENCES "question"("id_question")
);
COMMIT;
