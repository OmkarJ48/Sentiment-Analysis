# Import SentimentIntensityAnalyzer class from vaderSentiment.vaderSentiment module.
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tkinter import messagebox
from tkinter import *

# Function for clearing the contents of all entry boxes and text area.
def clearAll():
    textArea.delete(1.0, END)

# Function to print sentiments of the sentence.
def detect_sentiment():
    full_text = textArea.get("1.0", "end")
    # Extract the first five lines from the entered text
    first_five_lines = '\n'.join(full_text.split('\n')[:5])

    if not first_five_lines.strip():
        messagebox.showwarning("Input Error", "Please enter a paragraph.")
        return

    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(first_five_lines)

    # Display a summary report with the entered text
    report = f"Sentiment Analysis Summary for the entered paragraph:\n\n{first_five_lines}\n\nNegative: {sentiment_dict['neg']*100:.2f}%\nNeutral: {sentiment_dict['neu']*100:.2f}%\nPositive: {sentiment_dict['pos']*100:.2f}%\nOverall: {'Positive' if sentiment_dict['compound'] >= 0 else 'Negative' if sentiment_dict['compound'] <= 0 else 'Neutral'}"
    messagebox.showinfo("Sentiment Analysis Report", report)

# Driver Code
if __name__ == "__main__":
    gui = Tk()
    gui.config(background="light blue")
    gui.title("Sentiment Analysis")
    gui.geometry("400x500")

    enterText = Label(gui, text="Enter Your Paragraph", font=("Calibri", 12), bg="light blue")
    textArea = Text(gui, height=10, width=40, font="lucida 12")
    check = Button(gui, text="Check Sentiment", font=("Calibri", 12), fg="Black", bg="Red", command=detect_sentiment)
    clear = Button(gui, text="Clear", fg="Black", font=("Calibri", 12), bg="Red", command=clearAll)
    Exit = Button(gui, text="Exit", fg="Black", font=("Calibri", 12), bg="Red", command=exit)

    enterText.grid(row=0, column=2, pady=10)
    textArea.grid(row=1, column=2, padx=10, pady=10, sticky=W)
    check.grid(row=2, column=2, pady=10)
    clear.grid(row=3, column=2, pady=10)
    Exit.grid(row=4, column=2, pady=10)

    gui.mainloop()
