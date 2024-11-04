from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample data
qa_pairs = [
    ("What services do you provide?", "We provide various insurance solutions."),
    ("How can I contact support?", "You can contact support via email at support@yourcompany.com."),
    ("How to contact the customer support", "Please asend u r query to this jayanthcjy@gmail mail"),
    ("How to contact the customer support through call", "numner is 93883")
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

# Example usage
while True:
    user_question = "What services do you provide?"
    response = get_answer(input())
    print("Bot:", response)
