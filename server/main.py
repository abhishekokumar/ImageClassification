from flask import Flask, request, jsonify
import util
import os

app = Flask(__name__)
@app.route('/classify_image', methods=['GET', 'POST'])
def classify_image():
    ''' A route to return classification result of image'''
    image_data = request.form['image_data']
    print('***************************')
    print(image_data)
    print('***************************')
    response = jsonify(util.classify_image(image_data))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    ''' Main function to start the server'''
    print("Starting Python Flask Server For Sports Celebrity Image Classification")
    util.load_saved_artifacts()
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))

    # For Docker, run on 0.0.0.0 to allow external connections
    # But for single-container setup with nginx, use 127.0.0.1
    #host = '127.0.0.1'  # Internal to container, nginx will proxy
    host = '0.0.0.0'
    print(f"🏠 House Price Prediction API starting on {host}:{port}")
    app.run(host=host, port=port, debug=False)  # debug=False for production