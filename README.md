# **Health Tracker with Reminders for Seniors**
Authors: Lasha Kaliashvili, Mikheil Uglava.

## **Goal of the Project**
The main goal of the project was to create a purpose-built program designed to enhance the overall health management experience for the elderly population by providing tools to make it easier to manage and keep track of health-related scheduled activities, such as medications and doctor appointments.

#### Objectives of the Project:
* Develop an intuitive user interface: create a user-friendly interface that caters to the needs of seniors. We built the program with an emphasis on simplicity and ease of navigation.
* Enable users to sign up and log in to their accounts: a user can easily sign up with their information (email, username, password, etc.) and then log in with their personal credentials to their account to access their personal experience of the program.
* Provide tools to store basic information about users: When you first open an account of the health tracker, you will be asked to enter your information, such as name, age, date of birth, etc. so that the elderly can take this information with them anywhere they go with easy access.
* Provide tools to track medications: users can track their upcoming medications (medication name, when to take it, etc.), and they can add new ones, as well as delete existing ones from the database.
* Provide tools to track doctor appointments: the same goes for doctor appointments - users can track their upcoming appointments (doctor name, last name, appointment date, and time), add new ones, and delete existing ones.
* Integrate reminder functionality: integrate a reminder system that sends timely notifications to the user's email address for scheduled medications and upcoming doctor appointments.

## **Significance of the Project**
The Health Tracker with Reminders for Seniors can hold immense significance in enhancing the lives of the elderly by addressing specific challenges they face in managing their health.
* Many seniors deal with complex medication regimens and multiple doctor appointments. Our Health Tracker simplifies these processes, reducing the cognitive burden on seniors and promoting a more organized and efficient approach to health management.
* Forgetfulness is a normal part of aging. As people grow older, changes occur in all parts of the body, including the brain [1]. As a result, many people don't remember information as well as they once did and aren't able to recall it as quickly. By providing timely reminders for medications and appointments via email, the program helps seniors stay on track with their healthcare routines, reducing the likelihood of missed medications and appointments.
* Often, family members and caregivers play a crucial role in the well-being of seniors. This program can also be extremely useful to them - providing the same benefits to receive reminders and updates to them as well.
* And finally, the Health Tracker actively promotes the independence of seniors by providing a platform that allows them to take charge of their well-being while fostering a sense of control over their health-related activities.

## **Installation and Instructions to Use**

## **Structure of the Code**

## **Functionalities and Results**
When you first run the program, you are greeted with a login page, which includes a welcome message, fields that accept login credentials, and buttons to log in or sign up/register a new account. 

<img width="803" alt="Screenshot 2023-12-02 at 5 19 32 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/f0c07f45-1a07-4588-91ba-752ed0459241">

### **Signing up**
New users are going to have to create an account to use the program. Otherwise, they will not be able to access the functionalities of the Health Tracker. On the welcome/login page, a user can press the `Sign Up` button, which opens up a new window, prompting new users to enter their information. In the example below, we are creating an account for a fictional 78-year-old senior, John Denver, with the username johndenver, and the same password.

<img width="803" alt="Screenshot 2023-12-02 at 5 20 14 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/f4268498-9639-4dc1-966d-a4624abb6017">

After successful registration, a message is displayed, and the sign-up window disappears.

<img width="264" alt="Screenshot 2023-12-02 at 5 20 35 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/97c6e311-8ea0-4644-81c1-0f38867004dc">

### **Logging in to your account**
After the registration, users can use the username and password that they've set up during the registration process to log in to their account. If the username and password are correct, the main window is going to open up, otherwise, the following message is going to be displayed:

<img width="263" alt="Screenshot 2023-12-02 at 5 44 35 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/039b1fd4-266a-4942-b65e-986bc5c9c3ad">

Users can enter their login credentials in the given fields of the user interface.

<img width="802" alt="Screenshot 2023-12-02 at 5 21 07 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/acd0e708-4f43-40d7-aec2-9c7478d8c61f">

### **User Information**
The main window of the application consists of three frames - User Info, Medications, and Appointments. New users, since we don't have any information yet, will be asked to enter their basic information in the main window itself.

<img width="802" alt="Screenshot 2023-12-02 at 5 21 25 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/7efcf049-5928-40fd-a258-75ede0d07d0f">

Users can enter their information like this and press the `Update Health Information` button:

<img width="802" alt="Screenshot 2023-12-02 at 5 22 18 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/829faeed-3a08-4b8e-89fd-52598bd15d5e">

The program is going to take the user's input, update the database, and display the newly entered details in the main window. When the user logs in the next time, they aren't going to be asked to enter this information again - it will all be retrieved from the database and displayed in the `User Info` frame automatically.

<img width="802" alt="Screenshot 2023-12-02 at 5 22 32 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/991fbe91-3b3f-4af3-a921-a62391756d60">

### **Medications**
New users are greeted with an empty sheet of medications in the `Medications` frame. This is what the frame looks like initially.

