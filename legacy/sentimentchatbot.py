from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

def detect_sentiment(input_text):
    if not input_text.strip():
        return "Please enter a paragraph."

    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(input_text)

    overall_sentiment = "positive" if sentiment_dict['compound'] >= 0 else "negative"

    if sentiment_dict['compound'] == 0:
        sentiment_statement = "The sentiment of the text is neutral."
    else:
        positive_words = []
        negative_words = []

        words = input_text.split()
        for word in words:
            word_sentiment = sid_obj.polarity_scores(word)['compound']
            if word_sentiment > 0:
                positive_words.append((word, word_sentiment))
            elif word_sentiment < 0:
                negative_words.append((word, word_sentiment))

        positive_str = ", ".join([f"{word} ({score:.2f})" for word, score in positive_words]) if positive_words else "no positive sentiment detected"
        negative_str = ", ".join([f"{word} ({score:.2f})" for word, score in negative_words]) if negative_words else "no negative sentiment detected"

        sentiment_statement = f"The overall sentiment of the text is {overall_sentiment}.\n\n"
        sentiment_statement += f"Positive words: {positive_str}\n\n"
        sentiment_statement += f"Negative words: {negative_str}\n\n"

        if overall_sentiment == "positive":
            sentiment_reason = "The sentiment is positive because it contains more positive words."
        else:
            sentiment_reason = "The sentiment is negative because it contains more negative words."

        sentiment_statement += f"Summary Report:\n{sentiment_reason}"

    response_message = f"The sentiment analysis results indicate: {sentiment_statement}"

    return response_message

def send_message():
    input_text = entry.get()
    entry.delete(0, END)
    if not input_text.strip():
        messagebox.showwarning("Empty Input", "Please enter a paragraph.")
        return

    response = detect_sentiment(input_text)

    chat_history.config(state=NORMAL)
    chat_history.insert(END, "You: " + input_text + "\n\n", "user_message")
    chat_history.insert(END, "Chatbot:\n" + response + "\n\n", "chatbot_message")
    chat_history.config(state=DISABLED)
    chat_history.see(END)

def save_chat():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filename:
        try:
            with open(filename, "w") as file:
                file.write(chat_history.get("1.0", END))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {str(e)}")

def clear_chat():
    chat_history.config(state=NORMAL)
    chat_history.delete("1.0", END)
    chat_history.config(state=DISABLED)

def clear_text():
    entry.delete(0, END)

def exit_chat():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        gui.destroy()

def display_welcome_message():
    welcome_message = "Welcome to the Sentiment Analysis Chatbot!\n\n"
    instructions = "Instructions:\n1. Enter a paragraph in the text box below.\n2. Click 'Send' to analyze the sentiment.\n3. Use 'Save' to save the chat history.\n4. Use 'Clear Chat' to clear the chat history.\n5. Use 'Exit' to close the application.\n\n"
    use_case = "Use Case:\nYou can use this chatbot to analyze the sentiment of any text, such as product reviews, social media posts, or personal messages.\n"
    limitations = "Current Limitation:\nThis chatbot performs basic sentiment analysis and may not accurately interpret context or nuanced language.\n"
    chat_history.config(state=NORMAL)
    chat_history.insert(END, "Chatbot: " + welcome_message + instructions + use_case + limitations + "\n\n", "chatbot_message")
    chat_history.config(state=DISABLED)

if __name__ == "__main__":
    gui = Tk()
    gui.title("Sentiment Analysis Chatbot")
    gui.geometry("400x500")
    gui.configure(bg="#f7f7f7")

    chat_history = Text(gui, width=40, height=20, wrap=WORD, state=DISABLED, bg="#ffffff", fg="#333333", font=("Helvetica", 12))
    chat_history.tag_config("user_message", foreground="#007bff")  # Set user message color
    chat_history.tag_config("chatbot_message", foreground="#28a745")  # Set chatbot message color
    chat_history.pack(expand=True, fill=BOTH, padx=10, pady=10)

    entry_frame = Frame(gui, bg="#f7f7f7")
    entry_frame.pack(fill=X, padx=10, pady=(0, 10))

    entry = Entry(entry_frame, width=40, bg="#ffffff", fg="#333333", font=("Helvetica", 12))
    entry.pack(side=LEFT, expand=True, fill=X, padx=(0, 5))

    send_button = Button(entry_frame, text="Send", command=send_message, bg="#007bff", fg="#ffffff", font=("Helvetica", 12))
    send_button.pack(side=LEFT)

    save_button = Button(gui, text="Save", command=save_chat, bg="#007bff", fg="#ffffff", font=("Helvetica", 12))
    save_button.pack(side=LEFT, padx=(10, 5))

    clear_chat_button = Button(gui, text="Clear Chat", command=clear_chat, bg="#007bff", fg="#ffffff", font=("Helvetica", 12))
    clear_chat_button.pack(side=LEFT, padx=(10, 5))

    clear_text_button = Button(gui, text="Clear Text", command=clear_text, bg="#007bff", fg="#ffffff", font=("Helvetica", 10))
    clear_text_button.pack(side=LEFT, padx=(10, 5))

    exit_button = Button(gui, text="Exit", command=exit_chat, bg="#dc3545", fg="#ffffff", font=("Helvetica", 12))
    exit_button.pack(side=LEFT)

    display_welcome_message()

    gui.mainloop()

