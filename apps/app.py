'''
    SAMPLE DATABASE AS A SERVICE API

    Register a user with username and password

    Login a user with username and password

    A user gets 10 coins by default when registration completed.

    Every time a user logs in 1 coin is used up.

    Once all coins are used up the registered user won't be able to log in.
'''

from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource, reqparse
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)
db_client = MongoClient("mongodb://database:27017")
database = db_client["Webapp"]
users = database["Users"]


class ParseData:
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help='The username field is required'
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help='The password field is required'
    )

def user_verification(username, password):
    
    if users.find_one({"Username":username}):
        hashed_password = users.find_one({
            "Username":username
        })["Password"]
        if bcrypt.hashpw(password.encode('utf-8'), hashed_password) == hashed_password:
            return True
        else:
            return False

    else:
        return False

def coins_counter(username):

    coins = users.find_one({
        "Username":username
    })["Coins"]

    return coins



class RegisterUser(Resource):
    
    def post(self):
        posted_data = ParseData.parser.parse_args()
        username = posted_data['username']
        password = posted_data['password']

        # Check whether a user with the username already exists
        if users.find_one({"Username":username}):
            message = username + " already exists"
            response = jsonify({"message": message})
            resp = make_response(response)
            resp.headers["Content-Type"] = "application/json"
            resp.status_code = 422
            return resp
        
        # Encode and encrypt the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Register the user with default coins
        users.insert_one({
            "Username":username,
            "Password":hashed_password,
            "Coins":10
        })

        message = "User " + username + " successfully registered"
        response = jsonify({"message":message})
        resp = make_response(response)
        resp.headers["Content-Type"] = "application/json"
        resp.status_code = 200
        return resp



class LoginUser(Resource):

    def post(self):
        posted_data = ParseData.parser.parse_args()
        username = posted_data["username"]
        password = posted_data["password"]

        # Verify the username and password
        verified = user_verification(username, password)
        
        if not verified:

            message = "Invalid username or password"
            response = jsonify({"message": message})
            resp = make_response(response)
            resp.headers['Content-Type'] = 'application/json'
            resp.status_code = 422
            return resp
        
        else:
            # Check the coins remaining
            coins_remaining = coins_counter(username)
            if coins_remaining <= 0:
                message = "User out of coins. Trial access expired"
                response = jsonify({"message":message})
                resp = make_response(response)
                resp.headers["Content-Type"] = "application/json"
                resp.status_code = 402
                return resp
            else:
                # Remove 1 coin for Logging In
                users.update({
                    "Username":username
                },{
                    "$set":{
                        "Coins":coins_remaining - 1
                    }
                })
                message = "User Logged In"
                
                response = jsonify({
                    "message":message,
                    "account_access_chance_remaining":coins_remaining - 1
                })
                resp = make_response(response)
                resp.headers['Content-Type'] = 'application/json'
                resp.status_code = 200
                return resp





api.add_resource(RegisterUser, '/register')
api.add_resource(LoginUser, '/login')

if __name__ == '__main__':
    app.run(host="0.0.0.0")


