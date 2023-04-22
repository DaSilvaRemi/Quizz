BEGIN TRANSACTION;

DROP TABLE IF EXISTS "admin";
CREATE TABLE "admin" (
    "id_admin" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "password" TEXT NOT NULL
);

DROP TABLE IF EXISTS "player";
CREATE TABLE "player" (
    "id_player" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "score" INTEGER NOT NULL
);

DROP TABLE IF EXISTS "possibleAnswer";
CREATE TABLE "possibleAnswer" (
    "id_possible_answer" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "text" TEXT NOT NULL,
    "isCorrect" BLOB NOT NULL,
    "id_question" INTEGER NOT NULL,
    FOREIGN KEY ("id_question") REFERENCES "question" ("id_question")
);

DROP TABLE IF EXISTS "question";
CREATE TABLE "question" (
    "id_question" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title" TEXT NOT NULL,
    "text" TEXT NOT NULL,
    "image" TEXT NOT NULL,
    "position" INTEGER NOT NULL
);

DROP TABLE IF EXISTS "participation";
CREATE TABLE "participation" (
    "id_player" INTEGER NOT NULL,
    "id_question" INTEGER NOT NULL,
    FOREIGN KEY ("id_player") REFERENCES "player" ("id_player"),
    FOREIGN KEY ("id_question") REFERENCES "question" ("id_question")
);

COMMIT;