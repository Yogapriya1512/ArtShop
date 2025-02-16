from flask import Flask, request, jsonify
import stripe

app = Flask(__name__)

# Stripe API Key (Replace with your actual secret key)
stripe.api_key = "sk_test_your_secret_key"

# Sample products (Later, we can connect this to a database)
products = {
    1: {"name": "Sunset Bliss", "price": 499},
    2: {"name": "Ocean Waves", "price": 599},
    3: {"name": "City Lights", "price": 699}
}

@app.route("/")
def home():
    return "Flask server is running!"

# Checkout API - Handles the payment request
@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    address = data.get("address")
    cart = data.get("cart", [])

    if not cart:
        return jsonify({"error": "Cart is empty"}), 400

    # Calculate total amount
    total_amount = sum(products[item['id']]['price'] for item in cart)

    # Create Stripe payment intent
    intent = stripe.PaymentIntent.create(
        amount=total_amount * 100,  # Stripe works in paise (cents)
        currency="inr",
        receipt_email=email,
    )

    return jsonify({"client_secret": intent.client_secret, "total": total_amount})

if __name__ == "__main__":
    app.run(debug=True)
