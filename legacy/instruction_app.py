import tkinter as tk

def main():
    # Create the main window.
    root = tk.Tk()

    
    # Create a label to display the instructions.

    label = tk.Label(root, text="Welcome To Voice-based Sentiment Analysis (Beta)", font=("Calibri", 14), foreground="red")
    label.pack()

    label = tk.Label(root, text="Instructions:", font=("Calibri", 14))
    label.pack()

    # Create a label to display the instructions.
    label = tk.Label(root, text="1. Press the record button and wait for 'Listening for voice' message in command prompt.", font=("Calibri", 14))
    label.pack()

    # Create a label to display the instructions.
    label = tk.Label(root, text="2. Talk the sentence.", font=("Calibri", 14))
    label.pack()

    # Create a label to display the instructions.
    label = tk.Label(root, text="3. Check the results.", font=("Calibri", 14))
    label.pack()

    tk.Button(text="I Understand", command=tk._exit, font=("Calibri", 14)).pack()


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