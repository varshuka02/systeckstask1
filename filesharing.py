import tkinter as tk
from tkinter import filedialog, messagebox
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


# Constants
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

class FileSharingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Sharing App")
        self.root.geometry("600x500")  

        # Frame to contain login elements
        self.login_frame = tk.Frame(root)
        self.login_frame.pack(pady=20)

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Additional buttons and listbox
        self.upload_button = tk.Button(root, text="Upload File", command=self.upload_file)
        self.upload_button.pack()

        self.download_button = tk.Button(root, text="Download File", command=self.download_file)
        self.download_button.pack()

        self.delete_button = tk.Button(root, text="Delete File", command=self.delete_file)
        self.delete_button.pack()

        self.file_browser_button = tk.Button(root, text="Browse Files", command=self.browse_files)
        self.file_browser_button.pack()

        self.open_button = tk.Button(root, text="Open File", command=self.open_file)
        self.open_button.pack()

        self.close_button = tk.Button(root, text="Close App", command=self.close_app)
        self.close_button.pack(side=tk.BOTTOM)

        self.file_listbox = tk.Listbox(root)
        self.file_listbox.pack()

        self.authenticated_user = None
        self.directory = None
        self.uploaded_files = {} 

    def close_app(self):
        self.root.destroy()

    def login(self):
       
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "varshu" and password == "123!@ab":
            self.authenticated_user = username
            self.show_message("Login successful!")
        else:
            self.show_message("Invalid username or password.")
    # to upload a file
    def upload_file(self):
        if not self.authenticated_user:
            self.show_message("Please log in first.")
            return

        filename = filedialog.askopenfilename(initialdir="/", title="Select file to upload")
        if filename:
            # key for AES encryption
            key = get_random_bytes(16)

            encrypted_data = self.encrypt_file(filename, key)

            self.uploaded_files[os.path.basename(filename)] = (encrypted_data, key)

            self.file_listbox.insert(tk.END, os.path.basename(filename))
            self.show_message("File uploaded successfully.")

     # to download a file
    def download_file(self):
        if not self.authenticated_user:
            self.show_message("Please log in first.")
            return

        selected_file_index = self.file_listbox.curselection()
        if selected_file_index:
            
            file_name = self.file_listbox.get(selected_file_index)

            encrypted_data, key = self.uploaded_files.get(file_name, (None, None))
            if not key:
                self.show_message("File key not found.")
                return

            decrypted_data = self.decrypt_file(encrypted_data, key)

            save_filename = filedialog.asksaveasfilename(initialdir="/", title="Save file", defaultextension=".encrypted")
            if save_filename:
                with open(save_filename, 'wb') as file:
                    file.write(decrypted_data)

            self.show_message(f"File '{file_name}' downloaded and decrypted successfully.")

    # to delete a file
    def delete_file(self):
        if not self.authenticated_user:
            self.show_message("Please log in first.")
            return

        selected_file_index = self.file_listbox.curselection()
        if selected_file_index:
            
            file_name = self.file_listbox.get(selected_file_index)

            self.file_listbox.delete(selected_file_index)

            del self.uploaded_files[file_name]

            self.show_message(f"File '{file_name}' deleted successfully.")

     # to browse a file
    def browse_files(self):
        if not self.authenticated_user:
            self.show_message("Please log in first.")
            return

        self.file_listbox.delete(0, tk.END)
        self.directory = filedialog.askdirectory(initialdir="/", title="Select directory")
        if self.directory:
            files = os.listdir(self.directory)
            for file_name in files:
                self.file_listbox.insert(tk.END, file_name)
     
     # encryption
    def encrypt_file(self, filename, key):
        with open(filename, 'rb') as file:
            data = file.read()
        if len(data) % 16 != 0:
            data += b' ' * (16 - len(data) % 16)
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return ciphertext

    # decryption
    def decrypt_file(self, encrypted_data, key):
        cipher = AES.new(key, AES.MODE_EAX)
        decrypted_data = cipher.decrypt(encrypted_data)
        return decrypted_data

     # to open a file
    def open_file(self):
       if not self.authenticated_user:
          self.show_message("Please log in first.")
          return

       selected_file_index = self.file_listbox.curselection()
       if selected_file_index:
        file_name = self.file_listbox.get(selected_file_index)
        file_path = os.path.join(os.getcwd(), file_name)
        try:
            os.startfile(file_path)
        except OSError as e:
            self.show_message(f"Error opening file: {e}")
       else:
        self.show_message("Please select a file first.")

         
   
    def show_message(self, message):
        messagebox.showinfo("Message", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileSharingApp(root)
    root.mainloop()