from flask import Flask, request, jsonify
import hashlib
from dotenv import load_dotenv
import os
import pymongo
load_dotenv()
DB_LINK = os.getenv('DB_LINK')
client = pymongo.MongoClient(DB_LINK)
db = client.susanta
userCollection = db['users']
app = Flask(__name__)
@app.route('/')
def home():
    return "Hello World"
@app.route('/save', methods=['POST'])
def save():
    try:
        data = request.json

        if not data:
            return jsonify({"success": False, "error": "No JSON received"}), 400

        if 'email' not in data or 'password' not in data:
            return jsonify({"success": False, "error": "Missing fields"}), 400

        user = userCollection.find_one({"email": data['email']})

        # hash password
        data['password'] = hashlib.md5(data['password'].encode()).hexdigest()

        if user:
            userCollection.update_one(
                {"email": data['email']},
                {"$set": data}
            )
            data['_id'] = str(user['_id'])
        else:
            result = userCollection.insert_one(data)
            data['_id'] = str(result.inserted_id)

        return jsonify({
            "success": True,
            "data": data
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
@app.route('/view')
def view():
    users = list(userCollection.find())
    # convert ObjectId to string
    for user in users:
        user['_id'] = str(user['_id'])
    return users
if __name__ == "__main__":
    app.run(port=3001,host='0.0.0.0',debug=True)