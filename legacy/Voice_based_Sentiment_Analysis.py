from tkinter import Tk, Label, Text, Button, Toplevel, messagebox
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import speech_recognition as sr

recognizer = sr.Recognizer()  # Initialize recognizer object

def analyze_sentiment():
    global text_area
    text = text_area.get("1.0", "end-1c")  # Get text from the text area

    # Detect language and perform sentiment analysis accordingly
    language = detect_language(text)

    if language == 'en':
        analyze_sentiment_english(text)
    elif language == 'mr':
        analyze_sentiment_marathi(text)
    elif language == 'hi':
        analyze_sentiment_hindi(text)
    else:
        messagebox.showinfo("Unsupported Language", "Unsupported language for sentiment analysis.")

def analyze_sentiment_english(text):
    analyser = SentimentIntensityAnalyzer()
    v = analyser.polarity_scores(text)
    compound_score = v['compound']

    if compound_score >= 0.05:
        sentiment = 'Positive'
    elif compound_score <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    result_label.config(text=f'Sentiment: {sentiment}')
    show_summary_window(text, v)

def analyze_sentiment_marathi(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity

    if sentiment >= 0.05:
        sentiment_category = 'Positive'
    elif sentiment <= -0.05:
        sentiment_category = 'Negative'
    else:
        sentiment_category = 'Neutral'

    result_label.config(text=f'Sentiment: {sentiment_category}')
    show_summary_window(text, None)  # TextBlob does not provide detailed scores

def analyze_sentiment_hindi(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity

    if sentiment >= 0.05:
        sentiment_category = 'Positive'
    elif sentiment <= -0.05:
        sentiment_category = 'Negative'
    else:
        sentiment_category = 'Neutral'

    result_label.config(text=f'Sentiment: {sentiment_category}')
    show_summary_window(text, None)  # TextBlob does not provide detailed scores

def record_audio(language='en-US'):
    global recognizer
    with sr.Microphone() as source:
        print('')
        print('Clearing background noise...')
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print('Listening for voice...')
        recorded_audio = recognizer.listen(source)

        try:
            print('Printing the message..')
            text = recognizer.recognize_google(recorded_audio, language=language)
            text_area.delete("1.0", "end")  # Clear the current text
            text_area.insert("1.0", text)   # Insert the recognized text
            print(f'Your message ({language}): {text}')
        except Exception as ex:
            print(ex)

def clear_text():
    global text_area
    text_area.delete("1.0", "end")  # Clear the text area

def show_summary_window(sentence, sentiment_scores):
    summary_window = Toplevel(root)
    summary_window.title("Detailed Summary")

    # Create a Label widget to display the sentiment analysis output
    summary_label = Label(summary_window, text="", wraplength=400, font=('Helvetica', 12))
    summary_label.pack(expand=True, fill='both')

    # Display positivity, negativity, and neutrality ratios
    if sentiment_scores:
        positivity_ratio = sentiment_scores['pos'] * 100
        negativity_ratio = sentiment_scores['neg'] * 100
        neutrality_ratio = sentiment_scores['neu'] * 100

        summary_label.config(text=f"Sentence: {sentence}\n\n"
                                  f"Positivity Ratio: {positivity_ratio:.2f}%\n"
                                  f"Negativity Ratio: {negativity_ratio:.2f}%\n"
                                  f"Neutrality Ratio: {neutrality_ratio:.2f}%\n\n")
    else:
        summary_label.config(text=f"Sentence: {sentence}\n\n")

    # Display sentiment category based on compound score or TextBlob sentiment
    if sentiment_scores:
        if sentiment_scores['compound'] >= 0.05:
            sentiment_category = 'Positive'
        elif sentiment_scores['compound'] <= -0.05:
            sentiment_category = 'Negative'
        else:
            sentiment_category = 'Neutral'
    else:
        sentiment_category = None

    summary_label.config(text=f"{summary_label.cget('text')}Overall Sentiment: {sentiment_category}")

def exit_program():
    if messagebox.askyesno("Exit", "Do you want to exit the program?"):
        root.destroy()

def detect_language(text):
    # Perform simple language detection based on character range
    for char in text:
        if 'a' <= char <= 'z':
            return 'en'
        elif 'ँ' <= char <= 'ः':
            return 'hi'
        elif 'ऄ' <= char <= 'अ':
            return 'hi'
        elif 'आ' <= char <= 'ऋ':
            return 'hi'
        elif 'ऍ' <= char <= 'ऎ':
            return 'hi'
        elif 'ए' <= char <= 'ऑ':
            return 'hi'
        elif 'ऒ' <= char <= 'ओ':
            return 'hi'
        elif 'औ' <= char <= 'ह':
            return 'hi'
        elif 'ा' <= char <= '्':
            return 'hi'
        elif 'ॐ' <= char <= 'ॡ':
            return 'hi'
        elif 'ॢ' <= char <= 'ॣ':
            return 'hi'
        elif '।' <= char <= '॥':
            return 'hi'
        elif '०' <= char <= '९':
            return 'hi'
        elif '॰' <= char <= 'ॿ':
            return 'hi'
        elif 'ঀ' <= char <= 'ঃ':
            return 'hi'
        elif 'অ' <= char <= 'ঋ':
            return 'hi'
        elif 'ঌ' <= char <= 'এ':
            return 'hi'
        elif 'ঐ' <= char <= 'ও':
            return 'hi'
        elif 'ঔ' <= char <= 'হ':
            return 'hi'
        elif 'া' <= char <= '্':
            return 'hi'
        elif 'ৎ' <= char <= 'ৗ':
            return 'hi'
        elif 'ড়' <= char <= 'ঢ়':
            return 'hi'
        elif 'য়' <= char <= 'ৠ':
            return 'hi'
        elif 'ৡ' <= char <= 'ৢ':
            return 'hi'
        elif 'ৣ' <= char <= '৤':
            return 'hi'
        elif '৥' <= char <= '৮':
            return 'hi'
        elif 'ৰ' <= char <= '৳':
            return 'hi'
        elif '৴' <= char <= '৻':
            return 'hi'
        elif '༁' <= char <= '༂':
            return 'hi'
        elif '༃' <= char <= '༄':
            return 'hi'
        elif '༅' <= char <= '༈':
            return 'hi'
        elif '༉' <= char <= '༝':
            return 'hi'
        elif '༞' <= char <= '༟':
            return 'hi'
        elif '༠' <= char <= '༣':
            return 'hi'
        elif '༤' <= char <= '༦':
            return 'hi'
        elif '༦' <= char <= '༧':
            return 'hi'
        elif '༨' <= char <= '༩':
            return 'hi'
        elif '༪' <= char <= '༫':
            return 'hi'
        elif '༬' <= char <= '༯':
            return 'hi'
        elif '༰' <= char <= '༴':
            return 'hi'
        elif '༵' <= char <= '༷':
            return 'hi'
        elif '༸' <= char <= '༺':
            return 'hi'
        elif '༻' <= char <= '༼':
            return 'hi'
        elif '༽' <= char <= 'ྃ':
            return 'hi'
        elif '྄' <= char <= '྅':
            return 'hi'
        elif '྆' <= char <= '྇':
            return 'hi'
        elif 'ྈ' <= char <= 'ྉ':
            return 'hi'
        elif 'ྊ' <= char <= 'ྋ':
            return 'hi'
        elif 'ྌ' <= char <= 'ྏ':
            return 'hi'
        elif 'ྐ' <= char <= 'ྙ':
            return 'hi'
        elif 'ྚ' <= char <= 'ྜ':
            return 'hi'
        elif 'ྜྷ' <= char <= 'ྞ':
            return 'hi'
        elif 'ྟ' <= char <= 'ྡ':
            return 'hi'
        elif 'ྡྷ' <= char <= 'ྣ':
            return 'hi'
        elif 'ྤ' <= char <= 'ྥ':
            return 'hi'
        elif 'ྦ' <= char <= 'ྼ':
            return 'hi'
        elif '྾' <= char <= '྿':
            return 'hi'
        elif '၀' <= char <= 'ႇ':
            return 'hi'
        elif 'ក' <= char <= '៛':
            return 'hi'
        elif '၀' <= char <= '၏':
            return 'hi'
        elif 'ᠠ' <= char <= 'ᠾ':
            return 'hi'
        elif 'ᡀ' <= char <= 'ᡯ':
            return 'hi'
        elif 'ᢀ' <= char <= 'ᢲ':
            return 'hi'
        elif 'ᣀ' <= char <= 'ᣠ':
            return 'hi'
        elif 'ᣰ' <= char <= '᣾':
            return 'hi'

# Create the main window
root = Tk()
root.title("Sentiment Analysis App")

# Text area for input
text_area = Text(root, width=40, height=5, wrap="word", font=('Helvetica', 12))
text_area.pack(pady=10)

# Button to trigger speech recognition in English
record_button_en = Button(root, text="Record Audio (English)", command=lambda: record_audio('en-US'), font=('Helvetica', 12))
record_button_en.pack(pady=5)

# Button to trigger speech recognition in Marathi
record_button_mr = Button(root, text="Record Audio (Marathi)", command=lambda: record_audio('mr-IN'), font=('Helvetica', 12))
record_button_mr.pack(pady=5)

# Button to trigger speech recognition in Hindi
record_button_hi = Button(root, text="Record Audio (Hindi)", command=lambda: record_audio('hi-IN'), font=('Helvetica', 12))
record_button_hi.pack(pady=5)

# Button to trigger sentiment analysis
analyze_button = Button(root, text="Analyze Sentiment", command=analyze_sentiment, font=('Helvetica', 12))
analyze_button.pack(pady=10)

# Button to clear the previous entry
clear_button = Button(root, text="Clear", command=clear_text, font=('Helvetica', 12))
clear_button.pack(pady=10)

# Button to exit the program
exit_button = Button(root, text="Exit", command=exit_program, font=('Helvetica', 12))
exit_button.pack(pady=10)

# Label to display sentiment result
result_label = Label(root, text="Sentiment: ", font=('Helvetica', 14, 'italic'))
result_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()