from flask import Flask, render_template
from twilio.rest import Client

app = Flask(__name__)

# ================== SAMPLE EMAILS ==================
emails = [
    {"sender": "orders@amazon.in", "subject": "Your order has been shipped"},
    {"sender": "offers@flipkart.com", "subject": "Big Discount Sale Starts Today"},
    {"sender": "deals@swiggy.com", "subject": "Get 50% Off on Your Next Order"},
    {"sender": "promo@zomato.com", "subject": "Flat ₹100 Off on Food Delivery"},
    {"sender": "fashion@myntra.com", "subject": "Exclusive Fashion Sale Just for You"},
    {"sender": "updates@youtube.com", "subject": "New videos recommended for you"},
    {"sender": "alerts@linkedin.com", "subject": "People are viewing your profile"},
    {"sender": "music@spotify.com", "subject": "Your weekly playlist is ready"},
    {"sender": "notify@instagram.com", "subject": "You have new followers"},
    {"sender": "watch@netflix.com", "subject": "New movies added for you"},
    {"sender": "learning@coursera.org", "subject": "Your course progress report"},
    {"sender": "connect@socialhub.com", "subject": "New friend suggestions available"},
    {"sender": "careers@infosys.com", "subject": "Interview Scheduled for Monday"}
]

# ================== KEYWORDS ==================
category_keywords = {
    "Academic": [
        "exam", "hall ticket", "assignment", "attendance",
        "results", "marks", "project", "submission", "certificate"
        "class", "seminar", "syllabus", "faculty"
    ],
    "Career": [
        "interview", "job", "internship", "placement",
        "shortlisted", "selected", "recruitment", "offer letter",
        "hiring", "vacancy", "career", "hr"
    ],
    "Finance": [
        "payment", "fee", "statement", "transaction",
        "invoice", "bill", "salary", "refund", "balance",
        "bank", "credited", "debited", "loan"
    ],
    "Promotion": [
        "sale", "discount", "offer", "free",
        "coupon", "cashback", "shopping", "exclusive",
        "limited time", "special price", "mega sale", "deal"
    ],
    "Social": [
        "followers", "playlist", "videos", "recommended",
        "profile", "message", "comment", "story", "movies",
        "friend", "social", "network", "viewing"
    ]
}

# ================== PRIORITY ==================
category_priority = {
    "Academic": "High",
    "Career": "High",
    "Finance": "High",
    "Promotion": "Low",
    "Social": "Low",
    "Other": "Low"

}

# ================== TWILIO ==================
account_sid = "YOUR_TWILIO_ACCOUNT_SID"
auth_token = "YOUR_TWILIO_AUTH_TOKEN"
from_whatsapp = "TWILIO_WHATSAPP_NUMBER"
to_whatsapp = "YOUR_WHATSAPP_NUMBER"

# ================== CATEGORY DETECTION ==================
def detect_category(sender, subject):
    sender = sender.lower()
    subject = subject.lower()

    # DOMAIN BASED
    if (
        "college.com" in sender or "university.edu" in sender or
        "faculty.edu" in sender or "collegeportal.edu" in sender or
        "examcell.edu" in sender or "studentmail.edu" in sender or
        "campus.edu" in sender
    ):
        return "Academic"

    elif (
        "infosys.com" in sender or "tcs.com" in sender or
        "wipro.com" in sender or "internshala.com" in sender or
        "naukri.com" in sender or "linkedinjobs.com" in sender or
        "careers.com" in sender or "recruitment.com" in sender
    ):
        return "Career"

    elif (
        "bank.com" in sender or "payments.com" in sender or
        "paytm.com" in sender or "billing.com" in sender or
        "hdfcbank.com" in sender or "sbi.co.in" in sender or
        "icicibank.com" in sender or "phonepe.com" in sender
    ):
        return "Finance"

    elif (
        "offers.com" in sender or "shopping.com" in sender or
        "fashion.com" in sender or "deals.com" in sender or
        "amazon.in" in sender or "flipkart.com" in sender or
        "myntra.com" in sender or "zomato.com" in sender or
        "swiggy.com" in sender
    ):
        return "Promotion"

    elif (
        "instagram.com" in sender or "youtube.com" in sender or
        "linkedin.com" in sender or "spotify.com" in sender or
        "netflix.com" in sender or "facebook.com" in sender or
        "twitter.com" in sender or "socialhub.com" in sender
    ):
        return "Social"

    # KEYWORD BASED
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in subject:
                return category

    return "Other"


# ================== HOME ==================
@app.route('/')
def home():
    total = len(emails)
    important = 0

    for email in emails:
        category = detect_category(email["sender"], email["subject"])
        if category_priority[category] == "High":
            important += 1

    ignored = total - important

    return render_template("index.html",
                           total=total,
                           important=important,
                           ignored=ignored)


# ================== CHECK ==================
@app.route('/check')
def check_emails():
    important_emails = []

    for email in emails:
        category = detect_category(email["sender"], email["subject"])
        priority = category_priority[category]

        email["category"] = category
        email["priority"] = priority

        if priority == "High":
            important_emails.append(email)

    # ✅ COUNTS
    total = len(emails)
    important = len(important_emails)
    ignored = total - important

    try:
        client = Client(account_sid, auth_token)

        for email in important_emails:
            message_body = f"""
Important Email Alert!
From: {email['sender']}
Subject: {email['subject']}
Category: {email['category']}
Priority: {email['priority']}
"""
            client.messages.create(
                body=message_body,
                from_=from_whatsapp,
                to=to_whatsapp
            )

        status = "WhatsApp alert sent successfully!" if important_emails else "No important emails found."

    except Exception as e:
        status = f"Error: {str(e)}"

    return render_template(
        "emails.html",
        emails=important_emails,
        status=status,
        total=total,
        important=important,
        ignored=ignored
    )


# ================== RUN ==================
if __name__ == "__main__":
    app.run(debug=True)
