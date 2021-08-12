import base64
import io
import os
import cv2
import numpy as np
from flask import Flask, request, render_template
from flask_restful import Api, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from PIL import Image

#load model
from keras.models import load_model

model = load_model('smart_class.h5')
print("Model loaded successfully")



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



#Function to normalize image (make it pixel values range from 0-1 for easier processing)
def normalize(data):
    shape = data.shape
    normalized_data = np.reshape(data, (shape[0], -1))
    normalized_data = normalized_data.astype('float32') /255.
    
    return np.reshape(normalized_data, shape)
    

# Function to Preprocess the images for CNN modelling
def preprocess(img):
    image = cv2.resize(img, (270,540))
    
    #convert image to numpy array
    image = np.asarray(image, dtype=np.uint8).reshape((1,270,540,3))
    image = normalize(image)
    
    return image
    

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
            
            #preprocess the image before sending to model
            img = prepocess(image)
            
            #send to model and predict class
            pred = model.predict([img])
            final_pred = np.argmax(pred)
            
            if final_pred == 0:
                output = 'Attentive'
            elif final_pred == 1:
                output = 'Not Attentive'
            else:
                output = 'Sleepy'
            
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
    # TODO: Return to the user a URL to download the image
    return render_template('display.html', filename=img.name)


@app.route("/report", methods=['GET'])
def send_report():
    # TODO: Create a query that goes through the db and counts the number of times different classifications appear
    attentive_score = 180
    inattentive_score = 95
    sleeping_score = 12

    return {
        "attentive": attentive_score,
        "inattentive": inattentive_score,
        "sleeping": sleeping_score,
    }


if __name__ == '__main__':
    app.run(debug=True)
