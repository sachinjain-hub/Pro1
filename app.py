from flask import Flask, request, jsonify
import os
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    features = [data['area'], data['bedrooms'], data['bathrooms'], data['stories'],
                data['mainroad'], data['guestroom'], data['basement'],
                data['hotwaterheating'], data['airconditioning'],
                data['parking'], data['prefarea'], data['furnishingstatus']]
    
    prediction = model.predict([np.array(features)])
    return jsonify({'predicted_price': int(prediction[0])})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # This is required for Render
    app.run(host='0.0.0.0', port=port)
