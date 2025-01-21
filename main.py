# Import necessary libraries
from flask import Flask, request, jsonify  # Flask for API creation
from openai import OpenAI  # OpenAI client for LLM integration
from dotenv import load_dotenv  # For loading environment variables
import os  
# lod .env file 
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Retrieve the OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Configure OpenAI client with the API key
client = OpenAI(api_key=api_key)

# In-memory storage for processed results
processed_results = {}

# Defining a route to process text
@app.route('/process', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            # Validating input and return an error if 'text' field is missing
            return jsonify({"error": "Invalid input. 'text' field is required."}), 400

        # Extracting the text to process
        input_text = data['text']

        # Using OpenAI GPT model to summarize the input text
        completion = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Provide a concise summary less than 50 words of the following text: {input_text}"}
            ]
        )

        # Extracting the summary from the API response
        summary = completion.choices[0].message.content.strip()


        # Storing the result in memory with a unique ID
        result_id = len(processed_results) + 1
        processed_results[result_id] = {"input_text": input_text, "summary": summary}

        # Returning the processed result as JSON
        return jsonify({"id": result_id, "summary": summary}), 200

    except Exception as e:
        # Handleing unexpected errors and return an error message
        return jsonify({"error": str(e)}), 500

# Defining a route to retrieve all processed results
@app.route('/history', methods=['GET'])
def get_history():
    """
    Endpoint: GET /history
    Purpose: Retrieve all processed text results.
    """
    try:
        # Returning all results stored in memory
        return jsonify({"history": processed_results}), 200

    except Exception as e:
        # Handling unexpected errors and return an error message
        return jsonify({"error": str(e)}), 500

# Running the Flask application
if __name__ == '__main__':
    # Starting the Flask server on localhost at port 5000
    app.run(debug=True)
