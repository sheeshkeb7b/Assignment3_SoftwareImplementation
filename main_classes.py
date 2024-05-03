import pickle
from enum import Enum


class EmployeeType(Enum):
    SALES_MANAGERS = "Sales Managers"
    SALESPERSON = "Salesperson"
    MARKETING_MANAGERS = "Marketing Managers"
    MARKETERS = "Marketers"
    ACCOUNTANTS = "Accountants"
    DESIGNERS = "Designers"
    HANDYMEN = "Handymen"


class EmployeeDepartment(Enum):
    SALES = "Sales"
    MARKETING = "Marketing"
    ACCOUNTING = "Accounting"
    DESIGNERS = "Designers"
    FACILITIES_MANAGEMENT = "Facilities Management"

class EventType(Enum):
    WEDDINGS = "Weddings"
    BIRTHDAYS = "Birthdays"
    THEMED_PARTIES = "Themed Parties"
    GRADUATIONS = "Graduations"


class SupplierType(Enum):
    CATERING = "Catering"
    CLEANING =  "Cleaning"
    FURNITURE = "Furniture"
    DECORATIONS = "Decorations"
    ENTERTAINMENT = "Entertainment"

class Person:
    def __init__(self, name, DOB, passport, age):
        self._name = name
        self._DOB = DOB
        self._passport = passport
        self._age = age

    def display(self):
        print(f"Name: {self._name}")
        print(f"Date of Birth: {self._DOB}")
        print(f"Passport: {self._passport}")
        print(f"Age: {self._age}")

class Employee(Person):
    def __init__(self, name, DOB, passport, age, employee_ID, basic_salary, department, job_title, manager_ID=None):
        super().__init__(name, DOB, passport, age)
        self._employee_ID = employee_ID
        self._basic_salary = basic_salary
        self._department = department
        self._job_title = job_title
        self._manager_ID = manager_ID
        self._employee_list = []

        # Assigns a manager ID if the employee job title is not manager (managers would not have the attribute as None)
        if self._job_title in (EmployeeType.SALES_MANAGERS, EmployeeType.MARKETING_MANAGERS):
            self._manager_ID = None

    def display(self):
        print("---" * 10, "Employee", "---" * 10)
        super().display()
        print(f"Employee ID: {self._employee_ID}")
        print(f"Basic Salary: {self._basic_salary}")
        print(f"Department: {self._department}")
        print(f"Job Title: {self._job_title}")
        print(f"Manager ID: {self._manager_ID}")

    # Getter and setter methods for manager ID
    def get_manager_ID(self):
        return self._manager_ID

    def set_manager_ID(self, manager_ID):
        self._manager_ID = manager_ID

    # Methods to be used in the system
    def add_employee(self):
        "This method adds an employee to the employee_list"
        pass # This is implemented in the GUI

    def delete_employee(self):
        "This method removes an existing employee from the employee_list"
        pass # This is implemented in the GUI

    def modify_employee(self):
        "This method updates an existing employee's attributes"
        pass # This is implemented in the GUI



class Client(Person):
    def __init__(self, name, DOB, passport, age, client_ID, client_address, contact_details, budget):
        super().__init__(name, DOB, passport, age)
        self._client_ID = client_ID
        self._address = client_address
        self._contact_details = contact_details
        self._budget = budget

    def display(self):
        print("---" * 10, "Client", "---" * 10)
        super().display()
        print(f"Client ID: {self._client_ID}")
        print(f"Address: {self._address}")
        print(f"Contact Details: {self._contact_details}")
        print(f"Budget: {self._budget}")


    # Methods to be used in the system
    def add_clients(self):
        "This method adds a client to the client list"
        pass  # This is implemented in the GUI

    def delete_client(self):
        "This method removes an existing client from the client_list"
        pass  # This is implemented in the GUI

    def modify_client(self):
        "This method updates an existing client's attributes"
        pass  # This is implemented in the GUI

class Guest(Person):
    def __init__(self, name, DOB, passport, age, guest_ID, address, contact_details, guest_event):
        super().__init__(name, DOB, passport, age)
        self._guest_ID = guest_ID
        self._address = address
        self._contact_details = contact_details
        self._guest_event = guest_event

    def display(self):
        print("---" * 10, "Guest", "---" * 10)
        super().display()
        print(f"Guest ID: {self._guest_ID}")
        print(f"Address: {self._address}")
        print(f"Contact Details: {self._contact_details}")
        print(f"Guest Event: {self._guest_event}")

    # Methods to be used in the system
    def add_guests(self):
        "This method adds a guest to a guest list (which will then be added to an event's guest list)"
        pass  # This is implemented in the GUI

    def delete_guest(self):
        "This method removes an existing guest from a guest list"
        pass  # This is implemented in the GUI

    def modify_guest(self):
        "This method updates an existing client's attributes"
        pass  # This is implemented in the GUI

