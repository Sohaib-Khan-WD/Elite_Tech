import tkinter as tk
from tkinter import messagebox

def caesar_cipher(text, shift, mode):
    result = ''
    
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            ascii_offset = 65 if char.isupper() else 97
            if mode == 'encrypt':
                result += chr((ord(char) - ascii_offset + shift_amount) % 26 + ascii_offset)
            elif mode == 'decrypt':
                result += chr((ord(char) - ascii_offset - shift_amount) % 26 + ascii_offset)
        else:
            result += char  
    
    return result

def encrypt():
    try:
        text = text_input.get("1.0", "end-1c")
        shift = int(shift_value.get())
        encrypted_text = caesar_cipher(text, shift, 'encrypt')
        result_text.delete("1.0", "end-1c")
        result_text.insert(tk.END, encrypted_text)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid shift value.")

def decrypt():
    try:
        text = text_input.get("1.0", "end-1c")
        shift = int(shift_value.get())
        decrypted_text = caesar_cipher(text, shift, 'decrypt')
        result_text.delete("1.0", "end-1c")
        result_text.insert(tk.END, decrypted_text)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid shift value.")


root = tk.Tk()
root.title("Caesar Cipher Encryption/Decryption")

tk.Label(root, text="Enter text to encrypt/decrypt:").pack(pady=10)

text_input = tk.Text(root, height=5, width=40)
text_input.pack(pady=5)

tk.Label(root, text="Enter shift value:").pack(pady=10)

shift_value = tk.Entry(root)
shift_value.pack(pady=5)

encrypt_button = tk.Button(root, text="Encrypt", command=encrypt)
encrypt_button.pack(pady=5)

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt)
decrypt_button.pack(pady=5)

tk.Label(root, text="Result:").pack(pady=10)

result_text = tk.Text(root, height=5, width=40)
result_text.pack(pady=5)

root.mainloop()
