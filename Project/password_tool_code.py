import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from zxcvbn import zxcvbn

class PasswordToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Tool")
        self.root.geometry("500x400")
        
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Tab 1: Password Analyzer
        self.analyzer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analyzer_frame, text="Password Analyzer")
        self.setup_analyzer_tab()
        
        # Tab 2: Wordlist Generator
        self.wordlist_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.wordlist_frame, text="Wordlist Generator")
        self.setup_wordlist_tab()
    
    def setup_analyzer_tab(self):
        # Password Entry
        ttk.Label(self.analyzer_frame, text="Enter Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self.analyzer_frame, width=40)
        self.password_entry.pack(pady=5)
        
        # Analyze Button
        ttk.Button(self.analyzer_frame, text="Analyze", command=self.analyze_password).pack(pady=10)
        
        # Results Frame
        self.results_frame = ttk.LabelFrame(self.analyzer_frame, text="Analysis Results")
        self.results_frame.pack(fill='both', padx=10, pady=10)
        
        # Result Labels
        self.score_label = ttk.Label(self.results_frame, text="Strength Score: ")
        self.score_label.pack(anchor='w')
        
        self.time_label = ttk.Label(self.results_frame, text="Crack Time: ")
        self.time_label.pack(anchor='w')
        
        self.warning_label = ttk.Label(self.results_frame, text="Warning: ")
        self.warning_label.pack(anchor='w')
        
        self.suggestions_label = ttk.Label(self.results_frame, text="Suggestions: ")
        self.suggestions_label.pack(anchor='w')
    
    def setup_wordlist_tab(self):
        # Keywords Entry
        ttk.Label(self.wordlist_frame, text="Keywords (comma separated):").pack(pady=5)
        self.keywords_entry = ttk.Entry(self.wordlist_frame, width=40)
        self.keywords_entry.pack(pady=5)
        
        # Years Entry
        ttk.Label(self.wordlist_frame, text="Years (comma separated):").pack(pady=5)
        self.years_entry = ttk.Entry(self.wordlist_frame, width=40)
        self.years_entry.pack(pady=5)
        
        # Generate Button
        ttk.Button(self.wordlist_frame, text="Generate Wordlist", command=self.generate_wordlist).pack(pady=10)
        
        # Save Button
        ttk.Button(self.wordlist_frame, text="Save Wordlist", command=self.save_wordlist).pack(pady=5)
        
        # Wordlist Preview
        self.wordlist_text = tk.Text(self.wordlist_frame, height=10, width=50)
        self.wordlist_text.pack(pady=10)
        
        # Store generated words
        self.generated_words = []
    
    def analyze_password(self):
        password = self.password_entry.get()
        if not password:
            messagebox.showwarning("Warning", "Please enter a password!")
            return
        
        try:
            result = zxcvbn(password)
            
            # Update UI with results
            self.score_label.config(text=f"Strength Score: {result['score']}/4")
            self.time_label.config(text=f"Crack Time: {result['crack_times_display']['online_no_throttling_10_per_second']}")
            self.warning_label.config(text=f"Warning: {result['feedback']['warning'] or 'None'}")
            
            suggestions = "\n".join(result['feedback']['suggestions'])
            self.suggestions_label.config(text=f"Suggestions:\n{suggestions}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
    
    def generate_wordlist(self):
        keywords = self.keywords_entry.get().split(',')
        years = self.years_entry.get().split(',') if self.years_entry.get() else []
        
        if not keywords:
            messagebox.showwarning("Warning", "Please enter at least one keyword!")
            return
        
        # Clean inputs
        keywords = [k.strip() for k in keywords]
        years = [y.strip() for y in years]
        
        # Generate words
        self.generated_words = []
        for keyword in keywords:
            self.generated_words.append(keyword)
            self.generated_words.append(keyword + "123")
            for year in years:
                self.generated_words.append(keyword + year)
        
        # Display in text box
        self.wordlist_text.delete(1.0, tk.END)
        self.wordlist_text.insert(tk.END, "\n".join(self.generated_words))
    
    def save_wordlist(self):
        if not self.generated_words:
            messagebox.showwarning("Warning", "No wordlist generated yet!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Wordlist"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    for word in self.generated_words:
                        f.write(word + "\n")
                messagebox.showinfo("Success", f"Wordlist saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordToolGUI(root)
    root.mainloop()