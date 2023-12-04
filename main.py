import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tksheet import Sheet
from database.database_main import Database
import threading
import reminders


# Variables to store the logged-in user's details
logged_in_user_username = ""
logged_in_user_email = ""
logged_in_user_first_name = ""
logged_in_user_last_name = ""

# Thread declarations ands stop events for the threads, which are initialized inside login_window() function
appointments_thread = None
medications_thread = None
appointments_stop_event = threading.Event()
medications_stop_event = threading.Event()

# Initializing the database from database_main.py
my_db = Database()

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
        # Log in to the account using a username and a password
        username = username_var.get()
        password = password_var.get()

        # Check if the username and password match
        get_login_details = my_db.authenticate(username, password)
        if username in get_login_details and password in get_login_details:
            global logged_in_user_username, logged_in_user_email, logged_in_user_first_name, logged_in_user_last_name
            global appointments_stop_event, medications_stop_event, appointments_thread, medications_thread

            # Store the logged-in user's information in the above-mentioned variables
            logged_in_user_username = username
            user_info = my_db.get_patient_details(username, password)
            logged_in_user_email = user_info[0]
            logged_in_user_first_name = user_info[1]
            logged_in_user_last_name = user_info[2]

            # Initialize a thread for checking appointments
            appointments_thread = threading.Thread(target=reminders.check_appointments,
                                                   args=(appointments_stop_event, logged_in_user_email, logged_in_user_first_name, logged_in_user_last_name,))
            # Initialize a thread for checking medications
            medications_thread = threading.Thread(target=reminders.check_medications,
                                                  args=(medications_stop_event, logged_in_user_email, logged_in_user_first_name, logged_in_user_last_name,))
            # Start the trheads
            appointments_thread.start()
            medications_thread.start()

            # Once logged in, close the login window and open the main window
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

        # Add user's credentials to the database
        my_db.register_user(username, password)
        my_db.update_patient_data(username, first_name, last_name, email)

        # Close sign-up window
        signup_window.destroy()

        # Upon a successful registration, display a message
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

    # User Information Page
    user_info_frame = tk.Frame(notebook)
    notebook.add(user_info_frame, text='User Info')
    create_user_info_page(user_info_frame)

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


# Function to handle the user info page
def create_user_info_page(frame):
    # Check if there's information about the user in the database, and call methods accordingly
    if my_db.get_patient_health_history(logged_in_user_first_name, logged_in_user_last_name) == "No patient with the given first and last names":
        user_info_page_for_users_with_no_info(frame)
    else:
        user_info_page_for_users_with_info(frame)


# Function to handle the user info page for users with no information in the database
def user_info_page_for_users_with_no_info(frame):
    # Variables to store user input
    weight_var = tk.StringVar()
    height_var = tk.StringVar()
    age_var = tk.StringVar()
    dob_var = tk.StringVar()

    # Function to handle storing the user info in the database
    def update_user_info():
        weight = weight_var.get()
        height = height_var.get()
        age = age_var.get()
        dob = dob_var.get()

        # Store user's health information in the database
        my_db.insert_into_health_history(logged_in_user_first_name, logged_in_user_last_name, weight, height, age, dob)
        # Now that we have user's info, update the page
        user_info_page_for_users_with_info(frame)

    tk.Label(frame, text="Our records show that you have not\nadded your health information to the tracker.", font=("Arial 18 bold")).pack(pady=30)

    tk.Label(frame, text="Weight (kg):").pack()
    tk.Entry(frame, textvariable=weight_var).pack()

    tk.Label(frame, text="Height (cm):").pack()
    tk.Entry(frame, textvariable=height_var).pack()

    tk.Label(frame, text="Age:").pack()
    tk.Entry(frame, textvariable=age_var).pack()

    tk.Label(frame, text="Date of Birth (mm/dd/yyyy):").pack()
    tk.Entry(frame, textvariable=dob_var).pack()

    tk.Button(frame, text="Update Health Information", command=update_user_info).pack(pady=30)


