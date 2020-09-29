from flask import Flask, render_template, request, redirect
import random
import sqlite3
from os import path

app = Flask(__name__)

myHost = '127.0.0.1'
massA = ['0', '1', '2', '3', '4', '5',
       '6', '7', '8', '9', 'a', 'b',
       'c', 'd', 'e', 'f', 'g', 'h',
       'i', 'j', 'k', 'l', 'm', 'n',
       'o', 'p', 'q', 'r', 's', 't',
       'w', 'v', 'x', 'y', 'z', 'A',
       'B', 'C', 'D', 'E', 'F', 'G',
       'H', 'I', 'J', 'K', 'L', 'M',
       'N', 'O', 'P', 'Q', 'R', 'S',
       'T', 'W', 'V', 'X', 'Y', 'Z']


def createTable():
    with sqlite3.connect('linksData.db') as connect:
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS links
                       (shortlink TEXT NOT NULL PRIMARY KEY, link TEXT NOT NULL)
                       WITHOUT ROWID""")
        connect.commit()

def updateTable(shortlink, link):
    with sqlite3.connect('linksData.db') as connect:
        cursor = connect.cursor()
        cursor.execute("""INSERT INTO links VALUES (?, ?)""", (shortlink, link))
        connect.commit()

def getFromTable(shortlink):
    with sqlite3.connect('linksData.db') as connect:
        cursor = connect.cursor()
        cursor.execute("""SELECT * FROM links WHERE shortlink=?""", (shortlink,))
        link = cursor.fetchone()
        if link is not None:
            link = link[1]
        else:
            link = 'none.NONE'
        return link

def findSame(link):
    with sqlite3.connect('linksData.db') as connect:
        cursor = connect.cursor()
        cursor.execute("""SELECT * FROM links WHERE link=?""", (link,))
        shortlink = cursor.fetchone()
        if shortlink is not None:
            shortlink = shortlink[0]
        else:
            shortlink = 'none.NONE'
        return shortlink

def generateHASH():
    peremen = ''
    for i in range(7):
        rand = random.randint(0, len(massA)-1)
        peremen += massA[rand]
    return peremen


def generateNew(link):
    if 'https://' not in link or 'http://' not in link:
        link = 'http://' + link
    shortLink = findSame(link)
    if shortLink != 'none.NONE':
        return shortLink
    link_out = myHost + '/' + generateHASH()
    updateTable(link_out, link)
    return link_out


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('main.html')
    if request.method == 'POST':
        link = request.form.get('link_in') # name / id
        link_out = generateNew(link)
        return render_template('main.html', abc=link_out)



@app.route('/<link>', methods = ['GET'], strict_slashes=False)
def start(link):
    if link == 'favicon.ico':
        return redirect('http://' + myHost)
    normalLink = getFromTable(myHost + '/' + link)
    if normalLink == 'none.NONE':
        return redirect('http://' + myHost)
    return redirect(normalLink)

if __name__ == "__main__":
    createTable()
    app.run(host = myHost, port = '80', debug = False)
