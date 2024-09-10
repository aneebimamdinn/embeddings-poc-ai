from docx import Document
from google.cloud import bigquery
from typing import List, Optional
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel


def read_file_content():
    doc = Document("data.docx")
    chunks = []
    for paragraph in doc.paragraphs:
        # Join All paragraphs in single text
        chunks.append(paragraph.text)

    return chunks


def split_text_into_chunks(text: str, max_chunk_size: int) -> List[str]:
    if len(text) <= max_chunk_size:
        return [text]

    chunks = []
    current_chunk = ""

    for word in text.split():

        if len(current_chunk) + len(word) + 1 <= max_chunk_size:

            if current_chunk:
                current_chunk += " " + word
            else:
                current_chunk = word
        else:

            chunks.append(current_chunk)
            current_chunk = word

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def embed_text(
    texts: list = None,
    task: str = "RETRIEVAL_DOCUMENT",
    dimensionality: Optional[int] = 256,
) -> List[List[float]]:
    """Embeds texts with a pre-trained, foundational model.
    Args:
        texts (List[str]): A list of texts to be embedded.
        task (str): The task type for embedding. Check the available tasks in the model's documentation.
        dimensionality (Optional[int]): The dimensionality of the output embeddings.
    Returns:
        List[List[float]]: A list of lists containing the embedding vectors for each input text
    """
    if texts is None:
        texts = ["banana muffins? ", "banana bread? banana muffins?"]

    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    inputs = [TextEmbeddingInput(text, task) for text in texts]
    embeddings = model.get_embeddings(inputs)
    return [embedding.values for embedding in embeddings]


def split_text_into_sentences(text):
    sentences = [sentence.strip() for sentence in text.split('.') if sentence.strip()]
    return sentences


def generate_embedding():
    # To Store embedding and text
    data = []
    # Read content from file
    chunks = read_file_content()
    # Create Embedding for each chunk
    for chunk in chunks:
        embedding = embed_text([chunk], "RETRIEVAL_DOCUMENT", 256)
        data.append({
            "text": chunk,
            "embeddings": embedding[0]
        })

    return data


def save_to_bq(data):
    # Initialize BigQuery client
    client = bigquery.Client()

    # Define the table ID
    table_id = "YOUR_TABLE_ID"
    # Insert the rows into the BigQuery table
    errors = client.insert_rows_json(table_id, data)

    # Check for errors
    if not errors:
        print("New rows have been added.")
    else:
        print("Errors:", errors)


def vector_search_in_bigquery(query_embedding):
    sql_query = f"""
        SELECT base.text, distance
        FROM VECTOR_SEARCH(
   TABLE ai_practice_dataset.ai_poc_data , 'embeddings',
   (SELECT {query_embedding} as embed) , top_k => 5, distance_type => 'COSINE')
    """

    client = bigquery.Client()
    results = client.query(sql_query).result()
    parsed_results = []
    for row in results:
        row_dict = dict(row)
        parsed_results.append(row_dict)

    return parsed_results


# Run the Flask app
if __name__ == '__main__':
    # Uncomment this line if you want to insert the data
    # save_to_bq(generate_embedding())
    print("Running")
