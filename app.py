from flask import Flask, render_template, request, jsonify
from model import analyze_market
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        stock_symbol = data.get('symbol')
        if not stock_symbol:
            return jsonify({"error": "Stock symbol is required."}), 400

        # Call your function to get the analysis
        analysis = analyze_market(stock_symbol)
        
        if 'error' in analysis:
            return jsonify({"error": analysis['error']}), 500
        
        return jsonify(analysis)
    except Exception as e:
        # Log the error for debugging purposes
        logging.error(f"Error processing request: {e}")
        # Return an error response
        return jsonify({"error": "Failed to analyze stock data. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True)
