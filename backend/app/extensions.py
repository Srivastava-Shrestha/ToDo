from flask_cors import CORS
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
security = Security()
cors = CORS()
