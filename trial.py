import streamlit as st
import pytesseract
import numpy as np
from PIL import Image
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Function to detect sentiment of input text and identify positive, negative, neutral, and mixed parts
def detect_sentiment(input_text):
    try:
        if not input_text.strip():
            return "Please enter a paragraph.", "", {}, "", 0.0, 0.0

        # Perform sentiment analysis
        sid_obj = SentimentIntensityAnalyzer()
        sentiment_scores = sid_obj.polarity_scores(input_text)

        # Extract sentiment scores for each word
        word_sentiments = {}
        positive_words = []
        negative_words = []

        for word in input_text.split():
            word_sentiment = sid_obj.polarity_scores(word)['compound']
            word_sentiments[word] = word_sentiment
            if word_sentiment > 0:
                positive_words.append(word)
            elif word_sentiment < 0:
                negative_words.append(word)

        # Calculate percentage of positive and negative sentiments
        total_words = len(positive_words) + len(negative_words)
        
        # Handle division by zero
        if total_words == 0:
            return "Sorry, I couldn't analyze your text. Please make sure it's in English and try again.", "", {}, "", 0.0, 0.0

        positive_percentage = len(positive_words) / total_words * 100
        negative_percentage = len(negative_words) / total_words * 100

        # Determine overall sentiment
        compound_score = sentiment_scores['compound']
        if compound_score >= 0.05:
            overall_sentiment = 'positive'
            sentiment_emoji = '😊'
        elif compound_score <= -0.05:
            overall_sentiment = 'negative'
            sentiment_emoji = '😞'
        else:
            overall_sentiment = 'neutral'
            sentiment_emoji = '😐'

        # Generate summary of input paragraph (extracting key sentences)
        response_message = f"Based on the analysis of your input, it seems the overall sentiment is {overall_sentiment}."
        st.markdown(f"Sentiment Emotion: {sentiment_emoji}")
        response_message += f"\n\nHere's the breakdown:\n"
        response_message += f"- Positive: {positive_percentage:.2f}%\n"
        response_message += f"- Negative: {negative_percentage:.2f}%\n\n"
        response_message += f"Here is your input:\n\n"
        for word in input_text.split():
            if word in positive_words:
                response_message += f"<span style='background-color:#2AAA8A; padding: 2px 5px; border-radius: 5px;'>{word}</span> "
            elif word in negative_words:
                response_message += f"<span style='background-color:#FF6347; padding: 2px 5px; border-radius: 5px;'>{word}</span> "
            else:
                response_message += f"{word} "

        # Plot pie chart
        labels = ['Positive', 'Negative']
        sizes = [positive_percentage, negative_percentage]
        colors = ['#66c2a5', '#fc8d62']
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': 'white'}, textprops=dict(color="w"))
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Sentiment Breakdown', fontsize=14)
        # Add legend with custom colors
        legend_labels = ['Positive', 'Negative']
        legend_handles = [mpatches.Patch(color=color, label=label) for color, label in zip(colors, legend_labels)]
        plt.legend(handles=legend_handles, loc='best', fancybox=True, shadow=True, fontsize=10)
        # Remove unnecessary plot frame
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()

        st.pyplot(fig)

        return response_message, sentiment_emoji, word_sentiments, overall_sentiment, positive_percentage, negative_percentage
    except Exception as e:
        return f"An error occurred: {str(e)}", "", {}, "", 0.0, 0.0

# Function to extract text from the uploaded image
def extract_text_from_image(uploaded_image):
    img = Image.open(uploaded_image)
    img = img.convert('RGB')
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    # Perform text extraction using Tesseract OCR
    text = pytesseract.image_to_string(gray)
    return text

# Function for the main application logic
def main():
    # Display header and chat area
    st.title("Sentiment Analysis Bot")
    st.markdown("---")

    # Input options
    input_option = st.radio("How would you like to input your text?", ("Text", "Image"))

    if input_option == "Text":
        # Input text area
        input_text = st.text_area("Enter your paragraph:", "")

        # Send button
        if st.button("Analyze"):
            response, _, _, overall_sentiment, positive_percentage, negative_percentage = detect_sentiment(input_text)
            st.markdown("---")
            st.write(response, unsafe_allow_html=True)
            st.markdown("---")

            # Chatbot-style summary
            st.write("Here's what I found after analyzing your text:")
            st.write(f"The overall sentiment is {overall_sentiment}.")
            st.write(f"Positivity: {positive_percentage:.2f}%")
            st.write(f"Negativity: {negative_percentage:.2f}%")
            
    elif input_option == "Image":
        # Upload image
        uploaded_image = st.file_uploader("Upload Image:", type=["jpg", "jpeg", "png"])

        # Send button
        if st.button("Analyze") and uploaded_image is not None:
            # Extract text from the uploaded image
            extracted_text = extract_text_from_image(uploaded_image)
            st.markdown("---")
            st.write("Text Extracted from Image:")
            st.write(extracted_text)
            st.write("\n\n")

            # Perform sentiment analysis on the extracted text
            response, _, _, overall_sentiment, positive_percentage, negative_percentage = detect_sentiment(extracted_text)
            st.write(response, unsafe_allow_html=True)
            st.markdown("---")

            # Chatbot-style summary
            st.write("After analyzing the image, here's what I found:")
            st.write(f"The overall sentiment is {overall_sentiment}.")
            st.write(f"Positivity: {positive_percentage:.2f}%")
            st.write(f"Negativity: {negative_percentage:.2f}%")

# Run the main function
if __name__ == "__main__":
    main()

