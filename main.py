import os
from cryptography.fernet import Fernet, InvalidToken
from tkinter import *
from tkinter import filedialog
from functools import partial
import time
import threading

# Global variables
global filename
button_height = 2
button_width = 25

def browseFiles():
    # Function to browse and select a file
    browseFiles.filename = filedialog.askopenfilename(initialdir="/home/daddy", title="Select a File")
    label_file_explorer.configure(text="File Opened: " + os.path.basename(browseFiles.filename))
    
    # Reset buttons and status label
    reset_to_initial_state()
    check_file_encryption()

def check_file_encryption():
    # Function to check if the selected file is encrypted
    with open(browseFiles.filename, 'rb') as file:
        content = file.read()
    if content.startswith(b'gAAAAAB'):
        # File is encrypted
        status_label.configure(text=f"File: {os.path.basename(browseFiles.filename)} is encrypted")
        status_label.pack(pady=(10, 0))  # Add padding above the status label
        pass_label.configure(text="Type password to decrypt the file:")
        pass_label.pack()
        password.pack()
        button_decrypt.pack(pady=(20, 0))  # Add padding above the decrypt button
    else:
        # File is not encrypted
        status_label.configure(text=f"File: {os.path.basename(browseFiles.filename)} is not encrypted. You can encrypt it.")
        status_label.pack(pady=(10, 0))  # Add padding above the status label
        pass_label.configure(text="Type password to encrypt the file:")
        pass_label.pack()
        password.pack()
        button_encrypt.pack(pady=(20, 0))  # Add padding above the encrypt button

def generate_key(p_word):
    # Function to generate a key from the password
    temp_key = p_word.get()
    if not temp_key:
        return None
    temp_key = ''.join(e for e in temp_key if e.isalnum())
    return temp_key + ("s" * (43 - len(temp_key)) + "=")

def reset_to_initial_state():
    # Function to reset the UI to the initial state
    button_encrypt.pack_forget()
    button_decrypt.pack_forget()
    status_label.pack_forget()
    pass_label.pack_forget()
    password.pack_forget()
    password.delete(0, END)  # Clear the password field

def encrypt_file(p_word):
    # Function to encrypt the selected file
    key = generate_key(p_word)
    if key is None:
        status_label.configure(text="Password is required for encryption.")
        status_label.pack(pady=(10, 0))  # Add padding above the status label
        return

    fernet = Fernet(key)

    with open(browseFiles.filename, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)
    with open(browseFiles.filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    status_label.configure(text=f"Encryption completed for file: {os.path.basename(browseFiles.filename)}")
    status_label.pack(pady=(10, 0))  # Add padding above the status label
    
    # Use threading to implement the delay
    threading.Thread(target=delayed_reset).start()

def decrypt_file(p_word):
    # Function to decrypt the selected file
    key = generate_key(p_word)
    if key is None:
        status_label.configure(text="Password is required for decryption.")
        status_label.pack(pady=(10, 0))  # Add padding above the status label
        return

    fernet = Fernet(key)

    with open(browseFiles.filename, 'rb') as enc_file:
        encrypted = enc_file.read()
    try:
        decrypted = fernet.decrypt(encrypted)
        with open(browseFiles.filename, 'wb') as dec_file:
            dec_file.write(decrypted)
        status_label.configure(text=f"File: {os.path.basename(browseFiles.filename)}\n Decryption Completed")
    except InvalidToken:
        status_label.configure(text="Decryption failed. Incorrect password or file is not encrypted.")
    status_label.pack(pady=(10, 0))  # Add padding above the status label
    
    # Use threading to implement the delay
    threading.Thread(target=delayed_reset).start()

def delayed_reset():
    # Function to add a delay before resetting to the initial state
    time.sleep(5)
    reset_to_initial_state()
    label_file_explorer.configure(text="File Opened: " + os.path.basename(browseFiles.filename))
    check_file_encryption()

# Main window
window = Tk()

# Set window title, size, and background color
window.title('project_cryptus')
window.geometry("840x740")
window.config(background="black")

# Main title of the application
main_title = Label(window, text="Encryptor & Decryptor", width=100, height=2, fg="#00BFFF", bg="black", font=("", 30))

# Variable to store password
passwd = StringVar()

# Create partial functions for encrypt and decrypt buttons
submit_para_en = partial(encrypt_file, passwd)
submit_para_de = partial(decrypt_file, passwd)

# Credit label
credit = Label(window, text="Developed by Pankaj Kushwaha", bg="black", height=2, fg="#FFC0CB", font=("", 12))

# Label to show file explorer instructions
label_file_explorer = Label(window, text="Open the file that you want to Encrypt or Decrypt: ", width=100, height=2, fg="white", bg="black", font=("", 11))

# Label for password instructions
pass_label = Label(window, text=" Enter password for Encryption|Decryption : ", width=100, height=2, fg="white", bg="black", font=("", 15))

# Temporary label for spacing
temp_label = Label(window, text="", height=3, bg="black")

# Button to browse files
button_explore = Button(window, text="Browse File", command=browseFiles, width=button_width, height=button_height, font=("", 14))

# Entry field for password input
password = Entry(window, textvariable=passwd, show="*")

# Buttons for encryption and decryption
button_encrypt = Button(window, text="Encrypt", command=submit_para_en, width=button_width, height=button_height, font=("", 14))
button_decrypt = Button(window, text="Decrypt", command=submit_para_de, width=button_width, height=button_height, font=("", 14))

# Label to display status messages
status_label = Label(window, text="", width=100, height=4, fg="white", bg="black", font=("", 17))

# Pack all the components into the window
credit.pack()
main_title.pack()
label_file_explorer.pack()
button_explore.pack()
window.mainloop()
