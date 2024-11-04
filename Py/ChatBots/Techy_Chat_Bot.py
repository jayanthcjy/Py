from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Training data
questions = [
    "What services does your company offer?",
    "How does your RPA service work?",
    "What are the benefits of RPA for my business?",
    "Can you automate our data entry process?",
    "How long does it take to implement RPA?"
]
answers = [
    "We provide end-to-end robotic process automation (RPA) solutions using UI Path, including process automation, data extraction, workflow optimization, and custom bot development.",
    "Our RPA service uses UI Path to automate repetitive tasks, integrate with various software, and streamline workflows, allowing companies to save time and resources.",
    "RPA can reduce costs, minimize human error, improve compliance, and allow your team to focus on more complex, strategic tasks.",
    "Yes, we specialize in automating data entry and other manual processes using UI Path’s advanced data processing capabilities.",
    "The implementation time varies depending on the process, but most RPA solutions take a few weeks to design, test, and deploy."
]

# Convert questions to vectors
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)
from sklearn.metrics.pairwise import cosine_similarity

def get_answer(user_question):
    user_question_vec = vectorizer.transform([user_question])
    similarity = cosine_similarity(user_question_vec, X)
    best_match_idx = np.argmax(similarity)
    return answers[best_match_idx]

# Example query
user_query = "What services do you offer?"
print("Bot:", get_answer(user_query))



from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question")
    answer = get_answer(user_question)
    return jsonify({"answer": answer})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render uses a PORT environment variable
    app.run(host="0.0.0.0", port=port)
