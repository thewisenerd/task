from flask import Flask, render_template, request
app = Flask(__name__)

import sqlite3

F_DATABASE = 'app.db'
conn = sqlite3.connect(F_DATABASE)

@app.route("/")
def hello():
	return render_template("index.htm")

@app.route("/search/author")
def search_author():
	q = request.args.get('q')
	s = ""

	if q == None:
		return "missing search parameter q"

	# TODO: SQL injection
	cursor = conn.execute(" select * from books where lower(AUTHOR) like '%" + q + "%'")

	s += "<table>";
	s += "<tr>";
	s += "<td>%s</td>" % ("ID") 
	s += "<td>%s</td>" % ("TITLE") 
	s += "<td>%s</td>" % ("AUTHOR") 
	s += "<td>%s</td>" % ("RESERVED") 
	s += "</tr>"

	for row in cursor:
		s += "<tr> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> </tr>" % (row[0], row[1], row[2], str(bool(row[3])))

	return s


@app.route("/search/title")
def search_title():
	q = request.args.get('q')
	s = ""

	if q == None:
		return "missing search parameter q"

	# TODO: SQL injection
	cursor = conn.execute(" select * from books where lower(NAME) like '%" + q + "%'")

	s += "<table>";
	s += "<tr>";
	s += "<td>%s</td>" % ("ID") 
	s += "<td>%s</td>" % ("TITLE") 
	s += "<td>%s</td>" % ("AUTHOR") 
	s += "<td>%s</td>" % ("RESERVED") 
	s += "</tr>"

	for row in cursor:
		s += "<tr> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> </tr>" % (row[0], row[1], row[2], str(bool(row[3])))

	return s

@app.route("/search/student")
def search_student():
	q = request.args.get('q')
	s = ""

	if q == None:
		return "missing search parameter q"

	# TODO: SQL injection
	cursor = conn.execute(" select * from reserves inner join books on reserves.BOOKID = books.ID where reserves.STUDENTID = %s and RETURNED is null; " % str(q))
	req = cursor.fetchall()

	if len(req) == 0:
		return "no books issued"

	s += "<table>";
	s += "<tr>";
	s += "<td>%s</td>" % ("ID") 
	s += "<td>%s</td>" % ("TITLE") 
	s += "<td>%s</td>" % ("AUTHOR") 
	s += "<td>%s</td>" % ("BORROWED") 
	s += "<td>%s</td>" % ("DUE") 
	s += "</tr>"

	for row in req:
		s += "<tr> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> </tr>" % (row[1], row[7], row[8], row[3], row[4])

	return s



@app.route("/reserve/book")
def reserve_book():
	s_id = request.args.get('sid');
	b_id = request.args.get('bid');

	if s_id == None or b_id == None:
		return "missing student_id (sid) and book_id (bid) parameters";

	# TODO: Fuck, sql injection again. todo: learn flask? 
	cursor = conn.execute("select * from books where ID=" + str(b_id) + ";")
	rec = cursor.fetchone()

	if rec == None:
		return  "book does not exist" 

	if rec[3] == 1:
		return "book already reserved"

	c2 = conn.execute("select * from reserves where STUDENTID = %s and RETURNED is null" % (str(s_id)))
	stu = c2.fetchall()
	# print(stu, len(stu))

	if len(stu) >= 3:
		return "maximum books already reserved for student"

	# TODO: sql injection. meh.
	q1 = "insert into reserves (BOOKID, STUDENTID, BORROWED, DUE) VALUES ( '%s', '%s', date('now'), date('now', '+7 day') )" % (b_id, s_id)
	q2 = "update books set RESERVED = 1 where ID = %s;" % (b_id)

	conn.execute(q1);
	conn.execute(q2);
	conn.commit()

	return "book reserved"

@app.route("/return/book")
def return_book():
	b_id = request.args.get('bid');

	if b_id == None:
		return "missing book_id (bid) parameters";

	# TODO: Fuck, sql injection again. todo: learn flask? 
	cursor = conn.execute("select * from books where ID=" + str(b_id) + ";")
	rec = cursor.fetchone()

	if rec == None:
		return  "book does not exist" 

	if rec[3] == 0:
		return "book not reserved"

	# TODO: sql injection. meh.
	q1 = "update reserves set RETURNED = date('now') where BOOKID = %s and RETURNED is null" % (b_id)
	q2 = "update books set RESERVED = 0 where ID = %s;" % (b_id)

	conn.execute(q1);
	conn.execute(q2);
	conn.commit()

	return "book returned"



def setup_db():
	pass

def setup_tables():
	pass

def setup_server():
	app.run()

def main():
	setup_db()

	setup_tables()

	setup_server()


if __name__ == "__main__":
	main()
