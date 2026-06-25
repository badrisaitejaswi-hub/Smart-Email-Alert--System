# Smart-Email-Alert--System
Smart Email Alert System with WhatsApp Notifications
Smart Email Alert System with WhatsApp Notifications

Overview

Smart Email Alert System is a Python-based application that identifies important emails and sends instant WhatsApp notifications to users. The system helps users avoid missing critical emails hidden among promotional, social, and other less important messages.

Features

- Categorizes emails into different groups such as:
  - Education
  - Career
  - Social Media
  - Promotions
- Uses sender domains and subject keywords for classification.
- Assigns priority levels to each email category.
- Filters high-priority emails automatically.
- Sends WhatsApp alerts for important emails using Twilio API.
- Provides two operating modes:
  - Web Mode – Displays important emails on a website and sends WhatsApp alerts.
  - Automatic Mode – Continuously monitors emails and sends WhatsApp alerts automatically.

Project Structure

Web Mode

Files used:

- "app.py" – Backend logic, email categorization, filtering, and WhatsApp notification.
- "index.html" – Home page of the web application.
- "emails.html" – Displays filtered important emails.
- "style.css" – User interface styling.

Automatic Mode

Files used:

- "auto_alert.py" – Automatically checks emails, filters important emails, and sends WhatsApp notifications at regular intervals.

Working Methodology

1. Sample emails are provided as input.
2. Emails are categorized based on sender domains and subject keywords present in the subject.
3. A priority level is assigned to each category.
4. The system filters emails with high priority.
5. Important email details are displayed on the website (Web Mode).
6. WhatsApp notifications are sent using Twilio API.
7. In Automatic Mode, the process runs periodically without user interaction.

Technologies Used

- Python
- Flask
- HTML
- CSS
- Twilio API
- Visual Studio Code

Advantages

- Reduces the risk of missing important emails.
- Provides instant WhatsApp notifications.
- Simple and easy-to-use interface.
- Supports both manual and automatic monitoring.

How to Run

Web Mode

1. Install required packages:

pip install flask twilio

2. Run the application:

python app.py

3. Open the browser and visit:

http://127.0.0.1:5000

Automatic Mode

Run the automation script:

python auto_alert.py

Future Enhancements

- Integration with real Gmail and Outlook accounts.
- Machine Learning-based email classification.
- Database support for email history.
- Multi-user support.
- Mobile application integration.
