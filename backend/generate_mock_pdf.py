from fpdf import FPDF

def create_mock_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    
    pdf.cell(200, 10, txt="Welcome to the Tara AI E-Learning Platform", ln=1, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt="Tara AI is a state-of-the-art interactive e-learning platform launched in 2026. "
                              "We offer comprehensive courses spanning Data Science, Machine Learning, and Web Development.")
    
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt="Platform Features:\n"
                              "- 24/7 AI-powered tutoring with Tara.\n"
                              "- Certification upon completion of intermediate and advanced tracks.\n"
                              "- Access to an exclusive community of developers and data scientists.")
                              
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt="Contact & Support:\n"
                              "For any issues, you can reach out to support@tara-ai.com. "
                              "Billing inquiries should be directed to billing@tara-ai.com. "
                              "You can also use the built-in chat interface to ask Tara about courses and platform features.")
                              
    pdf.output("platform_info.pdf")
    print("Created platform_info.pdf")

if __name__ == "__main__":
    create_mock_pdf()
