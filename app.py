from flask import Flask, render_template, redirect, url_for
from entries import entries

app = Flask(__name__)

app.config.from_object(__name__)

@app.route('/')
def show_entries():
    return render_template('entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    return redirect(url_for('show_entries'))
