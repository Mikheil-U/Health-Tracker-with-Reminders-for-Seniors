import sqlite3
from database.db_columns import DatabaseColumns


class Database:

    def __init__(self):
        self.__sql_connection = sqlite3.connect('hospital.db')
        self.__cursor = self.__sql_connection.cursor()

    def create_table(self, table_name: str, columns: list[str]):
        """
        To create a SqLite table
        :param table_name: A name of a table we are creating
        :param columns: Columns names for table we are creating
        :return: None
        """
        query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})
            '''
        try:
            self.__cursor.execute(query)
            self.__sql_connection.commit()
            return f"Success! {table_name} has been created"
        except sqlite3.Error as err:
            return f"Error creating table: {table_name}: {err}"

    def insert_into_patient_table(self, first_name: str, last_name: str, dob: str,
                                  email: str, phone_no: str, assigned_doctor: str):
        query = '''
                INSERT INTO Patient(first_name, last_name, dob, email, phone_no, assigned_doctor)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
        values = (first_name, last_name, dob, email, phone_no, assigned_doctor)
        try:
            self.__cursor.execute(query, values)
            self.__sql_connection.commit()
            return f"Data inserted into Patient table successfully!"
        except sqlite3.Error as err:
            return f"Error inserting data into Patient table: {err}"

    def insert_into_doctor_table(self, first_name: str, last_name: str,
                                 email: str, phone_no: str, ):
        query = '''
            INSERT INTO Doctor(first_name, last_name, email, phone_no)
            VALUES (?, ?, ?, ?)
        '''
        values = (first_name, last_name, email, phone_no)
        try:
            self.__cursor.execute(query, values)
            self.__sql_connection.commit()
            return f"Data inserted into Doctor table successfully!"
        except sqlite3.Error as err:
            return f"Error inserting data into Doctor table: {err}"

    def insert_into_appointment_table(self, description: str, doctor_id: str,
                                      patient_id: str):
        query = '''
            INSERT INTO Doctor(description, doctor_id, patient_id)
            VALUES (?, ?, ?, ?)
        '''
        values = (description, doctor_id, patient_id)
        try:
            self.__cursor.execute(query, values)
            self.__sql_connection.commit()
            return f"Data inserted into Appointment table successfully!"
        except sqlite3.Error as err:
            return f"Error inserting data into Appointment table: {err}"

    def read_table_data(self, table_name: str):
        """
            Prints the entire data for the given table
        :param table_name: The name of a table
        :return:
        """
        query = f'''
            SELECT * FROM {table_name}
        '''
        try:
            self.__cursor.execute(query)
            rows = self.__cursor.fetchall()
            for row in rows:
                print(row)
        except sqlite3.Error as err:
            print(f"Error fetching data from table {table_name}")

    def update_patient_data(self, current_username: str, first_name: str, last_name: str, dob: str, email: str):
        """This function is used to update patient's data after creating their account.
            During sign up we only ask for username and password
        """
        query = """
            UPDATE PATIENT
            SET first_name = ?, last_name = ?, dob = ?, email = ?
            WHERE user_name = ?
        """
        try:
            # execute the query
            self.__cursor.execute(query, (first_name, last_name, dob, email, current_username))
            # save the changes
            self.__sql_connection.commit()
            if self.__cursor.rowcount > 0:
                return f"{current_username} information has been updated"
            else:
                return f"No such username: {current_username}"
        except sqlite3.Error as err:
            return f"An error occurred while updating patient's data: {err}"

    def get_patient_email(self, first_name: str, last_name: str):
        query = f"""
            SELECT email FROM Patient
            WHERE first_name = ? AND last_name = ?
        """
        try:
            self.__cursor.execute(query, (first_name, last_name))
            email = self.__cursor.fetchone()
            if email:
                return email[0]
            else:
                return f"Patient with the given first name and last name couldn't be found"
        except sqlite3.Error as err:
            return f"An error occurred: {err}"

    def get_doctor_info(self, patient_first_name: str, patient_last_name: str):
        # Get the doctor's ID from the Patient table
        query = f"""
                SELECT doctor_id FROM Patient
                WHERE first_name = ? AND last_name = ?
            """
        try:
            self.__cursor.execute(query, (patient_first_name, patient_last_name))
            result = self.__cursor.fetchone()

            if result:
                doctor_id = result[0]
                # Get the doctor's data from the Doctror table
                query_doc = "SELECT * FROM Doctor WHERE doctor_id =?"
                self.__cursor.execute(query_doc, (doctor_id, ))
                doctor_data = self.__cursor.fetchone()

                if doctor_data:
                    return doctor_data
                else:
                    return f"Doctor not found"
            else:
                return "Patient not found"
        except sqlite3.Error as err:
            return f"An error occurred finding doctor's data: {err}"

    def get_patient_appointment(self, patient_f_name: str, patient_l_name: str):
        pass

    def get_patient_medications(self):
        pass

    def get_patient_health_history(self):
        pass

    def delete_patient_data(self, first_name: str, last_name: str):
        query = f"""
            DELETE FROM Patient WHERE first_name = ? AND last_name = ?
        """
        try:
            self.__cursor.execute(query, (first_name, last_name))
            # save the changes
            self.__sql_connection.commit()

            if self.__cursor.rowcount > 0:
                return f"Patient data deleted successfully"
            else:
                return f"No patient found with the given first and last name."
        except sqlite3.Error as err:
            return f"Error deleting patient data: {err}"

    def register_user(self, username: str, password: str):
        query = "INSERT INTO Patient(user_name, password) VALUES (?, ?)"
        values = (username, password)
        try:
            self.__cursor.execute(query, values)
            self.__sql_connection.commit()
            return f"You have successfully registered!"
        except sqlite3.Error as err:
            return f"Error creating an account: {err}"

    def authenticate(self, username: str, password: str) -> list[str]:
        """This function will check whether the user with the given username and password exist in a database"""
        query = "SELECT * FROM Patient WHERE user_name = ? AND password = ?"
        try:
            self.__cursor.execute(query, (username, password))
            # get one record
            result = self.__cursor.fetchone()
            # check if any record was found
            if result:
                return result[3:5]
        except sqlite3.Error as err:
            return ['Error occurred', err]


db_cols = DatabaseColumns()
my_db = Database()


# def create_tables():
#     """A helper function to initialize Database and create all tables"""
#     # print(my_db.create_table('Doctor', db_cols.get_doctor_columns()))
#     print(my_db.create_table('Patient', db_cols.get_patient_columns()))
#     # print(my_db.create_table('Appointment', db_cols.get_appointment_columns()))
#     # print(my_db.create_table('Medications', db_cols.get_medications_columns()))
#     # print(my_db.create_table('Health_History', db_cols.get_health_info_columns()))
#     # pass
#
# if __name__ == '__main__':
#     create_tables()
#     my_db.read_table_data('Patient')
#     # my_db.register_user('misho', '12345678')