# Function to handle the user info page for users with existing info in the database
def user_info_page_for_users_with_info(frame):
    # Destroy all widgets in the frame - if any - to update the page
    for widget in frame.winfo_children():
        widget.destroy()

    # Get user info from the database and parse it
    user_info = my_db.get_patient_health_history(logged_in_user_first_name, logged_in_user_last_name)
    weight = user_info[2]
    height = user_info[3]
    age = user_info[4]
    dob = user_info[5]

    # Print out user info in the 'User Info' frame
    tk.Label(frame, text="\nYour Information:", font=("Arial 16 bold")).pack(pady=20)
    tk.Label(frame, text="\nFirst name: " + logged_in_user_first_name).pack()
    tk.Label(frame, text="Last name: " + logged_in_user_last_name).pack()
    tk.Label(frame, text="E-mail: " + logged_in_user_email).pack()
    tk.Label(frame, text="Username: " + logged_in_user_username).pack()
    tk.Label(frame, text="\nWeight (kg): " + weight).pack()
    tk.Label(frame, text="Height (cm): " + height).pack()
    tk.Label(frame, text="Age: " + age).pack()
    tk.Label(frame, text="Date of Birth (mm/dd/yyyy): " + dob).pack()


# Function to handle the creation of the medications page
def create_medications_page(frame):
    # Add widgets for medications page
    label = tk.Label(frame, text="Track your medications:", font=("Arial 18 bold"))
    label.pack(pady=10)

    # If there are any medications in the database, get them; if not, create an empty list
    if type(my_db.get_patient_medications(logged_in_user_first_name, logged_in_user_last_name)) == str:
        data = []
    else:
        data = my_db.get_patient_medications(logged_in_user_first_name, logged_in_user_last_name)

    # adding the medications sheet to the frame
    medications_sheet = Sheet(frame)
    medications_sheet.set_sheet_data(data)
    medications_sheet.headers(["Medication Name", "Scheduled Time"])
    medications_sheet.enable_bindings(("single_select"))
    medications_sheet.place(x=25, y=50, width=700, height=300)
    medications_sheet.set_options(auto_resize_columns=True)

    # Function to handle deletion of medications
    def delete_selected_medication_row():
        selected_cell = medications_sheet.get_currently_selected()
        selected_row = selected_cell.row
        my_db.delete_medications_data(logged_in_user_first_name, logged_in_user_last_name, data[selected_row][1], data[selected_row][0])
        del data[selected_row]

        # Update the medications sheet after deletion
        medications_sheet.select_cell(0, 0)
        medications_sheet.delete_row(idx=selected_row)
        medications_sheet.refresh()

    # Function to handle the creation of the add-new-medication window
    def add_new_medication_window():
        add_medication_window = tk.Toplevel(root)
        add_medication_window.title("Add New Medication")
        add_medication_window.geometry("380x100")

        medication_name_var = tk.StringVar()
        medication_time_var = tk.StringVar()

        # Function to add new medication to the database
        def add_medication():
            medication_name = medication_name_var.get()
            medication_time = medication_time_var.get()

            my_db.insert_into_medications(logged_in_user_first_name, logged_in_user_last_name, medication_time,
                                          medication_name)

            data.append((medication_name, medication_time))

            # Update the medications sheet
            medications_sheet.set_sheet_data(data)
            medications_sheet.refresh()
            add_medication_window.destroy()

            # Display a message
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

    add_medication_button = tk.Button(frame, text="Add new medication", command=add_new_medication_window)
    add_medication_button.pack(side=BOTTOM)


