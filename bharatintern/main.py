from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)
data = pd.read_csv('ParisHousing.xls')
pipe = pickle.load(open("house_pred.pkl", 'rb'))

@app.route('/')
def index():
    sqms = sorted(data['squareMeters'].unique())
    nors = sorted(data['numberOfRooms'].unique())
    hy = sorted(data['hasYard'].unique())
    nB = sorted(data['isNewBuilt'].unique())

    return render_template('index.html', sqms = sqms,nors =nors , hy = hy , nB = nB)

@app.route('/predict', methods=['POST'])
def predict():
    sqms = request.form.get('squareMeters')
    nors = request.form.get('nors')
    hy = request.form.get('hy')
    nB = request.form.get('nB')

    # Create a DataFrame with the input data
    input_data = pd.DataFrame([[sqms, nors, hy, nB]],
                               columns=['squareMeters', 'numberOfRooms', 'hasYard', 'isNewBuilt'])

    print("Input Data:")
    print(input_data)

    # Handle unknown categories in the input data
    for column in input_data.columns:
        unknown_categories = set(input_data[column]) - set(data[column].unique())
        if unknown_categories:
            # Handle unknown categories (e.g., replace with a default value)
            input_data[column] = input_data[column].replace(unknown_categories, data[column].mode()[0])

    print("Processed Input Data:")
    print(input_data)

    # Predict the price
    prediction = lr.predict(input_data)[0]

    return str(prediction)
from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)
data = pd.read_csv('ParisHousing.xls')
pipe = pickle.load(open("house_pred.pkl", 'rb'))

@app.route('/')
def index():
    sqms = sorted(data['squareMeters'].unique())
    nors = sorted(data['numberOfRooms'].unique())
    hy = sorted(data['hasYard'].unique())
    nB = sorted(data['isNewBuilt'].unique())

    return render_template('index.html', sqms = sqms,nors =nors , hy = hy , nB = nB)

@app.route('/predict', methods=['POST'])
def predict():
    sqms = request.form.get('squareMeters')
    nors = request.form.get('nors')
    hy = request.form.get('hy')
    nB = request.form.get('nB')

    # Create a DataFrame with the input data
    input_data = pd.DataFrame([[sqms, nors, hy, nB]],
                               columns=['squareMeters', 'numberOfRooms', 'hasYard', 'isNewBuilt'])

    print("Input Data:")
    print(input_data)

    # # Convert 'baths' column to numeric with errors='coerce'
    # input_data['squareMeters'] = pd.to_numeric(input_data['squareMeters'], errors='coerce')
    input_data['numberOfRooms'] = pd.to_numeric(input_data['numberOfRooms'], errors='coerce')
    # input_data['hasYard'] = pd.to_numeric(input_data['hasYard'], errors='coerce')
    # input_data['isNewBuilt'] = pd.to_numeric(input_data['isNewBuilt'], errors='coerce')

    # Convert input data to numeric types
    input_data = input_data.astype({'squareMeters': int, 'hasYard': int, 'isNewBuilt':int})

    # Handle unknown categories in the input data
    for column in input_data.columns:
        unknown_categories = set(input_data[column]) - set(data[column].unique())
        if unknown_categories:
            print(f"Unknown categories in {column}: {unknown_categories}")
            # Handle unknown categories (e.g., replace with a default value)
            input_data[column] = input_data[column].replace(unknown_categories, data[column].mode()[0])

    print("Processed Input Data:")
    print(input_data)

    # Predict the price
    prediction =pipe.predict(input_data)[0]

    return str(prediction)

if __name__ == "__main__":
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
