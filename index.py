from flask import Flask, jsonify, request
from text_embeddings import vector_search_in_bigquery, embed_text
# Initialize the Flask application
app = Flask(__name__)

# Define a route for the GET API
@app.route('/vector-search', methods=['GET'])
def get_data():
    query = request.args.get('query', default='Can i work from home ?')
    query_embeddings = embed_text([query], "RETRIEVAL_DOCUMENT", 256)
    data = vector_search_in_bigquery(query_embeddings[0])
    # Return the data as a JSON response
    return jsonify(data)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)