# Function to handle the creation of an appointments page
def create_appointments_page(frame):
    # Add widgets for appointments page
    label = tk.Label(frame, text="Track your doctor appointments:", font=("Arial 18 bold"))
    label.pack(pady=10)

    # If there are any appointments in the database, get them; if not, create an empty list
    if type(my_db.get_patient_appointments(logged_in_user_first_name, logged_in_user_last_name)) == str:
        data = []
    else:
        data = my_db.get_patient_appointments(logged_in_user_first_name, logged_in_user_last_name)

    # adding the appointments sheet to the frame
    appointments_sheet = Sheet(frame)
    appointments_sheet.set_sheet_data(data)
    appointments_sheet.headers(["Doctor's First Name", "Doctor's Last Name", "Appointment Date", "Appointment Time"])
    appointments_sheet.enable_bindings(("single_select"))
    appointments_sheet.place(x=25, y=50, width=700, height=300)
    appointments_sheet.set_options(auto_resize_columns=True)

    def delete_selected_appointment_row():
        selected_cell = appointments_sheet.get_currently_selected()
        selected_row = selected_cell.row
        my_db.delete_appointment_data(logged_in_user_first_name, logged_in_user_last_name, data[selected_row][2],
                                      data[selected_row][3])
        del data[selected_row]

        # Update the appointments sheet
        appointments_sheet.select_cell(0, 0)
        appointments_sheet.delete_row(idx=selected_row)
        appointments_sheet.refresh()

    # Function to handle the creation of the add-new-appointment window
    def add_new_appointment_window():
        add_appointment_window = tk.Toplevel(root)
        add_appointment_window.title("Add New Appointment")
        add_appointment_window.geometry("380x150")

        doctor_first_name_var = tk.StringVar()
        doctor_last_name_var = tk.StringVar()
        appointment_date_var = tk.StringVar()
        appointment_time_var = tk.StringVar()

        # Function to add a new appointment to the database
        def add_appointment():
            doctor_first_name = doctor_first_name_var.get()
            doctor_last_name = doctor_last_name_var.get()
            appointment_date = appointment_date_var.get()
            appointment_time = appointment_time_var.get()

            my_db.create_appointment(logged_in_user_first_name, logged_in_user_last_name, appointment_date,
                                          appointment_time, doctor_first_name, doctor_last_name)

            data.append((doctor_first_name, doctor_last_name, appointment_date, appointment_time))

            # Update the appointments sheet
            appointments_sheet.set_sheet_data(data)
            appointments_sheet.refresh()
            add_appointment_window.destroy()

            # Display a message
            messagebox.showinfo("Add New Appointment", "New appointment added successfully")

        # Labels and Entries
        tk.Label(add_appointment_window, text="Doctor's First Name:").grid(row=0, column=0, sticky=tk.E)
        tk.Entry(add_appointment_window, textvariable=doctor_first_name_var).grid(row=0, column=1)

        tk.Label(add_appointment_window, text="Doctor's Last Name:").grid(row=1, column=0, sticky=tk.E)
        tk.Entry(add_appointment_window, textvariable=doctor_last_name_var).grid(row=1, column=1)

        tk.Label(add_appointment_window, text="Appointment Date (mm/dd/yyyy):").grid(row=2, column=0, sticky=tk.E)
        tk.Entry(add_appointment_window, textvariable=appointment_date_var).grid(row=2, column=1)

        tk.Label(add_appointment_window, text="Appointment Time (hh:mm):").grid(row=3, column=0, sticky=tk.E)
        tk.Entry(add_appointment_window, textvariable=appointment_time_var).grid(row=3, column=1)

        tk.Button(add_appointment_window, text="Add", command=add_appointment).grid(row=4, column=0, columnspan=2)

    # Create a button to delete the selected row
    delete_button = tk.Button(frame, text="Delete Selected Row", fg="red", command=delete_selected_appointment_row)
    delete_button.pack(side=BOTTOM)

    add_medication_button = tk.Button(frame, text="Add new appointment", command=add_new_appointment_window)
    add_medication_button.pack(side=BOTTOM)


# Open the login window to start the program
login_window()

root.mainloop()

# To stop the threads, set stop events
appointments_stop_event.set()
medications_stop_event.set()

# Terminate the threads
if appointments_thread and medications_thread:
    appointments_thread.join()
    medications_thread.join()