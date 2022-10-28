from sqlite3 import connect
from requests import get
from bs4 import BeautifulSoup
from sys import argv

connection = connect(argv[2])
cursor = connection.cursor()

cursor.execute(
	"""
	CREATE TABLE IF NOT EXISTS 'channel' (
		id TEXT PRIMARY KEY,
		title TEXT,
		description TEXT NULLABLE
	)
	"""
	)

cursor.execute(
	"""
	CREATE TABLE IF NOT EXISTS 'post' (
		id INTEGER PRIMARY KEY,
		channel TEXT REFERENCES channel(id),
		text TEXT
	)
	"""
	)

# GET CHANNEL INFO BLOCK

bs = BeautifulSoup(get("https://t.me/%s" % (argv[1])).content, 'html.parser')

title = list(filter(lambda x: x.has_attr('class') and "tgme_page_title" \
	in x['class'], bs.find_all('div')))[0].get_text().strip()

description = list(filter(lambda x: x.has_attr('class') \
	and "tgme_page_description" in x['class'], \
	bs.find_all('div')))[0].get_text().strip()  # Here is a bs4's '\n' oddity.

cursor.execute("INSERT INTO channel VALUES (\'%s\', \'%s\', \'%s\')"
	% (argv[1], title, description))
connection.commit()
