Project Name: MCQ Generator
Overview
MCQ Generator is a Python project that allows users to generate Multiple Choice Questions (MCQs) from a given input text. The project utilizes various natural language processing (NLP) techniques, NLTK, spacy, and ConceptNet API to identify important words, generate distractors, and formulate MCQs based on the input text.
Features
Read text from a file
Process the input text to identify important words
Generate distractors for each important word
Formulate Multiple Choice Questions with blanks for important words
Display the MCQs in a Graphical User Interface (GUI)
Installation
Clone the repository to your local machine.
Install the required libraries by running the following command:
pip install nltk spacy requests pillow
Download necessary NLTK data by running the following Python code:
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('popular')
Download the English model for spacy by running:
python -m spacy download en_core_web_sm
How to Run
Open the terminal and navigate to the project directory.
Run the GUI main entry point gui.py using the following command:
python gui.py
Dependencies
Python 3.x
NLTK
spacy
requests
pillow
