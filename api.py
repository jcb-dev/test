import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)


class Users():
    def initialise_connection():
        conn = sqlite3.connect('./database/dev_jcb.db')
        return conn

    def get_users():
        users = []
        try:
            conn = Users.initialise_connection()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM users")
            rows = cur.fetchall()

            # convert row objects to dictionary
            for i in rows:
                user = {}
                user["first_name"] = i["first_name"]
                user["last_name"] = i["last_name"]
                users.append(user)

        except:
            users = []
        finally:
            conn.close()

        return users

    def insert_user(user):
        try:
            conn = Users.initialise_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (first_name, last_name) VALUES(?,?)",
                        (user['first_name'], user['last_name']))

            conn.commit()
        except:
            conn().rollback()
        finally:
            cur.close()
            conn.close()


class Locations():
    # methods go here
    pass


# api.add_resource(Users, '/users')  # '/users' is our entry point for Users
# # and '/locations' is our entry point
# api.add_resource(Locations, '/locations')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/api/users/add',  methods=['POST'])
def api_add_user():
    user = request.get_json(force=True)
    return jsonify(Users.insert_user(user))


@app.route('/api/users/',  methods=['GET'])
def api_get_users():
    return (Users.get_users())


if __name__ == '__main__':
    app.run()  # run our Flask app