<img width="802" alt="Screenshot 2023-12-02 at 5 22 42 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/41b90db1-a931-405d-a3c2-d92cf8d1e0c4">

#### Adding a New Medication
Users can add new medications to the database by pressing the `Add new medication` button. The button press opens up a new window with fields that take information about the medication such as the name and the time when the user needs to take it.

<img width="802" alt="Screenshot 2023-12-02 at 5 23 28 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/3e305b37-f4ca-46e2-8516-c2417e86d6eb">

After entering all necessary information about the new medication, users can press the `Add` button, which is going to add the medication to the database and update the sheet in the `Medications` frame.

<img width="262" alt="Screenshot 2023-12-02 at 5 26 16 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/47217a49-f4db-420d-bac0-12d0a49f88dd">

This is what the sheet looks like with a few medications added to the database:

<img width="803" alt="Screenshot 2023-12-02 at 5 29 46 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/62d66e13-eb5f-4e0d-b078-6d8f25c73d2f">

#### Deleting a Medication
Deleting a medication from the database is a very easy process. You just need to select the cell of the medication (this can be any cell of the row) like this:

<img width="803" alt="Screenshot 2023-12-02 at 5 29 55 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/f29a9f3f-a323-4511-8032-2723492998d3">

After the medication is selected, you can just press the `Delete Selected Row` button, which is going to remove the medication from the database by calling an appropriate method and then, update the sheet.

<img width="803" alt="Screenshot 2023-12-02 at 5 30 07 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/ac0beb66-97cb-4cc1-a8a1-c3b637721252">

### **Doctor Appointments**
The appointment window is dedicated to the user's doctor appointments, and it functions very similarly to the medications window. New users are greeted with an empty sheet of doctor appointments in the `Appointments` frame. This is what the frame looks like initially.

<img width="803" alt="Screenshot 2023-12-02 at 5 30 22 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/d824d891-1434-451f-a0ea-734001913b0f">

#### Adding a New Appointment
Users can add new appointments to the database by pressing the `Add new appointment` button. The button press opens up a new window with fields that take information about the appointment such as the doctor's first and last name, as well as the date and time of the appointment.

<img width="803" alt="Screenshot 2023-12-02 at 5 30 46 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/aa015420-acce-4f3b-a52b-f1ed4a6935ab">

After entering all necessary information about the new appointment, users can press the `Add` button, which is going to add the appointment to the database and update the sheet in the `Appointments` frame.

<img width="265" alt="Screenshot 2023-12-02 at 5 30 59 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/c3cc8d2c-6c7f-4f73-98ea-48e92d32e6eb">

<img width="801" alt="Screenshot 2023-12-02 at 5 31 10 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/1b2f44d9-4987-4102-b08e-3f9a8d2da68f">

#### Deleting an Appointment
Deleting an appointment from the database is a very easy process. You just need to select the cell of the appointment (this can be any cell of the row) like this:

<img width="801" alt="Screenshot 2023-12-02 at 5 31 17 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/a6569f6f-5c64-404b-8de8-8ef4bf34335f">

After the appointment is selected, you can just press the `Delete Selected Row` button, which is going to remove the appointment details from the database by calling an appropriate method and then, update the sheet.

<img width="801" alt="Screenshot 2023-12-02 at 5 31 27 PM" src="https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/9b513ad9-fe10-4cae-ab92-126fce59d6d1">

### **Reminders**
One of the main goals of the project was to create a reminder system to help seniors with the memory loss that might come with age, in many cases. The reminders system works in the background, and in practice, it's a very simple process.
* When the user first logs in to their account, the program takes the user's information, such as their username, email, etc., and initializes two threads, one dedicated to medications and another one to appointments. The newly initialized threads call `check_medications` and `check_appointments` functions from `reminders.py`, and the program passes the user's information to the function.
* Both of the functions, `check_medications` and `check_appointments` run continuously during the program run. Their main task is to check their respective databases, and if there are any upcoming medications or appointments (medications within 30 minutes; appointments within 60 minutes), send email reminders to the users.
* Beforehand, we've set up a dedicated email address `healthtrackerforseniors@gmail.com` with app access to use in our program to send email reminders to users.
* We use the SMTP library [2] to connect to the Gmail server, log in to our account, and send emails to the users.

This is what the email reminder currently looks like. In the case of a medication, it includes the medication name, as well as the scheduled time, and for an appointment, it includes the doctor's name, as well as the appointment date and time.

![IMG_1967](https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/d319d3f5-03d0-4ae8-88c4-e05fdd0ba821)

![IMG_1969](https://github.com/Mikheil-U/Health-Tracker-with-Reminders-for-Seniors/assets/111999712/8c71f77f-ef16-4ae8-bdc9-a3f84d374a7f)

## **Discussion and Conclusions**

## **References**
1. https://www.nia.nih.gov/health/memory-loss-and-forgetfulness/memory-problems-forgetfulness-and-aging
2. https://docs.python.org/3/library/smtplib.html
3. 
