import tkinter as tk

class ExitWithThankYou(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Exit with Thank You")

        self.label = tk.Label(self, text="Thank you for using our program!", font=("Calibri", 20))
        self.label.pack()

        self.button = tk.Button(self, text="Exit", font=("Calibri", 14), command=self.exit_program)
        self.button.pack()

    def exit_program(self):
        self.destroy()
        print("Thank you for using our program!")

if __name__ == "__main__":
    program = ExitWithThankYou()
    program.mainloop()
