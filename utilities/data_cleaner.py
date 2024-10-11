import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

def clean_text(text):
    nltk.download('stopwords')
    nltk.download('wordnet')

    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    text = [word for word in text.split() if word not in stop_words]
    text = [stemmer.stem(word) for word in text] 
    text = [lemmatizer.lemmatize(word) for word in text]
    return ' '.join(text)

def clean_data(df):
    df['Map Data'] = df['Map Data'].fillna('')
    df = df[df['Map Data'].str.len() > 0]
    df = df[df['Map Data'].str.len() < 10000]
    # df['Map Data'] = df['Map Data'].apply(clean_text)
    return df