"""

"""
from flask import Flask

from shared.infrastructure.database import init_db

app = Flask(__name__)

init_db()

if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)