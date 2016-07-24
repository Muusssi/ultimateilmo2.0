import psycopg2
import datetime

class Database(object):

    def __init__(self, pw):
        self.dsn = "dbname='ilmo' user='ultimate_secretary' host='localhost' password='%s'" % (pw, )

    # def _cursor(self):
    #     return self._conn.cursor()

    # def _close_connection(self):
    #     self._conn.close()

    # def _commit(self):
    #     self._conn.commit()

    def reconnect(self):
        self._close_connection()
        self._connect()

    def _query(self, sql, values):
        with psycopg2.connect(self.dsn) as con:
            with con.cursor() as cur:
                cur.execute(sql, values)
                rows = cur.fetchall()
        if not rows:
            rows = []
        return rows

    def _insert(self, sql, values):
        with psycopg2.connect(self.dsn) as con:
            with con.cursor() as cur:
                cur.execute(sql, values)

    def people(self):
        people = []
        query = 'SELECT name, id FROM person ORDER BY name'
        for name, person_id in self._query(query, None):
            people.append(Person(name, person_id))
        return people

    def person(self, person_id):
        person = None
        query = ("SELECT name, id FROM person WHERE id=%s")
        for name, person_id in self._query(query, (person_id, )):
            person = Person(name, person_id)
        return person

    def answers(self):
        query = ('SELECT p.name, a.notes, a.time01, a.time02, a.time03, a.time04, a.time05, a.time06, '
                 'a.time07, a.time08, a.time09, a.time10, a.time11, a.time12 '
                 'FROM person as p JOIN answer as a ON p.id=a.person_id '
                 'WHERE EXTRACT(WEEK FROM now()) = EXTRACT(WEEK FROM a.given_on) '
                 'AND EXTRACT(YEAR FROM now()) = EXTRACT(YEAR FROM a.given_on) '
                 'ORDER BY p.name, a.given_on DESC;')
        answers = []
        last_name = ''
        for row in self._query(query, None):
            name = row[0]
            if name != last_name:
                last_name = name
                answers.append(Answer(row))
        return answers

    def answer(self, person_id):
        query = ('SELECT p.name, a.notes, a.time01, a.time02, a.time03, a.time04, a.time05, a.time06, '
                 'a.time07, a.time08, a.time09, a.time10, a.time11, a.time12 '
                 'FROM person as p JOIN answer as a ON p.id=a.person_id '
                 'WHERE EXTRACT(WEEK FROM now()) = EXTRACT(WEEK FROM a.given_on) '
                 'AND EXTRACT(YEAR FROM now()) = EXTRACT(YEAR FROM a.given_on) '
                 'AND p.id=%s '
                 'ORDER BY a.given_on DESC '
                 'LIMIT 1')
        answer = None
        for row in self._query(query, (person_id, )):
            answer = Answer(row)
        return answer

    def register_answer(self, person_id, notes, times):
        query = ('INSERT INTO answer(person_id, notes, time01, time02, time03, time04, time05, time06, '
                 'time07, time08, time09, time10, time11, time12) '
                 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
        self._insert(query, (person_id, notes, times[0], times[1], times[2], times[3], times[4],
                       times[5], times[6], times[7], times[8], times[9], times[10], times[11]))

    def register_player(self, name):
        query = ('INSERT INTO person(name) VALUES(%s)')
        self._insert(query, (name, ))


class Answer(object):
    def __init__(self, data):
        self.name = data[0]
        self.notes = data[1]
        self.times = data[2:]

class Person(object):
    def __init__(self, name, person_id):
        self.name = name
        self.id = person_id




if __name__ == '__main__':
    pass

