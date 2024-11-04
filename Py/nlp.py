import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download the required NLTK data
nltk.download('punkt')          # For tokenizing the text
nltk.download('stopwords')      # For stopwords filtering
nltk.data.path.append('C:/Users/Jayanth C/nltk_data')
text = "Your text data goes here."
tokens = word_tokenize(text)
stop_words = set(stopwords.words('english'))
filtered_text = [word for word in tokens if word.lower() not in stop_words]

print(filtered_text)


# import nltk
# # nltk.download('punkt')
# # nltk.download('stopwords')
# nltk.data.path.append('C:/Users/Jayanth C/nltk_data')
