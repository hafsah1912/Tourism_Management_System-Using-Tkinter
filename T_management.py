import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

# Establish connection to MySQL database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='', 
    database='projectTTMS',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# Function to check customer login
def check_login(name, email):
    cur = connection.cursor()
    cur.execute("SELECT * FROM Customer WHERE customer_name = %s AND customer_email = %s", (name, email))
    customer = cur.fetchone()
    if customer:
        return True
    else:
        return False

# Function to register a new customer
def register_customer(customer_id, name, email, phone):
    try:
        cur = connection.cursor()
        cur.execute("INSERT INTO Customer (customer_id, customer_name, customer_email, customer_phone) VALUES (%s, %s, %s, %s)",
                    (customer_id, name, email, phone))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error in registration: {e}")
        return False

# Function to display tour packages
def display_tour_packages():
    root = tk.Tk()
    root.title("Tour Packages")
    root.geometry('800x500')
    
    cur = connection.cursor()
    cur.execute("SELECT * FROM Tour_Package")
    packages = cur.fetchall()
    
    for i, package in enumerate(packages):
        package_info = f"Package Name: {package['package_name']}\nDescription: {package['package_description']}\nPrice: {package['package_price']}\nDuration: {package['package_duration']} days"
        tk.Label(root, text=package_info, wraplength=600, justify='left').grid(row=i, column=0, padx=10, pady=10, sticky='w')
    
    root.mainloop()

