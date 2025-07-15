# How to Run HOSPI Locally

Prerequisites:

- Python 3.8+ installed.
- pip (Python package installer).

Setup Instructions:

## Setup Instructions:

1. **Clone the Repository:**
   - `git clone https://github.com/your-username/HOSPI-BOT.git`
   
2. **Install Dependencies:**
   - Navigate to the project folder: `cd HOSPI-BOT`
   - Create a virtual environment:  
     `python -m venv venv`
   - Activate the virtual environment:
     - On Windows: `.\venv\Scripts\activate`
     - On Mac/Linux: `source venv/bin/activate`
   - Install required packages:
     - `pip install -r requirements.txt`
   
3. **Configure .env file:**
   - Create a `.env` file in the root of the project.
   - Add your environment variables such as:
     ```
     ADMIN_PASSWORD=yourpassword
     GOOGLE_API_KEY=yourapikey
     ```

4. **Run the App Locally:**
   - Run the Streamlit app:  
     `streamlit run app.py`

5. **Access the App:**
   - Open the provided URL in your browser (typically `http://localhost:8501`).


