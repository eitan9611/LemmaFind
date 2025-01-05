import find_values
import heb_pipe_dicta
import find_in_text
import json
import sys
import io
import os
import merge_dicts

from pymongo import MongoClient
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()  # Load variables from .env file

# Ensures we deliver as UTF-8 to get it parsed well in node.js
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)

input_file = "input.txt"
text_file = "shmona01.pdf"
PROCESS = True  # True when URL is new and I want to make new data into roots
check = False  # if you change that so also change the word document

def main_logic(word):
    # Set up environment variables
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_cluster = os.getenv('DB_CLUSTER')
    db_name = os.getenv('DB_NAME')
    app_name = os.getenv('DB_APPNAME')
    connection_string = (
        f"mongodb+srv://{db_user}:{db_password}@{db_cluster}/{db_name}"
        f"?retryWrites=true&w=majority&appName={app_name}"
    )
    try:
        # Connect to MongoDB
        client = MongoClient(connection_string)
        db = client[db_name]
        roots_collection = db["Roots"]
    except Exception as e:
        return {"error": f"Connection failed: {str(e)}"}

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if PROCESS:
        dict = heb_pipe_dicta.process_roots_memory(input_file)
        merge_dicts.merge_dict_to_mongodb(roots_collection, dict)

    values = find_values.get_values_from_dict_inMongo(roots_collection, word)
    result = find_in_text.find_sentences_with_values(text_file, values)
    return result

@app.route('/run-main', methods=['POST'])
def run_main():
    word = request.json.get('word')
    if not word:
        return jsonify({'error': 'No word provided'}), 400

    result = main_logic(word)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
