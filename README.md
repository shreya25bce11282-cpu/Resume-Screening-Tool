# AI-Powered Resume Screening Tool

This project automates the process of screening and ranking resumes based on their relevance to a given job description. It uses NLP techniques to extract skills and experience from resumes and compares them against the job description to provide a ranked list of candidates.

---

## Features

- Extract text from PDF resumes using `pdfplumber`.
- Clean and normalize text for consistent analysis.
- Extract and weight relevant skills using spaCy.
- Extract years of experience using regex and date parsing.
- Vectorize resumes and job description using TF-IDF.
- Calculate cosine similarity scores to rank candidates.
- Interactive Streamlit web app to upload resumes and paste job descriptions.
- Adjustable scoring weights for skills and experience.
- Download ranked candidate results as CSV.

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/resume-screening-tool.git
   cd resume-screening-tool

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

3. **Install dependencies:**

     ```bash
     pip install -r requirements.txt

4.   **Download SpaCy English model**   

      ```bash
      python -m spacy download en_core_web_sm

5. **Run the app:**

     ```bash
     streamlit run app.py

 ## Usage
 1. Run the Streamlit app:

    ```bash
    streamlit run app.py

 2. In the web interface:

    -Upload one or more PDF resumes.
        
    -Paste the job description text.
        
    -Adjust skill match and experience weights using the sidebar sliders.
        
     -View the ranked candidates table.
        
     -Download the results as a CSV file.

 ## Project Structure
 ```
 resume-screening-tool/
|
|-- app.py                   # Main Streamlit app
|-- resume_parser.py         # Resume text extraction and processing
|-- vectorizer.py            # TF-IDF vectorization logic
|-- matcher.py               # Similarity and ranking logic
|-- skills.py                # List of skills for matching
|-- synonyms.py              # Synonym mapping for normalization
|-- requirements.txt         # Python dependencies
|-- README.md                # Project documentation
`-- sample_resumes/          # Sample PDF resumes for testing



  
 


