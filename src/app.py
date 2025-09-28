from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Fase II Iniciada - Construccion del Back End"})

if __name__ == '__main__':
    app.run(debug = True)