from flask import Flask, jsonify, request
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB connection using Atlas
MONGO_URI = os.getenv("MONGO_URI")  # Get MongoDB URI from environment variables
client = MongoClient(MONGO_URI)
db = client["education_db"]

# Collections
colleges_collection = db["colleges"]
users_collection = db["users"]  # New collection for storing user details

# Insert sample data (only if the colleges collection is empty)
if colleges_collection.count_documents({}) == 0:
    sample_colleges = [
        {"name": "Harvard University", "location": "Cambridge, MA", "rank": 1},
        {"name": "Stanford University", "location": "Stanford, CA", "rank": 2},
        {"name": "MIT", "location": "Cambridge, MA", "rank": 3},
        {"name": "University of Oxford", "location": "Oxford, UK", "rank": 4},
    ]
    colleges_collection.insert_many(sample_colleges)
    print("Inserted sample data into colleges collection")
else:
    print("Colleges data already exists")

@app.route("/colleges", methods=["GET"])
def get_colleges():
    """Fetch and return the list of colleges."""
    colleges = list(colleges_collection.find({}, {"_id": 0}))  # Exclude the MongoDB `_id` field
    return jsonify(colleges)

@app.route("/add_user", methods=["POST"])
def add_user():
    """Add a new user with their selected college to the database."""
    data = request.get_json()  # Get JSON data from Unity or the frontend
    required_fields = ["name", "age", "roll_no", "selected_college"]
    
    # Validate the input data
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Invalid data. Please provide 'name', 'age', 'roll_no', and 'selected_college'."}), 400
    
    # Insert the new user document into the users collection
    users_collection.insert_one(data)
    return jsonify({"message": "User data added successfully!"}), 201

@app.route("/users", methods=["GET"])
def get_users():
    """Fetch and return the list of all users."""
    users = list(users_collection.find({}, {"_id": 0}))  # Exclude the MongoDB `_id` field
    return jsonify(users)

if __name__ == "__main__":
    # Ensure the app binds to the correct port
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5001)))