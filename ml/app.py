from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Mock ML model functions
def clean_text(text):
    # Remove filler words and unnecessary characters
    filler_words = ['and', 'or', 'but', 'so', 'because', 'however', 'then', 'also',
                    'like', 'just', 'actually', 'basically', 'literally', 'kinda', 'sorta',
                    'um', 'uh', 'ah', 'er', 'well', 'you', 'know', 'I', 'mean', 'am', 'is', 'are']
    # Remove filler words
    pattern = re.compile(r'\b(' + '|'.join(filler_words) + r')\b', re.IGNORECASE)
    cleaned_text = pattern.sub('', text)
    # Remove extra spaces
    cleaned_text = re.sub(' +', ' ', cleaned_text)
    return cleaned_text.strip()

def detect_job_field(text):
    # Mock implementation of job field detection
    # In a real scenario, this would involve ML model inference
    text_lower = text.lower()
    if 'python' in text_lower or 'machine learning' in text_lower or 'software' in text_lower:
        return 'Software Engineering'
    elif 'marketing' in text_lower or 'seo' in text_lower or 'content' in text_lower:
        return 'Marketing'
    elif 'finance' in text_lower or 'accounting' in text_lower or 'investment' in text_lower:
        return 'Finance'
    else:
        return 'General'

def generate_suggestions(job_field):
    # Mock suggestions based on job field
    suggestions = {
        'Software Engineering': [
            'Include more programming projects.',
            'Highlight your experience with version control systems like Git.',
            'Mention any collaborative development experience.'
        ],
        'Marketing': [
            'Emphasize your successful marketing campaigns.',
            'Include metrics like ROI to showcase effectiveness.',
            'Highlight experience with digital marketing tools.'
        ],
        'Finance': [
            'Detail your experience with financial analysis.',
            'Include certifications like CPA if applicable.',
            'Mention proficiency with financial software.'
        ],
        'General': [
            'Provide clear and concise bullet points.',
            'Highlight your most relevant experience.',
            'Ensure your contact information is up to date.'
        ]
    }
    return suggestions.get(job_field, suggestions['General'])

@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided.'}), 400

    # Clean the text
    cleaned_text = clean_text(text)

    # Detect the job field
    job_field = detect_job_field(cleaned_text)

    # Generate suggestions
    suggestions = generate_suggestions(job_field)

    # Return the results
    return jsonify({
        'job_field': job_field,
        'suggestions': suggestions
    })

if __name__ == '__main__':
    app.run(debug=True)
