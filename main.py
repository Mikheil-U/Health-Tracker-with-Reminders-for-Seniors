import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tksheet import Sheet
from database.database_main import Database
from database.db_columns import *
import threading
import reminders


logged_in_user_username = ""
logged_in_user_email = ""
logged_in_user_first_name = ""
logged_in_user_last_name = ""

# Stop events
appointments_stop_event = threading.Event()
medications_stop_event = threading.Event()

# Create a thread for checking appointments
appointments_thread = threading.Thread(target=reminders.check_appointments, args=(appointments_stop_event,))
# Create a thread for checking medications
medications_thread = threading.Thread(target=reminders.check_medications, args=(medications_stop_event,))
appointments_thread.start()
medications_thread.start()


db_cols = DatabaseColumns()
my_db = Database()

# my_db.read_table_data('Patient')

"""A helper function to initialize Database and create all tables"""
# print(my_db.create_table('Doctor', db_cols.get_doctor_columns()))
# print(my_db.create_table('Patient', db_cols.get_patient_columns()))
# print(my_db.create_table('Appointment', db_cols.get_appointment_columns()))
# print(my_db.create_table('Medications', db_cols.get_medications_columns()))
# print(my_db.create_table('Health_History', db_cols.get_health_info_columns()))

# main application window - hidden
root = tk.Tk()
root.withdraw()

# If the user closes the program window, the program execution stops
def on_window_close():
    root.destroy()

# Function to handle login window
def login_window():
    login_window = tk.Toplevel(root)
    login_window.protocol("WM_DELETE_WINDOW", on_window_close)
    login_window.title("Log In")
    login_window.geometry("800x500")

    # Variables to store user input
    username_var = tk.StringVar()
    password_var = tk.StringVar()

    # Function to handle login button click
    def login():
        # TODO - update the login requirements
        username = username_var.get()
        password = password_var.get()

        # TODO - login
        # Check if the username and password match
        get_login_details = my_db.authenticate(username, password)
        if username in get_login_details and password in get_login_details:
            global logged_in_user_username, logged_in_user_email, logged_in_user_first_name, logged_in_user_last_name
            logged_in_user_username = username
            user_info = my_db.get_patient_details(username, password)
            logged_in_user_email = user_info[0]
            logged_in_user_first_name = user_info[1]
            logged_in_user_last_name = user_info[2]
            login_window.destroy()
            main_window()
            return

        # Display an error message if login fails
        messagebox.showerror("Error", "Invalid username or password")

    # Create widgets for login window
    tk.Label(login_window, text="WELCOME TO YOUR HEALTH TRACKER!", font=("Arial 26 bold")).pack(pady=40)
    tk.Label(login_window, text="Please log in to your account", font=("Arial 18 bold")).pack(pady=10)
    tk.Label(login_window, text="Username:").pack()
    tk.Entry(login_window, textvariable=username_var).pack()
    tk.Label(login_window, text="Password:").pack()
    tk.Entry(login_window, textvariable=password_var, show="*").pack()
    tk.Button(login_window, text="Log In", command=login).pack(pady=10)
    tk.Button(login_window, text="Sign Up", command=signup_window).pack()

    login_window.mainloop()


# Function to handle sign-up window
def signup_window():
    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")
    signup_window.geometry("380x200")

    # Variables to store user input
    username_var = tk.StringVar()
    password_var = tk.StringVar()
    email_var = tk.StringVar()
    first_name_var = tk.StringVar()
    last_name_var = tk.StringVar()

    # Function to handle sign-up button click
    def signup():
        username = username_var.get()
        password = password_var.get()
        email = email_var.get()
        first_name = first_name_var.get()
        last_name = last_name_var.get()

        my_db.register_user(username, password)
        my_db.update_patient_data(username, first_name, last_name, email)

        # Close sign-up window
        signup_window.destroy()

        messagebox.showinfo("Sign Up", "Singing up successful")

    # Labels and Entries
    tk.Label(signup_window, text="Username:").grid(row=0, column=0, sticky=tk.E)
    tk.Entry(signup_window, textvariable=username_var).grid(row=0, column=1)

    tk.Label(signup_window, text="Password:").grid(row=1, column=0, sticky=tk.E)
    tk.Entry(signup_window, textvariable=password_var, show="*").grid(row=1, column=1)

    tk.Label(signup_window, text="E-mail:").grid(row=2, column=0, sticky=tk.E)
    tk.Entry(signup_window, textvariable=email_var).grid(row=2, column=1)

    tk.Label(signup_window, text="First Name:").grid(row=3, column=0, sticky=tk.E)
    tk.Entry(signup_window, textvariable=first_name_var).grid(row=3, column=1)

    tk.Label(signup_window, text="Last Name:").grid(row=4, column=0, sticky=tk.E)
    tk.Entry(signup_window, textvariable=last_name_var).grid(row=4, column=1)

    tk.Button(signup_window, text="Sign Up", command=signup).grid(row=5, column=0, columnspan=2)


