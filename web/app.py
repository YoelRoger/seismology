import os
from dotenv import load_dotenv
from flask import Flask


app = Flask(__name__)

load_dotenv()

if __name__ == '__main__':
    app.run(debug=True, port = os.getenv('PORT'))