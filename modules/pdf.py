from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
import os


def generate_module_pdf(module):
    """Generate PDF for a module"""
    # Render the HTML template
    html_string = render_to_string('modules/module_pdf.html', {
        'module': module,
    })
    
    # Create PDF
    html = HTML(string=html_string)
    
    # Generate PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        html.write_pdf(temp_file.name)
        temp_file.seek(0)
        
        # Read the PDF content
        with open(temp_file.name, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
        
        # Clean up temp file
        os.unlink(temp_file.name)
        
        return pdf_content
