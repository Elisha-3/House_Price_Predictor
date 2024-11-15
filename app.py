import pandas as pd
from flask import Flask, request, render_template
import pickle


app = Flask(__name__)

# Load the dataset
df = pd.read_json('Data/House_Price.json')

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    county = request.form.get('county')
    area_type = request.form.get('area_type')
    area = float(request.form.get('area'))

    # Fetch the price per square meter based on county and area type
    if area_type == "Urban":
        price_per_sqm = df.loc[df['County'] == county, 'Urban Price (KES per sq. m)'].values[0]
    elif area_type == "Suburban":
        price_per_sqm = df.loc[df['County'] == county, 'Suburban Price (KES per sq. m)'].values[0]
    elif area_type == "Rural":
        price_per_sqm = df.loc[df['County'] == county, 'Rural Price (KES per sq. m)'].values[0]
    else:
        price_per_sqm = 0

    # Calculate the predicted price
    predicted_price = price_per_sqm * area

    # Format the prediction result
    prediction_text = f"The estimated house price in {county} ({area_type}) for an area of {area:.2f} sq. m is KES {predicted_price:,.2f}."
    return render_template('index.html', prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
