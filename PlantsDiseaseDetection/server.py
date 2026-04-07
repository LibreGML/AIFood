from flask import Flask, request, jsonify, render_template
from transformers import pipeline
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # 正确的位置是在创建app之后

@app.route('/infer', methods=['POST'])
def infer():
    try:
        pipe = pipeline("image-classification", model="./plant_disease_model")
        result = pipe(request.json['image'])
        if result:
            return jsonify({'status': 'success', 'error': None, 'result': result})
        else:
            return jsonify({'status': 'failed', 'error': 'No result', 'result': None})
    except Exception as e:
        return jsonify({'status': 'failed', 'error': str(e), 'result': None})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)