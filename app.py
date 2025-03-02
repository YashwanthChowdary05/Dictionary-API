from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    word = request.args.get('word', '').strip()
    if not word:
        return jsonify({"error": "No word provided"}), 400

    response = requests.get(API_URL + word)

    if response.status_code == 200:
        data = response.json()
        print("Full API Response:", data)

        formatted_result = []
        for entry in data:
            word_info = {
                "word": entry.get("word", ""),
                "phonetic": entry.get("phonetic", ""),
                "phonetics": entry.get("phonetics", []),
                "meanings": {}
            }
            for meaning in entry.get("meanings", []):
                pos = meaning.get("partOfSpeech", "")
                if pos not in word_info["meanings"]:
                    word_info["meanings"][pos] = []
                for definition in meaning.get("definitions", []):
                    word_info["meanings"][pos].append({
                        "definition": definition.get("definition", ""),
                        "synonyms": definition.get("synonyms", []),
                        "antonyms": definition.get("antonyms", []),
                        "example": definition.get("example", "")
                    })
            
            # Convert meanings back to list format
            word_info["meanings"] = [
                {"partOfSpeech": pos, "definitions": defs} for pos, defs in word_info["meanings"].items()
            ]
            
            formatted_result.append(word_info)

        return jsonify(formatted_result)
    
    else:
        return jsonify({"error": "Word not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
