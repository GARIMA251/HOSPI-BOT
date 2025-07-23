# How to Run HOSPI Locally

Prerequisites:

- Python 3.8+ installed.
- pip (Python package installer).

Setup Instructions:

- Clone the Repository:
git clone <YOUR_GITHUB_REPO_URL_HERE>
cd <YOUR_REPO_NAME>


- Create a Virtual Environment (Recommended): 
python -m venv venv

- Activate the virtual environment:

On macOS/Linux: source venv/bin/activate

On Windows: .\venv\Scripts\activate

- Install Dependencies:
pip install -r requirements.txt

- Set up Your Google Gemini API Key:
Generate an API key from Google AI Studio.

- Create a .env file in the project root directory and add:

GOOGLE_API_KEY=YOUR_GENERATED_API_KEY_HERE

- Run the Streamlit Application:
streamlit run app.py

This will open HOSPI in your default web browser, typically at http://localhost:8501.

