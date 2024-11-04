from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sample data
qa_pairs = [
    ("What services do you provide?", "We provide various insurance solutions."),
    ("How can I contact support?", "You can contact support via email at support@yourcompany.com."),
    ("How to contact the customer support", "Please send your query to this jayanthcjy@gmail mail"),
    ("How to contact the customer support through call", "The number is 93883")
]

questions, answers = zip(*qa_pairs)

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

# Function to get an answer
def get_answer(user_question):
    user_question_vec = vectorizer.transform([user_question])
    similarities = cosine_similarity(user_question_vec, X)
    best_match_index = similarities.argmax()
    return answers[best_match_index]

# Function to send an email
def send_email(to_email, subject, body):
    from_email = "householdsmart09@gmail.com"
    from_password = "R@ny00001"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage
while True:
    user_question = input("You: ")
    response = get_answer(user_question)
    print("Bot:", response)

    if "send details through mail" in user_question.lower():
        to_email = input("Please provide your email address: ")
        subject = "Requested Information"
        body = response
        send_email(to_email, subject, body)