# Function to handle the main window
def main_window():
    main_window = tk.Toplevel(root)
    main_window.protocol("WM_DELETE_WINDOW", on_window_close)
    main_window.title("Health Tracker")
    main_window.geometry("800x500")

    # Create notebook with three frames
    notebook = ttk.Notebook(main_window)

    # Health Information Page
    health_frame = tk.Frame(notebook)
    notebook.add(health_frame, text='Health Info')
    create_health_page(health_frame)

    # Medications Page
    medications_frame = tk.Frame(notebook)
    notebook.add(medications_frame, text='Medications')
    create_medications_page(medications_frame)

    # Appointments Page
    appointments_frame = tk.Frame(notebook)
    notebook.add(appointments_frame, text='Appointments')
    create_appointments_page(appointments_frame)

    notebook.pack(expand=True, fill="both")

    main_window.mainloop()


def create_health_page(frame):
    # Add widgets for health information page
    label = tk.Label(frame, text="Enter health information:")
    label.pack(pady=10)

    # TODO - Add health information of the user and other stuff


def create_medications_page(frame):
    # Add widgets for medications page
    label = tk.Label(frame, text="Track your medications and set reminders:")
    label.pack(pady=10)

    # TODO - store sql table of medications in data list to open with tksheet
    # now data is only for demonstration purposes
    data = my_db.get_patient_medications(logged_in_user_first_name, logged_in_user_last_name)

    # adding the medications sheet to the frame
    medications_sheet = Sheet(frame)
    medications_sheet.set_sheet_data(data)
    medications_sheet.headers(["Medication Name", "Scheduled Time"])
    medications_sheet.enable_bindings(("single_select"))
    medications_sheet.place(x=25, y=50, width=700, height=300)
    medications_sheet.set_options(auto_resize_columns=True)

    def delete_selected_medication_row():
        selected_cell = medications_sheet.get_currently_selected()
        selected_row = selected_cell.row
        print(selected_row)
        my_db.delete_medications_data(logged_in_user_first_name, logged_in_user_last_name, data[selected_row][1], data[selected_row][0])
        del data[selected_row]
        medications_sheet.set_sheet_data(data)
        medications_sheet.refresh()

    def add_new_medication_window():
        add_medication_window = tk.Toplevel(root)
        add_medication_window.title("Add New Medication")
        add_medication_window.geometry("380x100")

        medication_name_var = tk.StringVar()
        medication_time_var = tk.StringVar()

        def add_medication():
            medication_name = medication_name_var.get()
            medication_time = medication_time_var.get()

            my_db.insert_into_medications(logged_in_user_first_name, logged_in_user_last_name, medication_time,
                                          medication_name)

            data.append((medication_name, medication_time))
            medications_sheet.set_sheet_data(data)
            medications_sheet.refresh()
            add_medication_window.destroy()

            messagebox.showinfo("Add New Medication", "New medication added successfully")

        # Labels and Entries
        tk.Label(add_medication_window, text="Medication Name:").grid(row=0, column=0, sticky=tk.E)
        tk.Entry(add_medication_window, textvariable=medication_name_var).grid(row=0, column=1)

        tk.Label(add_medication_window, text="When to take (hh:mm):").grid(row=1, column=0, sticky=tk.E)
        tk.Entry(add_medication_window, textvariable=medication_time_var).grid(row=1, column=1)

        tk.Button(add_medication_window, text="Add", command=add_medication).grid(row=2, column=0, columnspan=2)

    # Create a button to delete the selected row
    delete_button = tk.Button(frame, text="Delete Selected Row", fg="red", command=delete_selected_medication_row)
    delete_button.pack(side=BOTTOM)

    # TODO - add functionality to add_medication_button
    add_medication_button = tk.Button(frame, text="Add new medication", command=add_new_medication_window)
    add_medication_button.pack(side=BOTTOM)

def create_appointments_page(frame):
    # Add widgets for appointments page
    label = tk.Label(frame, text="Manage your doctor appointments:")
    label.pack()

    # TODO - copy-paste and adjust whatever we have in create_medications_page


# Open the login window to start the program
login_window()

root.mainloop()

# To stop the threads
appointments_stop_event.set()
medications_stop_event.set()

appointments_thread.join()
medications_thread.join()