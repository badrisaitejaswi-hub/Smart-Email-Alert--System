from twilio.rest import Client

# Sample emails
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

# Subject keywords for category detection
category_keywords = {
    "Academic": [
        "exam", "hall ticket", "assignment", "attendance",
        "results", "marks", "project", "submission", "certificate",
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

# Priority mapping
category_priority = {
    "Academic": "High",
    "Career": "High",
    "Finance": "High",
    "Promotion": "Low",
    "Social": "Low",
    "Other": "Low"
}

# Twilio Credentials
account_sid = "YOUR_TWILIO_ACCOUNT_SID"
auth_token = "YOUR_TWILIO_AUTH_TOKEN"

# Twilio Sandbox WhatsApp Number
from_whatsapp = "TWILIO_WHATSAPP_NUMBER"

# Your WhatsApp Number
to_whatsapp = "YOURS_WHATSAPP_NUMBER"


# Function to detect category using sender domain + subject keywords
def detect_category(sender, subject):
    sender = sender.lower()
    subject = subject.lower()

    # Sender domain based filtering
    if (
        "college.com" in sender or
        "university.edu" in sender or
        "faculty.edu" in sender or
        "collegeportal.edu" in sender or
        "examcell.edu" in sender or
        "studentmail.edu" in sender or
        "campus.edu" in sender
    ):
        return "Academic"

    elif (
        "infosys.com" in sender or
        "tcs.com" in sender or
        "wipro.com" in sender or
        "internshala.com" in sender or
        "naukri.com" in sender or
        "linkedinjobs.com" in sender or
        "careers.com" in sender or
        "recruitment.com" in sender
    ):
        return "Career"

    elif (
        "bank.com" in sender or
        "payments.com" in sender or
        "paytm.com" in sender or
        "billing.com" in sender or
        "hdfcbank.com" in sender or
        "sbi.co.in" in sender or
        "icicibank.com" in sender or
        "phonepe.com" in sender
    ):
        return "Finance"

    elif (
        "offers.com" in sender or
        "shopping.com" in sender or
        "fashion.com" in sender or
        "deals.com" in sender or
        "amazon.in" in sender or
        "flipkart.com" in sender or
        "myntra.com" in sender or
        "zomato.com" in sender or
        "swiggy.com" in sender
    ):
        return "Promotion"

    elif (
        "instagram.com" in sender or
        "youtube.com" in sender or
        "linkedin.com" in sender or
        "spotify.com" in sender or
        "netflix.com" in sender or
        "facebook.com" in sender or
        "twitter.com" in sender or
        "socialhub.com" in sender
    ):
        return "Social"

    # Subject keyword based filtering
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in subject:
                return category

    return "Other"


# Twilio Client
client = Client(account_sid, auth_token)

# Process emails and send alerts
print("Checking maisl......\n")
for email in emails:
    sender = email["sender"]
    subject = email["subject"]

    # Detect category
    category = detect_category(sender, subject)

    # Detect priority
    priority = category_priority[category]

    print("Email Found:")
    print("From:", sender)
    print("Subject:", subject)
    print("Category:", category)
    print("Priority:", priority)
    print("-" * 50)

    # Send WhatsApp alert only for high priority emails
    if priority == "High":
        message_body = (
            f"Important Email Alert!\n"
            f"From: {sender}\n"
            f"Subject: {subject}\n"
            f"Category: {category}\n"
            f"Priority: {priority}"
        )

        try:
            message = client.messages.create(
                body=message_body,
                from_=from_whatsapp,
                to=to_whatsapp
            )
            print("WhatsApp Alert Sent Successfully!")
            print("SID:", message.sid)
        except Exception as e:
            print("Error sending WhatsApp message:", e)
