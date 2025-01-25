
import tkinter as tk
from tkinter import messagebox
import re
import math

def password_strength(password):
    length = len(password)
    has_uppercase = bool(re.search(r'[A-Z]', password))
    has_lowercase = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_special_char = bool(re.search(r'[@$!%*?&]', password))
    
    strength = 0
    feedback = []

    if length >= 8:
        strength += 1
    else:
        feedback.append("Password should be at least 8 characters long.")
    
    if has_uppercase:
        strength += 1
    else:
        feedback.append("Include at least one uppercase letter.")
    
    if has_lowercase:
        strength += 1
    else:
        feedback.append("Include at least one lowercase letter.")
    
    if has_digit:
        strength += 1
    else:
        feedback.append("Include at least one number.")
    
    if has_special_char:
        strength += 1
    else:
        feedback.append("Include at least one special character (@$!%*?&).")
    
    strength_percentage = (strength / 5) * 100
    
    estimated_crack_time = estimate_crack_time(password)

    if strength == 5:
        result = "Password is strong. Good job!"
    elif strength == 4:
        result = "Password is medium strength. Consider adding more variety."
    else:
        result = "Password is weak. Please follow the recommendations."
    
    return result, feedback, strength_percentage, estimated_crack_time

def estimate_crack_time(password):
    char_set = 26 + 26 + 10 + 32  
    length = len(password)
    
    total_combinations = char_set ** length

    attack_rate = 1e9  
    crack_time_seconds = total_combinations / attack_rate
    
    if crack_time_seconds < 60:
        return f"{crack_time_seconds:.2f} seconds"
    elif crack_time_seconds < 3600:
        return f"{crack_time_seconds / 60:.2f} minutes"
    elif crack_time_seconds < 86400:
        return f"{crack_time_seconds / 3600:.2f} hours"
    else:
        return f"{crack_time_seconds / 86400:.2f} days"

def check_password():
    password = password_entry.get()
    
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password.")
        return
    
    result, recommendations, strength_percentage, crack_time = password_strength(password)
    
    result_label.config(text=f"{result} ({strength_percentage:.2f}% strength)")
    recommendations_text.delete(1.0, tk.END)
    
    if recommendations:
        recommendations_text.insert(tk.END, "\n".join(recommendations))
    else:
        recommendations_text.insert(tk.END, "Your password meets all the requirements!")
    
    crack_time_label.config(text=f"Estimated crack time: {crack_time}")

def toggle_password():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        show_password_button.config(text='🙈') 
    else:
        password_entry.config(show='*')
        show_password_button.config(text='👁️')  

root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("600x500")

instructions_label = tk.Label(root, text="Enter your password below:", font=("Arial", 12))
instructions_label.pack(pady=10)

password_entry = tk.Entry(root, show="*", font=("Arial", 12), width=30)
password_entry.pack(pady=10)

show_password_button = tk.Button(root, text="👁️", font=("Arial", 12), bd=0, command=toggle_password)
show_password_button.place(x=510, y=210)

check_button = tk.Button(root, text="Check Strength", font=("Arial", 12), command=check_password)
check_button.pack(pady=20)

result_label = tk.Label(root, text="", font=("Arial", 14), fg="green")
result_label.pack(pady=10)

recommendations_text = tk.Text(root, height=5, width=40, font=("Arial", 10), wrap=tk.WORD)
recommendations_text.pack(pady=10)

crack_time_label = tk.Label(root, text="", font=("Arial", 12), fg="red")
crack_time_label.pack(pady=10)

root.mainloop()
