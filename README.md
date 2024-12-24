# Entersoft Challenge

## Overview

This project is a chatbot developed for the Entersoft Challenge during [Makeathon 2024](https://uniai.gr/makeathon-2024/). It enables company managers to interact with an SQL database (ERP system) using natural language queries. The chatbot interprets user inputs, converts them into SQL queries, retrieves the relevant data, and responds in a human-readable format.

## Features

- **Natural Language Processing (NLP):** Understands and processes user queries in natural language.
- **SQL Query Generation:** Translates user inputs into SQL commands to interact with the database.
- **Data Retrieval:** Fetches accurate information from the database based on user queries.
- **User-Friendly Responses:** Provides answers in a clear and structured natural language format.

## Installation

1. **Clone the Repository:**
  > git clone https://github.com/NIKOMAHOS/entersoft_challenge.git

2. **Navigate to the Project Directory:**
  > cd entersoft_challenge
   
4. **Set Up a Virtual Environment (Optional but Recommended)**:
  > python -m venv venv
  > source venv/bin/activate  # On Windows: venv\Scripts\activate

5. **Install Dependencies:**
  > pip install -r requirements.txt

## Usage

1. Configure API Keys:
  > Ensure your api_key.ini file contains the necessary API keys for any external services the chatbot uses.

2. Run the Application:
  > python src/app.py
  > The application will start, and you can interact with the chatbot through the provided interface.

### Project Structure
- `src/`: Contains the main application code.
- `data/`: Includes any datasets or database files used.
- `static/`: Holds static files like images or CSS.
- `requirements.txt`: Lists all Python dependencies.
- `api_key.ini`: Configuration file for API keys.

## Acknowledgments
- Developed for the Entersoft Challenge during the 2024 Makeathon.
- Inspired by the need for seamless human-database interactions.
