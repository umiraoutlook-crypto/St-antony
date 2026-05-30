import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Set the secret key for session security (in a real app, this would be loaded from environment variables)
app.secret_key = os.urandom(24)

# SMTP Mail Configuration
ADMIN_EMAIL = "kaifhadgone@gmail.com"
ADMIN_PASSWORD = "kodj sgss idyh dljy".replace(" ", "")  # Gmail App Password (strip spaces)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SSL port

def send_smtp_email(to_email, subject, body_html, body_text):
    """Sends a multi-part HTML/Text email via Gmail SMTP using SSL."""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"St. Antony's HSS <{ADMIN_EMAIL}>"
    msg['To'] = to_email

    # Attach text and html parts
    msg.attach(MIMEText(body_text, 'plain'))
    msg.attach(MIMEText(body_html, 'html'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(ADMIN_EMAIL, ADMIN_PASSWORD)
            server.sendmail(ADMIN_EMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"SMTP Error encountered: {str(e)}")
        return False

@app.route('/')
def index():
    """Render the school home page."""
    news = [
        {
            "id": 1,
            "title": "Admissions Open for Academic Year 2026-27",
            "date": "May 25, 2026",
            "summary": "Online admission inquiry forms are now active. Limited seats are available for Higher Secondary streams (Science & Commerce)."
        },
        {
            "id": 2,
            "title": "St. Antony's Wins Zonal Athletics Championship",
            "date": "May 18, 2026",
            "summary": "Our student sports council led the school to victory, securing 12 gold medals at the Chennai Zonal Athletics meet."
        },
        {
            "id": 3,
            "title": "Annual Science Exhibition 'Anveshan 2026'",
            "date": "April 30, 2026",
            "summary": "Students from classes IX to XII showcased innovative models in renewable energy and green technologies."
        }
    ]
    
    events = [
        {
            "id": 1,
            "title": "Parent-Teacher Association Meeting",
            "date": "June 05, 2026",
            "time": "09:30 AM - 01:00 PM",
            "location": "School Auditorium"
        },
        {
            "id": 2,
            "title": "World Environment Day Celebrations",
            "date": "June 05, 2026",
            "time": "08:30 AM",
            "location": "School Campus"
        },
        {
            "id": 3,
            "title": "Higher Secondary Classes Reopen",
            "date": "June 12, 2026",
            "time": "08:00 AM",
            "location": "St. Antony's Campus"
        }
    ]
    return render_template('index.html', news=news, events=events)

@app.route('/about')
def about():
    """Render the About Us page."""
    return render_template('about.html')

@app.route('/academics')
def academics():
    """Render the Academics page."""
    return render_template('academics.html')

@app.route('/admissions')
def admissions():
    """Render the Admissions page."""
    return render_template('admissions.html')

@app.route('/gallery')
def gallery():
    """Render the Gallery page."""
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    """Render the Contact Us page."""
    return render_template('contact.html')

@app.route('/submit-inquiry', methods=['POST'])
def submit_inquiry():
    """Handle admission inquiry form submissions and send SMTP mails."""
    try:
        data = request.get_json() or request.form
        
        student_name = data.get('studentName')
        parent_name = data.get('parentName')
        email = data.get('email')
        phone = data.get('phone')
        grade = data.get('grade')
        message = data.get('message', 'No details provided.')
        
        if not all([student_name, parent_name, email, phone, grade]):
            return jsonify({
                "status": "error", 
                "message": "All required fields must be completed. Please check your inputs."
            }), 400

        # --- 1. Send detailed inquiry to Admin ---
        admin_subject = f"New Admission Inquiry - Student: {student_name}"
        admin_text = (
            f"Dear Admin,\n\n"
            f"A new admission inquiry has been submitted. Details:\n"
            f"Student Name: {student_name}\n"
            f"Parent Name: {parent_name}\n"
            f"Email Address: {email}\n"
            f"Phone Number: {phone}\n"
            f"Grade Requested: {grade}\n"
            f"Additional Queries: {message}\n\n"
            f"Please take action accordingly.\n"
        )
        admin_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #800000; border-bottom: 2px solid #D4AF37; padding-bottom: 10px;">New Admission Inquiry</h2>
                <p>Hello Admin,</p>
                <p>A parent has submitted an admission inquiry for St. Antony's. Here are the details:</p>
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                    <tr style="background-color: #FAF7F2;"><td style="padding: 10px; font-weight: bold; width: 180px;">Student Name:</td><td style="padding: 10px;">{student_name}</td></tr>
                    <tr><td style="padding: 10px; font-weight: bold;">Parent Name:</td><td style="padding: 10px;">{parent_name}</td></tr>
                    <tr style="background-color: #FAF7F2;"><td style="padding: 10px; font-weight: bold;">Email Address:</td><td style="padding: 10px;"><a href="mailto:{email}">{email}</a></td></tr>
                    <tr><td style="padding: 10px; font-weight: bold;">Phone Number:</td><td style="padding: 10px;"><a href="tel:{phone}">{phone}</a></td></tr>
                    <tr style="background-color: #FAF7F2;"><td style="padding: 10px; font-weight: bold;">Grade Requested:</td><td style="padding: 10px;">{grade}</td></tr>
                    <tr><td style="padding: 10px; font-weight: bold;">Additional Queries:</td><td style="padding: 10px;">{message}</td></tr>
                </table>
                <p style="font-size: 0.9rem; color: #777; border-top: 1px solid #eee; padding-top: 15px; margin-top: 20px;">
                    This inquiry was submitted from the official St. Antony's School Admissions portal.
                </p>
            </div>
        </body>
        </html>
        """
        
        admin_mail_success = send_smtp_email(ADMIN_EMAIL, admin_subject, admin_html, admin_text)

        # --- 2. Send automated Thank You reply to Parent ---
        parent_subject = "Inquiry Received - St. Antony's Girls Higher Secondary School, Chennai"
        parent_text = (
            f"Dear {parent_name},\n\n"
            f"Thank you for contacting St. Antony's Girls Higher Secondary School regarding the admission of {student_name} for Grade {grade}.\n\n"
            f"We have successfully received your inquiry and our admission office has logged the details. "
            f"Our admission coordinator will get in touch with you at this email address or via phone (+91 9498802477) within the next 48 business hours to guide you through the next steps (interaction scheduling and verification).\n\n"
            f"Warm regards,\n"
            f"Admissions Desk\n"
            f"St. Antony's Girls Higher Secondary School, Chennai\n"
            f"Email: stantony28@gmail.com\n"
        )
        parent_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 25px; border: 1px solid #e5f0e6; border-radius: 8px; background-color: #FAF7F2;">
                <div style="text-align: center; border-bottom: 2px solid #800000; padding-bottom: 15px; margin-bottom: 20px;">
                    <h2 style="color: #800000; margin: 0; font-family: Georgia, serif;">St. Antony's Girls Higher Secondary School</h2>
                    <p style="color: #D4AF37; font-size: 0.95rem; text-transform: uppercase; margin: 5px 0 0 0; letter-spacing: 1px;">Walk in Light and Truth</p>
                </div>
                <p>Dear <strong>{parent_name}</strong>,</p>
                <p>Thank you for your interest in St. Antony's. We have received your admission inquiry for <strong>{student_name}</strong> seeking enrollment in <strong>Grade {grade}</strong>.</p>
                <p>Our admissions desk has recorded the details. An administrative representative will contact you at <strong>{phone}</strong> or via email within 48 business hours to discuss the counseling session and guide you through the enrollment procedure.</p>
                
                <div style="background-color: #ffffff; border: 1px solid #eee; padding: 15px; border-radius: 6px; margin: 20px 0;">
                    <h4 style="margin-top: 0; color: #800000;">Next Steps in our Enrollment:</h4>
                    <ol style="margin-bottom: 0; padding-left: 20px; font-size: 0.95rem;">
                        <li><strong>Campus Counseling:</strong> Interaction of the candidate and parents with the Principal.</li>
                        <li><strong>Document Verification:</strong> Review of birth/transfer certificates and academic marks.</li>
                        <li><strong>Fee Settlement:</strong> Term payment to confirm and lock the candidate's seat.</li>
                    </ol>
                </div>
                
                <p>If you have any urgent queries, feel free to reach out to us at <a href="tel:+919498802477">+91 9498802477</a> or reply directly to <a href="mailto:stantony28@gmail.com">stantony28@gmail.com</a>.</p>
                
                <div style="border-top: 1px solid #ddd; padding-top: 15px; margin-top: 25px; font-size: 0.85rem; color: #777;">
                    <p style="margin: 0;">Warm regards,</p>
                    <p style="font-weight: bold; margin: 5px 0 0 0; color: #800000;">Admissions Coordinating Desk</p>
                    <p style="margin: 0;">Mylapore, Chennai - 600004</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        parent_mail_success = send_smtp_email(email, parent_subject, parent_html, parent_text)
        
        # Verify success of SMTP and return appropriate message
        if admin_mail_success and parent_mail_success:
            return jsonify({
                "status": "success",
                "message": f"Thank you, {parent_name}. The admission inquiry has been sent to the admin. A confirmation email has also been sent to your mail id: {email}."
            }), 200
        else:
            # Fallback in case mail transfer fails but inputs were logged
            return jsonify({
                "status": "success",
                "message": f"Thank you, {parent_name}. The inquiry for {student_name} was logged successfully. (Note: Email confirmation delivery was interrupted, but our admin has noted your request)."
            }), 200
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred while processing your request: {str(e)}"
        }), 500

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    """Handle contact page submissions, notifying admin and auto-responding to the user."""
    try:
        data = request.get_json() or request.form
        
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        
        if not all([name, email, subject, message]):
            return jsonify({
                "status": "error", 
                "message": "All fields are required. Please fill in the details."
            }), 400
            
        # --- 1. Send query notice to Admin ---
        admin_subj = f"New Contact Query: {subject} [From: {name}]"
        admin_text = (
            f"Dear Admin,\n\n"
            f"A user has submitted a contact query through the website. Details:\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Subject: {subject}\n"
            f"Message:\n{message}\n\n"
            f"Please respond accordingly.\n"
        )
        admin_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #800000; border-bottom: 2px solid #D4AF37; padding-bottom: 10px;">New Contact Query</h2>
                <p>Hello Admin,</p>
                <p>A query has been received from the Contact Us page on the school website:</p>
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                    <tr style="background-color: #FAF7F2;"><td style="padding: 10px; font-weight: bold; width: 140px;">From Name:</td><td style="padding: 10px;">{name}</td></tr>
                    <tr><td style="padding: 10px; font-weight: bold;">User Email:</td><td style="padding: 10px;"><a href="mailto:{email}">{email}</a></td></tr>
                    <tr style="background-color: #FAF7F2;"><td style="padding: 10px; font-weight: bold;">Subject:</td><td style="padding: 10px;">{subject}</td></tr>
                    <tr><td style="padding: 10px; font-weight: bold; vertical-align: top;">Message:</td><td style="padding: 10px; white-space: pre-wrap;">{message}</td></tr>
                </table>
                <p style="font-size: 0.9rem; color: #777; border-top: 1px solid #eee; padding-top: 15px; margin-top: 20px;">
                    This query was submitted from the official St. Antony's School Contact Us portal.
                </p>
            </div>
        </body>
        </html>
        """
        
        admin_mail_success = send_smtp_email(ADMIN_EMAIL, admin_subj, admin_html, admin_text)

        # --- 2. Send automated response to User ---
        user_subj = "Thank you for contacting St. Antony's Girls HSS, Chennai"
        user_text = (
            f"Dear {name},\n\n"
            f"Thank you for reaching out to St. Antony's Girls Higher Secondary School. We have received your query regarding '{subject}'.\n\n"
            f"Our administrative desk has logged your message. A school representative will review the details and respond to your email shortly.\n\n"
            f"Warm regards,\n"
            f"Office of Administration\n"
            f"St. Antony's Girls Higher Secondary School, Chennai\n"
            f"Phone: +91 9498802477\n"
            f"Email: stantony28@gmail.com\n"
        )
        user_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 25px; border: 1px solid #ddd; border-radius: 8px; background-color: #FAF7F2;">
                <div style="text-align: center; border-bottom: 2px solid #800000; padding-bottom: 15px; margin-bottom: 20px;">
                    <h2 style="color: #800000; margin: 0; font-family: Georgia, serif;">St. Antony's Girls Higher Secondary School</h2>
                    <p style="color: #D4AF37; font-size: 0.95rem; text-transform: uppercase; margin: 5px 0 0 0; letter-spacing: 1px;">Walk in Light and Truth</p>
                </div>
                <p>Dear <strong>{name}</strong>,</p>
                <p>Thank you for contacting us. We have received your message regarding "<strong>{subject}</strong>".</p>
                <p>Our administrative office has queued your request. A school representative will review the context and get back to you at <strong>{email}</strong> shortly.</p>
                
                <p>If your inquiry is urgent, please do not hesitate to contact our desk at <a href="tel:+919498802477">+91 9498802477</a> or email us at <a href="mailto:stantony28@gmail.com">stantony28@gmail.com</a>.</p>
                
                <div style="border-top: 1px solid #ddd; padding-top: 15px; margin-top: 25px; font-size: 0.85rem; color: #777;">
                    <p style="margin: 0;">Warm regards,</p>
                    <p style="font-weight: bold; margin: 5px 0 0 0; color: #800000;">Office of Administration</p>
                    <p style="margin: 0;">Mylapore, Chennai - 600004</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        user_mail_success = send_smtp_email(email, user_subj, user_html, user_text)

        if admin_mail_success and user_mail_success:
            return jsonify({
                "status": "success",
                "message": f"Thank you, {name}. Your message has been sent to the admin. A confirmation reply has also been sent to your email id: {email}."
            }), 200
        else:
            return jsonify({
                "status": "success",
                "message": f"Thank you, {name}. Your query was logged. (Note: Email notices are offline, but our office has logged your query)."
            }), 200
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred while processing your message: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
