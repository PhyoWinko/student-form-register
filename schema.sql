DROP TABLE IF EXISTS students;
CREATE TABLE "students" (
    "id" INTEGER PRIMARY KEY,
    "name" TEXT NOT NULL,
    "year" TEXT NOT NULL,
    "roll_no" TEXT NOT NULL,
    "phone_number" TEXT NOT NULL,
    "email" TEXT NOT NULL
);

DROP TABLE IF EXISTS sports;
CREATE TABLE "sports" (
    "id" INTEGER PRIMARY KEY,
    "sport_name" TEXT NOT NULL
);

DROP TABLE IF EXISTS register;
CREATE TABLE "register" (
    "id" INTEGER PRIMARY KEY,
    "student_id" INTEGER NOT NULL,
    "sport_id" INTEGER NOT NULL,
    "register_time" DATETIME NOT NULL,
    FOREIGN KEY ("student_id") REFERENCES "students"("id"),
    FOREIGN KEY ("sport_id") REFERENCES "sports"("id")
);