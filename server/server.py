import base64
import io
import os
from flask import Flask, request, render_template
from flask_restful import Api, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
api = Api(app)  # Wrap our app in an API
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # max image upload size shouldn't be more than 16MB
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# Image Model to store images sent to the server
class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text, nullable=False)  # Data to render the pic in browser
    name = db.Column(db.Text, nullable=False)
    # TODO: Add field for result from Model

    def __repr__(self):
        return f"Image (ID: {self.id} Name: {self.name} Data: {self.image})"


# db.create_all()


def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic


# Function to help validate that the file uploaded by the user is indeed an image.
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=['POST'])
def upload_image():
    uploaded_file = request.files['picture']

    if not uploaded_file:
        abort(400, message="No picture uploaded!")

    filename = secure_filename(uploaded_file.filename)

    if allowed_file(filename):
        img = ImageModel.query.filter_by(name=filename).first()
        if not img:
            print("Now reading image data")
            data = uploaded_file.read()
            if not filename or not data:
                abort(400, message="Bad upload!")
            render_file = render_picture(data)
            # Add to the database the name of the image
            image = ImageModel(image=render_file, name=filename)
            db.session.add(image)
            db.session.commit()
            # TODO: Place line that sends image to model to get classification result
            # Save the image in our upload folder
            img = Image.open(io.BytesIO(data))
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f"Image uploaded and stored: ({image.name})", 201
        else:
            return f"Image already exists in database", 400
    else:
        return f"Allowed image types are -> png, jpg, jpeg", 400


@app.route("/image/<int:image_id>")
def retrieve(image_id):
    img = ImageModel.query.filter_by(id=image_id).first()
    if not img:
        return render_template('display.html', filename=None), 404
    # redirect(url_for('static', filename='uploads/' + img.name), code=301)
    # TODO: Return to the user a json dict that has ID of image and it's name and the respective classification result
    return render_template('display.html', filename=img.name)


if __name__ == '__main__':
    app.run(debug=True)
