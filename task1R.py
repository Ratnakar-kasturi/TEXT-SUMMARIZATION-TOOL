import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict
import string

# Ensure NLTK data is downloaded (run these once)
# nltk.download('punkt')
# nltk.download('stopwords')

def summarize_text(text, num_sentences=3):
    """
    Summarizes the given text by extracting the most important sentences.
    """
    sentences = sent_tokenize(text)

    if not sentences:
        return "Input text is empty or could not be tokenized into sentences."

    if len(sentences) <= num_sentences:
        return text

    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)

    words = word_tokenize(text.lower())
    filtered_words = [
        word for word in words
        if word.isalnum() and word not in stop_words and word not in punctuation
    ]

    if not filtered_words:
        return "Cannot summarize: No meaningful words found after filtering."

    word_frequencies = defaultdict(int)
    for word in filtered_words:
        word_frequencies[word] += 1

    max_frequency = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] = (word_frequencies[word] / max_frequency)

    sentence_scores = defaultdict(int)
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                sentence_scores[i] += word_frequencies[word]

    if not sentence_scores:
        return "Cannot summarize: Sentences could not be scored."

    sorted_sentence_indices = sorted(sentence_scores.keys(), key=lambda x: sentence_scores[x], reverse=True)
    top_n_indices_unsorted = sorted_sentence_indices[:num_sentences]
    top_sentence_indices_sorted = sorted(top_n_indices_unsorted)

    summary_sentences = [sentences[i] for i in top_sentence_indices_sorted]
    summary = ' '.join(summary_sentences)

    return summary

if __name__ == "__main__":
    article = """
    Natural language processing (NLP) is a subfield of artificial intelligence (AI) that focuses on enabling computers to understand, interpret, and generate human language. It combines computational linguistics—rule-based modeling of human language—with statistical, machine learning, and deep learning models. NLP has made significant strides in recent years, largely due to advancements in deep learning architectures like transformers.

    Key applications of NLP include sentiment analysis, machine translation, spam detection, chatbots, and text summarization. Sentiment analysis, for instance, helps businesses understand customer opinions from reviews and social media. Machine translation, like Google Translate, allows for communication across language barriers. Chatbots are increasingly used for customer service and information retrieval.

    Text summarization, the focus of this tool, aims to create a concise and coherent summary of a longer text document while retaining the main points. There are two main types: extractive and abstractive. Extractive summarization identifies and pulls key sentences or phrases directly from the original text. Abstractive summarization, on the other hand, generates new sentences that capture the essence of the original text, often requiring more advanced AI models.

    Challenges in NLP include ambiguity in language, variations in grammar, and the need for vast amounts of data for training models. However, ongoing research continues to push the boundaries of what's possible, leading to more sophisticated and accurate NLP systems. The future of NLP holds immense potential for transforming how humans interact with technology and process information.
    """

    print("--- Original Article ---")
    print(article)
    print("\n" + "="*50 + "\n")

    summary_3_sentences = summarize_text(article, num_sentences=3)
    print(f"--- Summary (3 sentences) ---")
    print(summary_3_sentences)
    print("\n" + "="*50 + "\n")

    summary_2_sentences = summarize_text(article, num_sentences=2)
    print(f"--- Summary (2 sentences) ---")
    print(summary_2_sentences)
    print("\n" + "="*50 + "\n")

    empty_summary = summarize_text("", num_sentences=2)
    print(f"--- Summary of Empty String ---")
    print(empty_summary)
    print("\n" + "="*50 + "\n")

    short_text = "This is a short sentence. Another one follows."
    short_summary = summarize_text(short_text, num_sentences=5)
    print(f"--- Summary of Short Text (more sentences requested than available) ---")
    print(short_summary)
    print("\n" + "="*50 + "\n")