import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def validate_data():
    name = name_entry.get()
    age = age_entry.get()
    aicte_id = aicte_id_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    college = college_entry.get()

    # Performing of data validation for possible exceptions 
    if not name or not age_entry or not aicte_id or not email or not phone or not college:
        messagebox.showerror("Error", "Please fill in all fields.")
        return False
    elif not aicte_id.isdigit():
        messagebox.showerror("Error", "AICTE ID must be a numeric value.")
        return False
    
    return True

def generate_pdf():
    if validate_data():
        name = name_entry.get()
        age = age_entry.get()
        aicte_id = aicte_id_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        college = college_entry.get()

        pdf_filename = f"{name}_registration.pdf"

        # Generating the PDF for student registration form
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.drawString(100, 750, "Name: " + name)
        c.drawString(100, 690, "Age: " + age)
        c.drawString(100, 730, "AICTE ID: " + aicte_id)
        c.drawString(100, 710, "Email: " + email)
        c.drawString(100, 690, "Phone: " + phone)
        c.drawString(100, 670, "College: " + college)
        c.save()

        messagebox.showinfo("Success", "PDF generated successfully.")

# GUI
root = tk.Tk()
root.title("Student Registration Form")

# Labels 
tk.Label(root, text="Name:").grid(row=0, column=0, sticky="e")
tk.Label(root, text="Age:").grid(row=1, column=0, sticky="e")
tk.Label(root, text="AICTE ID:").grid(row=2, column=0, sticky="e")
tk.Label(root, text="Email:").grid(row=3, column=0, sticky="e")
tk.Label(root, text="Phone no.:").grid(row=4, column=0, sticky="e")
tk.Label(root, text="College name:").grid(row=5, column=0, sticky="e")

# Entry of different  fields we require
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)
age_entry = tk.Entry(root)
age_entry.grid(row=1, column=1)
aicte_id_entry = tk.Entry(root)
aicte_id_entry.grid(row=2, column=1)
email_entry = tk.Entry(root)
email_entry.grid(row=3, column=1)
phone_entry = tk.Entry(root)
phone_entry.grid(row=4, column=1)
college_entry = tk.Entry(root)
college_entry.grid(row=5, column=1)

# Submition button
submit_button = tk.Button(root, text="Generate PDF", command=generate_pdf)
submit_button.grid(row=6, columnspan=2)

root.mainloop()