# Function to book a tour
def book_tour():
    def book_function():
        package_name = package_name_entry.get()
        customer_name = customer_name_entry.get()
        transport_type = transport_type_entry.get()
        hotel_name = hotel_name_entry.get()
        place_name = place_name_entry.get()
        booking_date = booking_date_entry.get()

        if not (package_name and customer_name and transport_type and hotel_name and place_name and booking_date):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        try:
            cur = connection.cursor()
            cur.execute("SELECT package_id FROM Tour_Package WHERE package_name = %s", (package_name,))
            package_id = cur.fetchone()['package_id']

            cur.execute("SELECT customer_id FROM Customer WHERE customer_name = %s", (customer_name,))
            customer_id = cur.fetchone()['customer_id']

            cur.execute("SELECT transport_id FROM Transport WHERE transport_type = %s", (transport_type,))
            transport_id = cur.fetchone()['transport_id']

            cur.execute("SELECT hotel_id FROM Hotel WHERE hotel_name = %s", (hotel_name,))
            hotel_id = cur.fetchone()['hotel_id']

            cur.execute("SELECT place_id FROM Tourism_Place WHERE place_name = %s", (place_name,))
            place_id = cur.fetchone()['place_id']

            cur.execute("INSERT INTO Tour_Booking (package_id, customer_id, transport_id, hotel_id, place_id, booking_date, booking_total_price, booking_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (package_id, customer_id, transport_id, hotel_id, place_id, booking_date, '5000', 'Confirmed'))
            connection.commit()
            
            messagebox.showinfo("Booking Successful", "Your tour has been booked!")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    root = tk.Tk()
    root.title("Book Tour")
    root.geometry('400x400')
    
    tk.Label(root, text="Package Name:", padx=10, pady=5).grid(row=0, column=0, sticky='w')
    package_name_entry = ttk.Combobox(root, values=get_package_names())
    package_name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Customer Name:", padx=10, pady=5).grid(row=1, column=0, sticky='w')
    customer_name_entry = ttk.Combobox(root, values=get_customer_names())
    customer_name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Transport Type:", padx=10, pady=5).grid(row=2, column=0, sticky='w')
    transport_type_entry = ttk.Combobox(root, values=get_transport_types())
    transport_type_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Hotel Name:", padx=10, pady=5).grid(row=3, column=0, sticky='w')
    hotel_name_entry = ttk.Combobox(root, values=get_hotel_names())
    hotel_name_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(root, text="Place Name:", padx=10, pady=5).grid(row=4, column=0, sticky='w')
    place_name_entry = ttk.Combobox(root, values=get_place_names())
    place_name_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(root, text="Booking Date (YYYY-MM-DD):", padx=10, pady=5).grid(row=5, column=0, sticky='w')
    booking_date_entry = tk.Entry(root)
    booking_date_entry.grid(row=5, column=1, padx=10, pady=5)

    book_button = tk.Button(root, text="Book Tour", command=book_function, padx=10, pady=5, bg='lightblue', fg='black', relief=tk.RAISED)
    book_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
    book_button.bind("<Enter>", lambda event: book_button.config(bg="lightgreen"))  # Hover effect
    book_button.bind("<Leave>", lambda event: book_button.config(bg="lightblue"))  # Hover effect

    root.mainloop()

# Function to get package names
def get_package_names():
    cur = connection.cursor()
    cur.execute("SELECT package_name FROM Tour_Package")
    packages = cur.fetchall()
    return [package['package_name'] for package in packages]

# Function to get customer names
def get_customer_names():
    cur = connection.cursor()
    cur.execute("SELECT customer_name FROM Customer")
    customers = cur.fetchall()
    return [customer['customer_name'] for customer in customers]

# Function to get transport types
def get_transport_types():
    cur = connection.cursor()
    cur.execute("SELECT DISTINCT transport_type FROM Transport")
    transports = cur.fetchall()
    return [transport['transport_type'] for transport in transports]

# Function to get hotel names
def get_hotel_names():
    cur = connection.cursor()
    cur.execute("SELECT hotel_name FROM Hotel")
    hotels = cur.fetchall()
    return [hotel['hotel_name'] for hotel in hotels]

# Function to get place names
def get_place_names():
    cur = connection.cursor()
    cur.execute("SELECT place_name FROM Tourism_Place")
    places = cur.fetchall()
    return [place['place_name'] for place in places]

# Function to handle customer login
def login():
    def validate_login():
        name = reg_name_entry.get()
        email = email_entry.get()
        if check_login(name,email):
            messagebox.showinfo("Login Successful", "Welcome!")
            main_menu()
            login_root.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register():
        name = reg_name_entry.get()
        email = reg_email_entry.get()
        phone = reg_phone_entry.get()
        customer_id = reg_customer_id_entry.get()  # New field

        if not (customer_id and name and email and phone):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if register_customer(customer_id, name, email, phone):
            messagebox.showinfo("Registration Successful", "You have been registered successfully!")
        else:
            messagebox.showerror("Registration Failed", "Failed to register. Please try again.")

    login_root = tk.Tk()
    login_root.title("Customer Login")
    login_root.geometry('600x400')  # Increase the width

    # Login Frame
    login_frame = ttk.Frame(login_root)
    login_frame.pack(pady=10)

    ttk.Label(login_frame, text="Name :").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    name_entry = ttk.Entry(login_frame)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(login_frame, text="Email:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    email_entry = ttk.Entry(login_frame, show="*")
    email_entry.grid(row=1, column=1, padx=10, pady=5)

    login_button = ttk.Button(login_frame, text="Login", command=validate_login)
    login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Registration Frame
    register_frame = ttk.Frame(login_root)
    register_frame.pack(pady=10)

    ttk.Label(register_frame, text="Customer ID:").grid(row=5, column=0, padx=10, pady=5, sticky='w')
    reg_customer_id_entry = ttk.Entry(register_frame)  # New field
    reg_customer_id_entry.grid(row=5, column=1, padx=10, pady=5)


    ttk.Label(register_frame, text="Name:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
    reg_name_entry = ttk.Entry(register_frame)
    reg_name_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(register_frame, text="Email:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
    reg_email_entry = ttk.Entry(register_frame)
    reg_email_entry.grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(register_frame, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    reg_password_entry = ttk.Entry(register_frame, show="*")
    reg_password_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(register_frame, text="Phone:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
    reg_phone_entry = ttk.Entry(register_frame)
    reg_phone_entry.grid(row=4, column=1, padx=10, pady=5)
    
    register_button = ttk.Button(register_frame, text="Register", command=register)
    register_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    login_root.mainloop()

# Main Menu after successful login
def main_menu():
    root = tk.Tk()
    root.title("Tourism Management System")

    display_button = tk.Button(root, text="Display Tour Packages", command=display_tour_packages, padx=10, pady=5, bg='lightblue', fg='black', relief=tk.RAISED)
    display_button.pack(pady=10)
    display_button.bind("<Enter>", lambda event: display_button.config(bg="lightgreen"))  # Hover effect
    display_button.bind("<Leave>", lambda event: display_button.config(bg="lightblue"))  # Hover effect

    book_button = tk.Button(root, text="Book Tour", command=book_tour, padx=10, pady=5, bg='lightblue', fg='black', relief=tk.RAISED)
    book_button.pack(pady=10)
    book_button.bind("<Enter>", lambda event: book_button.config(bg="lightgreen"))  # Hover effect
    book_button.bind("<Leave>", lambda event: book_button.config(bg="lightblue"))  # Hover effect

    root.mainloop()

# Entry point for the application
login()  # Show login page initially