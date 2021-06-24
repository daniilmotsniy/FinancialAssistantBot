from flask import Flask
from backend.config import Configuration
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config.from_object(Configuration)
CORS(app)
