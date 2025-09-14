import tkinter as tk

def main():
    # Create the main window.
    root = tk.Tk()

    # Create a label to display the instructions.
    
    label = tk.Label(root, text="Disclaimer:", font=("Calibri", 14), foreground="red")
    label.pack()

    # Create a label to display the instructions.
    label = tk.Label(root, text="1. Voice-based sentiment analysis understands Marathi, Hindi & English language.", font=("Calibri", 14))
    label.pack()
    
    # Create a label to display the instructions.
    label = tk.Label(root, text="2. Sentiment analysis is currently done only on the English language.", font=("Calibri", 14))
    label.pack()

    # Create a label to display the instructions.
    label = tk.Label(root, text="3. After viewing results, remember to click the 'Clear' button before entering the next entry.", font=("Calibri", 14))
    label.pack()

    # Create a label to display the instructions.
    label = tk.Label(root, text="4. Results may vary or be inaccurate in some cases.", font=("Calibri", 14))
    label.pack()

    tk.Button(text="I Agree", command=tk._exit, font=("Calibri", 14)).pack()


    # Enter the main event loop.
    root.mainloop()

def format_text():
    # Get the selected text.
    text = listbox.get("active")

    # Format the text.
    formatted_text = text.replace(" ", "_")

    # Display the formatted text.
    label.config(text=formatted_text)

if __name__ == "__main__":
    main()