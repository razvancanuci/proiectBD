import os
import sqlite3
import re

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(CURRENT_PATH, 'ServiceAuto.db')


def regex(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None


class DataBase:
    CREATE_SCRIPT = [''' CREATE TABLE detaliimasini (
    nr_inmatriculare VARCHAR2(10) CHECK(nr_inmatriculare REGEXP '^[A-Z]{1,2}\s[0-9]{2,3}\s[A-Z]{3}$' AND length(nr_inmatriculare)=9) PRIMARY KEY NOT NULL,
    model            VARCHAR2(20) CHECK(model REGEXP '^[A-Za-z0-9\s]+') NOT NULL,
    an_fabricatie    NUMBER(4) NOT NULL CHECK ( an_fabricatie BETWEEN 1990 AND 2021 ),
    serie_sasiu      VARCHAR2(20) UNIQUE NOT NULL,
    valabilitate_itp NUMBER(1)
);''',
                     '''
CREATE TABLE lucrari (
    id_lucrare   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nume_lucrare VARCHAR2(40) CHECK(nume_lucrare REGEXP '^[A-Za-z\s+]+') NOT NULL,
    id_meserie   VARCHAR2(3) CHECK ( id_meserie IN ( 'REC', 'MEC', 'ELE' ) ) NOT NULL,
    cost_ora     NUMBER(4) CHECK ( cost_ora > 0 ) NOT NULL
);''',
                     '''CREATE TABLE personal (
    id_angajat INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nume       VARCHAR2(30) CHECK ( nume REGEXP '^[A-Z][a-z]+\s+[A-Z][a-z]+$' ) NOT NULL,
    id_meserie VARCHAR2(3) CHECK ( id_meserie IN ( 'REC', 'MEC', 'ELE' ) ) NOT NULL,
    vechime    NUMBER(2) CHECK ( vechime BETWEEN 0 AND 40 ),
    salariu    NUMBER(5) CHECK ( salariu >= 2300 ) NOT NULL
);''',
                     '''CREATE TABLE lucraripersonal (
    id_serv_pers        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    lucrari_id_lucrare  NUMBER(3) NOT NULL,
    personal_id_angajat NUMBER(2) NOT NULL,
    FOREIGN KEY(lucrari_id_lucrare) REFERENCES lucrari(id_lucrare),
    FOREIGN KEY(personal_id_angajat) REFERENCES personal(id_angajat)
);''',
                     '''CREATE TABLE masini (
    telefon_proprietar VARCHAR2(10) CHECK(telefon_proprietar REGEXP '^07[0-9]+$' AND length(telefon_proprietar)=10) NOT NULL,
    detaliimasini_nr_inmatriculare VARCHAR2(10) PRIMARY KEY NOT NULL,
    FOREIGN KEY(detaliimasini_nr_inmatriculare) REFERENCES detaliimasini(nr_inmatriculare)
);''',
                     '''CREATE TABLE revizii (
    id_revizie INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    lucraripersonal_id_serv_pers NUMBER(3) NOT NULL,
    masini_nr_inmatriculare VARCHAR2(10) NOT NULL,
    data_efectuarii DATE CHECK ( data_efectuarii > '01-JAN-2021' ) NOT NULL,
    tip_revizie VARCHAR2(17) CHECK ( tip_revizie IN ( 'ITP', 'REPARATIE', 'REVIZIE PERIODICA' ) ) NOT NULL,
    durata NUMBER(4, 2) CHECK ( durata > 0 ) NOT NULL,
    pret FLOAT,
    FOREIGN KEY(lucraripersonal_id_serv_pers) REFERENCES lucraripersonal(id_serv_pers),
    FOREIGN KEY(masini_nr_inmatriculare) REFERENCES masini(detaliimasini_nr_inmatriculare)
);'''
                     ]
    INSERT_SCRIPT = ["INSERT INTO detaliimasini VALUES ('B 303 ABC', 'Dacia Sandero', 2013, '3KD82KP93N715TC90', 1);",
                     "INSERT INTO detaliimasini VALUES ('CT 33 DND', 'Ford Mustang', 2015, 'JR92L10FN381927H2', 2);",
                     "INSERT INTO detaliimasini VALUES ('DJ 99 ZZZ', 'Toyota Supra', 1995, '3J2MKZGQU7291728J3', 1);",
                     "INSERT INTO detaliimasini VALUES ('TM 11 BOS', 'Mercedes-Benz GLC', 2021, '67GH2391OE38312U7', 0);",
                     "INSERT INTO detaliimasini VALUES ('B 999 KYS', 'Lamborghini Urus', 2012, 'YRL2RHL2LHRLH2GGE', 0);",

                     "INSERT INTO lucrari (nume_lucrare, id_meserie, cost_ora) VALUES ('manipulare vehicul', 'REC', 50);",
                     "INSERT INTO lucrari (nume_lucrare, id_meserie, cost_ora) VALUES ('curatare interior', 'REC', 50);",
                     "INSERT INTO lucrari (nume_lucrare, id_meserie, cost_ora) VALUES ('curatare exterior', 'REC', 25);",
                     "INSERT INTO lucrari (nume_lucrare, id_meserie, cost_ora) VALUES ('revizie generala', 'MEC', 250);",
                     "INSERT INTO lucrari (nume_lucrare, id_meserie, cost_ora) VALUES ('efectuare itp', 'MEC', 150);",
                     "INSERT INTO lucrari (nume_lucrare, id_meserie, cost_ora) VALUES ('reparatie caroserie', 'MEC', 400);",
                     "INSERT INTO lucrari (nume_lucrare, id_meserie, cost_ora) VALUES ('schimb discuri frana', 'MEC', 200);",
                     "INSERT INTO lucrari (nume_lucrare, id_meserie, cost_ora) VALUES ('schimb anvelope', 'MEC', 300);",
                     "INSERT INTO lucrari (nume_lucrare, id_meserie, cost_ora) VALUES ('echilibrare roti', 'MEC', 200);",
                     "INSERT INTO lucrari (nume_lucrare, id_meserie, cost_ora) VALUES ('schimb bujii', 'MEC', 40);",
                     "INSERT INTO lucrari (nume_lucrare, id_meserie, cost_ora) VALUES ('schimb ulei + filtru', 'MEC', 200);",
                     "INSERT INTO lucrari (nume_lucrare, id_meserie, cost_ora) VALUES ('schimb distributie', 'MEC', 600);",
                     "INSERT INTO lucrari (nume_lucrare, id_meserie, cost_ora) VALUES ('efectuare diagnoza', 'ELE', 150);",
                     "INSERT INTO lucrari (nume_lucrare, id_meserie, cost_ora) VALUES ('depanare sistem inchidere', 'ELE', 500);",
                     "INSERT INTO lucrari (nume_lucrare, id_meserie, cost_ora) VALUES ('depanare panou bord', 'ELE', 700);",
                     "INSERT INTO lucrari (nume_lucrare, id_meserie, cost_ora) VALUES ('depanare sistem iluminat', 'ELE', 400);",

                     "INSERT INTO personal (nume, id_meserie, salariu) VALUES ('George Georgescu', 'REC', 4500);",
                     "INSERT INTO personal (nume, id_meserie, vechime, salariu) VALUES ('Ion Dorobantu', 'MEC', 20, 8000);",
                     "INSERT INTO personal (nume, id_meserie, vechime, salariu) VALUES ('Grigore Vasiliu', 'MEC', 5, 5500);",
                     "INSERT INTO personal (nume, id_meserie, salariu) VALUES ('Toader Daniel', 'ELE', 5000);",
                     "INSERT INTO personal (nume, id_meserie, vechime, salariu) VALUES ('Petrica Ionescu', 'ELE', 15, 6300);",

                     '''INSERT INTO lucraripersonal (lucrari_id_lucrare, personal_id_angajat) 
    SELECT lucrari.id_lucrare, personal.id_angajat FROM personal, lucrari WHERE personal.id_meserie = lucrari.id_meserie;''',

                     "INSERT INTO masini VALUES ('0712345678','B 303 ABC');",
                     "INSERT INTO masini VALUES ('0711223344','CT 33 DND');",
                     "INSERT INTO masini VALUES ('0787654321','DJ 99 ZZZ');",
                     "INSERT INTO masini VALUES ('0711223344','TM 11 BOS');",
                     "INSERT INTO masini VALUES ('0707070707','B 999 KYS');",

                     "INSERT INTO revizii(lucraripersonal_id_serv_pers,masini_nr_inmatriculare, data_efectuarii, tip_revizie,durata) VALUES (2, 'DJ 99 ZZZ', '08-JUL-2021', 'REVIZIE PERIODICA', 0.50);",
                     "INSERT INTO revizii(lucraripersonal_id_serv_pers,masini_nr_inmatriculare, data_efectuarii, tip_revizie,durata) VALUES (14, 'DJ 99 ZZZ', '08-JUL-2021', 'REVIZIE PERIODICA', 1);",
                     "INSERT INTO revizii(lucraripersonal_id_serv_pers,masini_nr_inmatriculare, data_efectuarii, tip_revizie,durata) VALUES (11, 'DJ 99 ZZZ', '08-JUL-2021', 'REVIZIE PERIODICA', 4);",
                     "INSERT INTO revizii(lucraripersonal_id_serv_pers,masini_nr_inmatriculare, data_efectuarii, tip_revizie,durata) VALUES (6, 'B 999 KYS', '11-SEP-2021', 'ITP', 1);",
                     "SAVEPOINT U;",
                     '''UPDATE detaliimasini SET valabilitate_itp = (SELECT
    CASE
    WHEN SUBSTR(DATE('now'),0,5) - an_fabricatie < 2 THEN 3
    WHEN SUBSTR(DATE('now'),0,5) - an_fabricatie BETWEEN 3 AND 12 THEN 2
    ELSE 1
    END
    FROM detaliimasini
    WHERE nr_inmatriculare = 'B 999 KYS')
    WHERE nr_inmatriculare = 'B 999 KYS';''',
                     "COMMIT;",
                     "INSERT INTO revizii(lucraripersonal_id_serv_pers,masini_nr_inmatriculare, data_efectuarii, tip_revizie,durata) VALUES (1, 'B 303 ABC', '18-SEP-2021', 'REVIZIE PERIODICA', 1);",
                     "INSERT INTO revizii(lucraripersonal_id_serv_pers,masini_nr_inmatriculare, data_efectuarii, tip_revizie,durata) VALUES (18, 'B 303 ABC', '18-SEP-2021', 'REVIZIE PERIODICA', 1);",
                     "INSERT INTO revizii(lucraripersonal_id_serv_pers,masini_nr_inmatriculare, data_efectuarii, tip_revizie,durata) VALUES (17, 'CT 33 DND', '18-SEP-2021', 'REPARATIE', 1);",
                     "INSERT INTO revizii(lucraripersonal_id_serv_pers,masini_nr_inmatriculare, data_efectuarii, tip_revizie,durata) VALUES (19, 'CT 33 DND', '18-SEP-2021', 'REPARATIE', 1);",
                     "INSERT INTO revizii(lucraripersonal_id_serv_pers,masini_nr_inmatriculare, data_efectuarii, tip_revizie,durata) VALUES (8, 'B 999 KYS', '01-OCT-2021', 'REPARATIE', 14);",
                     "INSERT INTO revizii(lucraripersonal_id_serv_pers,masini_nr_inmatriculare, data_efectuarii, tip_revizie,durata) VALUES (29, 'B 999 KYS', '01-OCT-2021', 'REPARATIE', 3);",
                     "INSERT INTO revizii(lucraripersonal_id_serv_pers,masini_nr_inmatriculare, data_efectuarii, tip_revizie,durata) VALUES (7, 'TM 11 BOS', '27-OCT-2021', 'ITP', 1);",
                     "SAVEPOINT U;",
                     '''UPDATE detaliimasini SET valabilitate_itp = (SELECT
    CASE
    WHEN SUBSTR(DATE('now'),0,5) - an_fabricatie < 2 THEN 3
    WHEN SUBSTR(DATE('now'),0,5) - an_fabricatie BETWEEN 3 AND 12 THEN 2
    ELSE 1
    END
    FROM detaliimasini
    WHERE nr_inmatriculare = 'TM 11 BOS')
    WHERE nr_inmatriculare = 'TM 11 BOS';''',
                     "COMMIT;",
                     "INSERT INTO revizii(lucraripersonal_id_serv_pers,masini_nr_inmatriculare, data_efectuarii, tip_revizie,durata) VALUES (10, 'DJ 99 ZZZ', '03-NOV-2021', 'REVIZIE PERIODICA', 2);",
                     "INSERT INTO revizii(lucraripersonal_id_serv_pers,masini_nr_inmatriculare, data_efectuarii, tip_revizie,durata) VALUES (16, 'DJ 99 ZZZ', '03-NOV-2021', 'REVIZIE PERIODICA', 1.5);",
                     "INSERT INTO revizii(lucraripersonal_id_serv_pers,masini_nr_inmatriculare, data_efectuarii, tip_revizie,durata) VALUES (2, 'CT 33 DND', '07-NOV-2021', 'REVIZIE PERIODICA', 1);",
                     "INSERT INTO revizii(lucraripersonal_id_serv_pers,masini_nr_inmatriculare, data_efectuarii, tip_revizie,durata) VALUES (22, 'CT 33 DND', '07-NOV-2021', 'REVIZIE PERIODICA', 1);"
                     ]

    def __init__(self):
        with sqlite3.connect(DATABASE_PATH) as db:
            db.create_function("REGEXP", 2, regex)
            cursor = db.cursor()
            for cmd in self.CREATE_SCRIPT:
                cursor.execute(cmd)
            for cmd in self.INSERT_SCRIPT:
                cursor.execute(cmd)
            cursor.close()


if __name__ == '__main__':
    dataBase = DataBase()
