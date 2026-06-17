#!/usr/bin/python3
"""Starts a Flask web application for listing States and State detail."""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Display an HTML page with a sorted list of all State objects."""
    all_states = sorted(storage.all(State).values(), key=lambda s: s.name)
    return render_template('9-states.html', states=all_states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """Display an HTML page with a specific State and its Cities."""
    state = storage.all(State).get('State.{}'.format(id))
    return render_template('9-states.html', state=state)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy session after each request."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
