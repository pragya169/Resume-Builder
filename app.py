from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from fpdf import FPDF
import os
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Needed for flash messages
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('resume.html')

@app.route('/generate', methods=['POST'])
def generate_resume():
    try:
        # Debug: Print received form data
        print("Received form data:", request.form)
        
        # Get all form data
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        summary = request.form.get('summary', '').strip()
        skills = request.form.get('skills', '').strip()
        experience = request.form.get('experience', '').strip()

        # Validate required fields
        if not all([full_name, email, phone, summary, skills, experience]):
            return "All fields are required", 400

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Add content to PDF
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt=full_name, ln=True, align='C')
        
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
        pdf.cell(200, 10, txt=f"Phone: {phone}", ln=True)
        
        # Add other sections (summary, skills, experience)
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt="Professional Summary", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=summary)
        
        # Repeat for skills and experience...

        # Save PDF
        filename = f"{re.sub('[^a-zA-Z0-9]', '_', full_name)}_resume.pdf"
        pdf_path = os.path.join(UPLOAD_FOLDER, filename)
        pdf.output(pdf_path)
        
        # Return the PDF file
        return send_file(pdf_path, as_attachment=True)

    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return f"Error generating resume: {str(e)}", 500
import webbrowser
if __name__ == '__main__':
    port = 8000
    url = f"http://localhost:{port}"
    webbrowser.open_new(url)  # Auto-opens browser
    app.run(host='0.0.0.0', port=5500, debug=True, threaded=True)