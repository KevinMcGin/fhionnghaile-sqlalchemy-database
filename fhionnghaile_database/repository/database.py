import time
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Database():

    def __init__(
        self,
        app
    ):
        DB_USER = os.environ.get('POSTGRES_USER', 'DB_USER')
        DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'DB_PASS')
        DB_HOST = os.environ.get('DB_HOST', 'localhost')
        # DB_HOST = os.environ.get('DB_HOST', 'host.docker.internal')
        DB_PORT = os.environ.get('DB_PORT', 6432)
        DB_NAME = os.environ.get('POSTGRES_DB', 'testdb')
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
                user=DB_USER,
                passwd=DB_PASS,
                host=DB_HOST,
                port=DB_PORT,
                db=DB_NAME
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.secret_key = 'foobarbaz'
        global db
        db.app = app
        db.init_app(app)

    def setup_database(self):
        dbstatus = False
        dbAttempts = 0
        maxDbAttempts = 25
        print("Waiting for database to start...")
        while dbstatus == False:
            dbAttempts += 1
            if dbAttempts > maxDbAttempts:
                print("Max database start attempts reached. Breaking loop...")
                break
            try:
                print("Trying to start database...")
                db.create_all()
                print("Database started!")
            except BaseException as error:
                print('An exception occurred: {}'.format(error))
                time.sleep(2)
            else:
                dbstatus = True

