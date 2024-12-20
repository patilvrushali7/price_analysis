from flask import Flask, request, jsonify
import pickle
import pandas as pd

# Load dataset (ensure it's accessible or use a relative path)
df = pd.read_csv('ecommerce_recommendation.csv')

# Initialize Flask app
app = Flask(__name__)

# Load the serialized recommendation function
with open('recommendation_function.pkl', 'rb') as file:
    recommend_similar_products = pickle.load(file)

@app.route('/recommend', methods=['GET'])
def recommend():
    # Get input data from the URL query parameters
    product_name = request.args.get('name')
    product_price = request.args.get('price', type=float)  # Convert price to float

    # Validate inputs
    if not product_name or product_price is None:
        return jsonify({"error": "Both 'name' and 'price' query parameters are required."}), 400

    # Call the recommendation function
    recommendations = recommend_similar_products(product_name, product_price, df)

    # Convert DataFrame results to JSON
    if isinstance(recommendations, pd.DataFrame):
        recommendations = recommendations.to_dict(orient='records')

    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)


