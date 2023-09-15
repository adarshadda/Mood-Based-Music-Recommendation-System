from flask import Flask, request, jsonify, render_template
from modules import Module  # Import your custom module for audio processing
import os
import uuid

app = Flask(__name__)

# Define the directory where temporary audio files will be stored
TEMP_AUDIO_DIR = 'temp'

# Check if the "temp" directory exists, and if not, create it
if not os.path.exists(TEMP_AUDIO_DIR):
    os.makedirs(TEMP_AUDIO_DIR)

# Serve the index.html page when the root URL is accessed
@app.route('/')
def home():
    return render_template('index.html')

# Define a route to handle audio recording and processing
@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        # Check if the 'audio' file is present in the request
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']

        # Check if the file is empty
        if audio_file.filename == '':
            return jsonify({'error': 'Empty audio file provided'}), 400

        # Generate a unique filename using UUID
        uuid_filename = f'{str(uuid.uuid4())}.mp3'
        filename = os.path.join(TEMP_AUDIO_DIR, uuid_filename)
        audio_file.save(filename)

        # Now, call the Module.predict method with the UUID filename
        emotion = Module.predict(uuid_filename)

        # Return the emotion prediction as a response
        response = {'emotion': emotion}
        return jsonify(response), 200

    except Exception as e:
        # Handle any errors or exceptions
        response = {'error': str(e)}
        return jsonify(response), 500

# Define a route to save the recorded audio in the "temp" directory
@app.route('/save_audio', methods=['POST'])
def save_audio():
    try:
        audio_file = request.files['audio']

        # Check if the 'audio' file is present in the request
        if audio_file is None:
            return jsonify({'error': 'No audio file provided'}), 400

        # Generate a unique filename using UUID
        uuid_filename = f'{str(uuid.uuid4())}.mp3'
        filename = os.path.join(TEMP_AUDIO_DIR, uuid_filename)
        audio_file.save(filename)

        # Return a success response
        response = {'message': 'Audio file saved successfully'}
        return jsonify(response), 200

    except Exception as e:
        # Handle any errors or exceptions
        response = {'error': str(e)}
        return jsonify(response), 500

if __name__ == '__main__':
    app.run(debug=True)