class Venue:
    def __init__(self, venue_ID, name, address, contact, min_guests, max_guests):
        self._venue_ID = venue_ID
        self._name = name
        self._address = address
        self._contact = contact
        self._min_guests = min_guests
        self._max_guests = max_guests

    def display(self):
        print("---" * 10, "Venue", "---" * 10)
        print(f"Venue ID: {self._venue_ID}")
        print(f"Name: {self._name}")
        print(f"Address: {self._address}")
        print(f"Contact: {self._contact}")
        print(f"Minimum Guests: {self._min_guests}")
        print(f"Maximum Guests: {self._max_guests}")


    # Methods to be used in the system
    def add_venue(self):
        "This method adds a venue to the venue list"
        pass  # This is implemented in the GUI

    def delete_venue(self):
        "This method removes an existing venue from the venue list"
        pass  # This is implemented in the GUI

    def modify_venue(self):
        "This method updates an existing venue's attributes"
        pass  # This is implemented in the GUI

class Supplier:
    def __init__(self, supplier_ID, supplier_name, address, contact_details, supplier_type):
        self._supplier_ID = supplier_ID
        self._supplier_name = supplier_name
        self._address = address
        self._contact_details = contact_details
        self._supplier_type = supplier_type

    def display(self):
        print("---" * 10, "Supplier", "---" * 10)
        print(f"Supplier ID: {self._supplier_ID}")
        print(f"Supplier Name: {self._supplier_name}")
        print(f"Address: {self._address}")
        print(f"Contact Details: {self._contact_details}")
        print(f"Supplier Type: {self._supplier_type}")

    # Methods to be used in the system
    def add_supplier(self):
        "This method adds a supplier to the supplier list"
        pass  # This is implemented in the GUI

    def delete_supplier(self):
        "This method removes an existing supplier from the supplier list"
        pass  # This is implemented in the GUI

    def modify_supplier(self):
        "This method updates an existing supplier's attributes"
        pass  # This is implemented in the GUI

class Event:
    def __init__(self, event_title, event_ID, event_type, event_theme, event_date, event_time, event_duration,
                 event_venue, event_catering=None, event_cleaning=None, event_decorations=None,
                 event_entertainment=None, event_furniture=None, invoice=None, client=None):

        self._event_title = event_title
        self._event_ID = event_ID
        self._event_type = event_type
        self._event_theme = event_theme
        self._event_date = event_date
        self._event_time = event_time
        self._event_duration = event_duration
        self._event_venue = event_venue
        self._event_catering = event_catering
        self._event_cleaning = event_cleaning
        self._event_decorations = event_decorations
        self._event_entertainment = event_entertainment
        self._event_furniture = event_furniture
        self._invoice = invoice
        self._client = client
        self._guest_list = []
        self._suppliers = []

    def display(self):
        print("---" * 10, "Event", "---" * 10)
        print(f"Event Title: {self._event_title}")
        print(f"Event ID: {self._event_ID}")
        print(f"Event Type: {self._event_type}")
        print(f"Event Theme: {self._event_theme}")
        print(f"Event Date: {self._event_date}")
        print(f"Event Time: {self._event_time}")
        print(f"Event Duration: {self._event_duration}")
        print(f"Event Venue: {self._event_venue}")
        print(f"Event Catering: {self._event_catering}")
        print(f"Event Cleaning: {self._event_cleaning}")
        print(f"Event Decorations: {self._event_decorations}")
        print(f"Event Entertainment: {self._event_entertainment}")
        print(f"Event Furniture: {self._event_furniture}")
        print(f"Invoice: {self._invoice}")
        print(f"Client: {self._client}")
        print(f"Guest List: {self._guest_list}")
        print(f"Suppliers: {self._suppliers}")


    # Methods to be used in the system
    def add_event(self):
        "This method adds a event to the event list"
        pass  # This is implemented in the GUI

    def delete_event(self):
        "This method removes an existing event from the event list"
        pass  # This is implemented in the GUI

    def modify_event(self):
        "This method updates an existing event's attributes"
        pass  # This is implemented in the GUI

# Functions to save and load data using pickle
def load_data(file_path):
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("File not found. Initializing new data.")
        return {}

def save_data(data, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)