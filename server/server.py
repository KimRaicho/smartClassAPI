from flask import Flask, request, jsonify
from PIL import Image

app = Flask(__name__)


@app.route('/test/connection', methods=['POST'])
def test():
    file = request.files['image']
    img = Image.open(file.stream)

    file.save('img.jpg')

    return jsonify({'message': 'success', 'size': [img.width, img.height]})


if __name__ == '__main__':
    app.run(debug=True)
