from flask import Flask, render_template
from entries import entries

app = Flask(__name__)

app.config.from_object(__name__)

@app.route('/')
def hello_world():
    for entry in entries:
        print(entry)
    return render_template('entries.html', entries=entries)
