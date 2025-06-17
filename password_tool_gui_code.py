import tkinter as tk
from tkinter import messagebox
from zxcvbn import zxcvbn

def analyze_password():
    password = entry.get()
    result = zxcvbn( password )
    message = (
        f"Password: { password }\n"
        f"Strength: {result['score']}/4\n"
        f"Crack Time: {result['crack_times_display']['online_no_throttling_10_per_second']}\n"
        f"Warning: {result['feedback']['warning'] or 'None'}"
    )
    messagebox.showinfo(" Password Analysis ", message)

# Create the window
root = tk.Tk()
root.title(" Password Analyzer ")

# Add input field
label = tk.Label(root, text=" Enter Password:")
label.pack()
entry = tk.Entry(root, width=50)
entry.pack()

# Add analyze button
button = tk.Button(root, text=" Analyze ", command=analyze_password)
button.pack()

root.mainloop()