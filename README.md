# Project Title

This project performs vector search using Python and Google Cloud services like BigQuery. Follow the steps below to set up the environment, install dependencies, and authenticate with Google Cloud.

## Prerequisites

Ensure that the following are installed on your system:

- **Python** (version 3.6 or higher)
- **Pip** (Python's package installer)
- **Google Cloud SDK** for interacting with Google Cloud services

Ensure the following APIs are enabled in your Google Cloud project:
- **BigQuery API**
- **Vertex AI API**

### Install Google Cloud SDK

If you don't have the **Google Cloud SDK** installed, download and install it by following the official instructions [here](https://cloud.google.com/sdk/docs/install).

Once the SDK is installed, authenticate with your Google Cloud account by running the following command in your terminal or command prompt:

```bash
gcloud auth login
```

### Run the project

- Create Virtual Environment 
```bash
python3 -m venv venv
```

- Activate Virtual Environment 
```bash
source venv/bin/activate
```

- Install Project Requirements 
```bash
pip install -r requirements.txt
```

- Replace the TableId with Actual TableId in line 91 and 106
```bash
YOUR_TABLE_ID
```

- Uncomment Line 123 to save data in BigQuery Table (Ignore This if already done)
```bash
save_to_bq(generate_embedding())
```

- Run text_embeddings.py If you want to store data in BQ (Ignore This if already done)
```bash
python text_embeddings.py
```

- Once Data is stored run the Flask Server 
```bash
python index.py
```

- Development Server Started now access the URL from Browser and do the testing with Api
```bash
http://127.0.0.1:5000/vector-search?query=Test Query
```

### NOTES

- Data.docx file is already present in the code.
- If You want to change the data you are free to replace the content of the file.
- We are taking every paragraph and generating its embeddings, You are free to change this logic and define your preferred chunk size.