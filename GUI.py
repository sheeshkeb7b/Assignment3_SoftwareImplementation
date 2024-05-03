import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from main_classes import *
import random

class CompanySystemGUI:
    "This represents the user interface for the company's system to operate in"
    def __init__(self, master):

        self.master = master
        self.master.title("Company Management System")

        # Loads data from storage, handles any potential errors if data are missing.
        self.employees = load_data("employees.pkl")
        self.clients_events = load_data("clients_events.pkl")
        self.events = load_data("events.pkl")
        self.suppliers = load_data("suppliers.pkl")
        self.guests = load_data("guests.pkl")
        self.venues = load_data("venues.pkl")

        # Setup the initial user interface when launching the program.
        self.setup_welcome_frame()

    def setup_welcome_frame(self):
        # Set up the welcome frame that allows users to select their role to enter the program.

        self.welcome_frame = tk.Frame(self.master)
        self.welcome_frame.pack(padx=10, pady=10)
        tk.Label(self.welcome_frame, text="Best Events Management System",
                 font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self.welcome_frame, text="Please select the desired role:").pack(pady=10)

        self.role_var = tk.StringVar()
        self.role_dropdown = ttk.Combobox(self.welcome_frame, textvariable=self.role_var, state="readonly",
                                          values=("Employee/Manager", "Client"))
        self.role_dropdown.pack(pady=10)
        self.role_dropdown.bind("<<ComboboxSelected>>", self.role_selected)

        self.management_frame = tk.Frame(self.master)

    def role_selected(self, event):
        # Handle the role dselection event.
        role = self.role_var.get()
        self.welcome_frame.pack_forget()
        self.management_frame.pack(padx=10, pady=10)

        # Clear any widgets from the management frame before displaying new widgets
        for widget in self.management_frame.winfo_children():
            widget.destroy()

        tk.Label(self.management_frame, text="Best Events Management System",
                 font=("Arial", 16, "bold")).pack(pady=20)

        # If the user selects a specific role, it would take them to the place that they chose.
        if role == "Employee/Manager":
            self.display_employee_management_options()
        elif role == "Client":
            self.display_client_management_options()

    def display_employee_management_options(self):
        # Display the management options for Managing employees and Clients.
        tk.Button(self.management_frame, text="Manage Employees", command=self.manage_employees).pack(pady=10)
        tk.Button(self.management_frame, text="Manage Clients", command=self.manage_clients).pack(pady=10)
        tk.Button(self.management_frame, text="Return To Menu", command=self.return_to_menu).pack(pady=5)

    def display_client_management_options(self):
        # Display the management options for Managing Events and Suppliers and Guests.
        tk.Button(self.management_frame, text="Manage Events", command=self.display_event_management).pack(pady=10)
        tk.Button(self.management_frame, text="Manage Suppliers", command=self.display_supplier_management).pack(pady=10)
        tk.Button(self.management_frame, text="Manage Guests", command=self.display_guest_management).pack(pady=10)
        tk.Button(self.management_frame, text="Manage Venues", command=self.manage_venues).pack(pady=10)
        tk.Button(self.management_frame, text="Return To Menu", command=self.return_to_menu).pack(pady=5)

    def return_to_menu(self):
        # Function that returns to the main menu
        self.management_frame.pack_forget()
        self.setup_welcome_frame()

    def manage_employees(self):
        self.display_employee_management()

    def manage_clients(self):
        self.display_client_management()

    def display_main_menu(self):
        # Hides all frames and toplevel windows before showing the main menu again.
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
            else:
                widget.pack_forget()

        # Calls the setup function for the welcome frame to return and rebuild the main menu
        self.setup_welcome_frame()
        self.welcome_frame.pack(padx=10, pady=10)

    # The employee management system if the user's role is Employee/Manager
    def display_employee_management(self):
        for widget in self.management_frame.winfo_children():
            widget.destroy()

        tk.Label(self.management_frame, text="Best Events Management System",
                 font=("Arial", 16, "bold")).pack(pady=20)

        self.employee_tree = ttk.Treeview(self.management_frame,
                                          columns=("ID", "Name", "Department", "Job Title", "Basic Salary", "Manager ID"),
                                          show="headings")

        self.employee_tree.heading("ID", text="Employee ID")
        self.employee_tree.heading("Name", text="Name")
        self.employee_tree.heading("Department", text="Department")
        self.employee_tree.heading("Job Title", text="Job Title")
        self.employee_tree.heading("Basic Salary", text="Basic Salary")
        self.employee_tree.heading("Manager ID", text="Manager ID")
        self.employee_tree.pack(padx=10, pady=10, expand=True, fill='both')

        # User-interactive buttons below the employee table
        tk.Button(self.management_frame, text="Add Employee", command=self.add_employee).pack(side=tk.LEFT, padx=10,
                                                                                              pady=10)
        tk.Button(self.management_frame, text="Delete Employee", command=self.delete_employee).pack(side=tk.LEFT,
                                                                                                    padx=10, pady=10)
        tk.Button(self.management_frame, text="Modify Employee", command=self.modify_employee).pack(side=tk.LEFT,
                                                                                                    padx=10, pady=10)
        tk.Button(self.management_frame, text="Display Employee Details", command=self.display_employee).pack(
            side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.management_frame, text="Back to Menu", command=self.display_main_menu).pack(side=tk.LEFT,
                                                                                                   padx=10, pady=10)

        self.update_employee_tree()

    def update_employee_tree(self):
        self.employee_tree.delete(*self.employee_tree.get_children())
        for emp_id, emp in self.employees.items():
            emp_data = {
                "ID": emp._employee_ID,
                "Name": emp._name,
                "Department": emp._department,
                "Job Title": emp._job_title.value,
                "Basic Salary": emp._basic_salary,
                "Manager ID": emp._manager_ID if emp._manager_ID else "None"
            }

            # Ensure order matches the treeview column order
            self.employee_tree.insert("", "end", values=[
                emp_data["ID"],  # ID
                emp_data["Name"],  # Name
                emp_data["Department"],  # Department
                emp_data["Job Title"],  # Job Title
                emp_data["Basic Salary"],  # Basic Salary
                emp_data["Manager ID"],  # Manager ID
            ])

    # Function that adds a new employee to the database (activated once the user presses add employee) The format below
    # will be applied to other sections as well due to time constraints
    def add_employee(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New Employee")

        # Generates the next unique employee ID
        next_id = max(self.employees.keys(), default=0) + 1

        # Name entry
        tk.Label(add_window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Department entry (limited options with dropdown choice)
        tk.Label(add_window, text="Department:").grid(row=1, column=0, padx=5, pady=5)
        department_var = tk.StringVar()
        department_dropdown = ttk.Combobox(add_window, textvariable=department_var, state="readonly",
                                           values=[dep.value for dep in EmployeeDepartment])
        department_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Job Title entry (limited options with dropdown choice)
        tk.Label(add_window, text="Job Title:").grid(row=2, column=0, padx=5, pady=5)
        job_title_var = tk.StringVar()
        job_title_dropdown = ttk.Combobox(add_window, textvariable=job_title_var, state="readonly",
                                          values=[jt.value for jt in EmployeeType])
        job_title_dropdown.grid(row=2, column=1, padx=5, pady=5)

        # Manager ID (If empty becomes none)
        tk.Label(add_window, text="Manager ID (optional):").grid(row=3, column=0, padx=5, pady=5)
        manager_id = tk.Entry(add_window)
        manager_id.grid(row=3, column=1, padx=5, pady=5)

        # Salary (automatically assigned)
        basic_salary = random.randint(5000, 75000)
        tk.Label(add_window, text="Basic Salary: " + str(basic_salary)).grid(row=4, column=1, padx=5, pady=5)

        # Add Employee Button
        tk.Button(add_window, text="Add Employee",
                  command=lambda: self.save_new_employee(add_window, next_id, name_entry.get(), department_var.get(),
                                                         job_title_var.get(), manager_id.get(), basic_salary)).grid(
            row=5, column=0, columnspan=2, padx=5, pady=10)

        # Go Back Button
        tk.Button(add_window, text="Go Back", command=add_window.destroy).grid(row=6, column=0, columnspan=2, padx=5,
                                                                               pady=10)

    def save_new_employee(self, add_window, employee_ID, name, department, job_title, manager_ID, basic_salary):
        # Check if the job_title is empty
        if not job_title:
            messagebox.showerror("Error", "Job Title cannot be empty!")
            return

        # Check if the manager ID is empty
        if manager_ID.strip() == "":
            manager_ID = None

        # Check if the job title selected exists in the EmployeeType enum
        job_title_enum = job_title.replace(' ', '_').upper()
        if job_title_enum not in EmployeeType.__members__:
            # Provide a default job title if the selected one doesn't match any of the enum members
            job_title_enum = "DEFAULT"

        employee_type_ENUM = EmployeeType[job_title_enum]

        if name and department:
            new_emp = Employee(employee_ID, name, department, employee_type_ENUM, basic_salary, manager_ID)
            self.employees[employee_ID] = new_emp
            save_data(self.employees, "employees.pkl")
            self.update_employee_tree()
            add_window.destroy()
            messagebox.showinfo("Success", "Employee added successfully")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def delete_employee(self):
        selected_item = self.employee_tree.selection()
        # Generates the next unique employee ID
        next_id = max(self.employees.keys(), default=0) - 1
        if selected_item:
            emp_id = int(self.employee_tree.item(selected_item, 'values')[0])
            if messagebox.askyesno("Confirm", "Do you want to delete this employee?"):
                del self.employees[emp_id]
                save_data(self.employees, "employees.pkl")
                self.update_employee_tree()
                messagebox.showinfo("Success", "Employee deleted successfully")
        else:
            messagebox.showerror("Error", "No employee selected")

    def modify_employee(self):
        selected_item = self.employee_tree.selection()
        if selected_item:
            emp_id = int(self.employee_tree.item(selected_item, 'values')[0])
            employee = self.employees.get(emp_id)
            if employee:
                modify_window = tk.Toplevel()  # Create a new top-level window
                modify_window.title("Modify Employee Details")

                # Name Entry with Validation (Example)
                name_label = tk.Label(modify_window, text="Name:")
                name_label.grid(row=0, column=0)
                name_entry = tk.Entry(modify_window)
                name_entry.insert(0, employee._name)
                name_entry.grid(row=0, column=1)

                # Department Dropdown
                department_label = tk.Label(modify_window, text="Department:")
                department_label.grid(row=2, column=0)
                department_var = tk.StringVar(value=employee._department)
                department_dropdown = ttk.Combobox(modify_window, textvariable=department_var, state="readonly",
                                                   values=["Sales", "Marketing", "Accounting",
                                                           "Designers", "Handymen"])
                department_dropdown.grid(row=2, column=1)

                # Job Title Dropdown
                job_title_label = tk.Label(modify_window, text="Job Title:")
                job_title_label.grid(row=3, column=0)
                job_title_var = tk.StringVar(value=employee._job_title)
                job_title_dropdown = ttk.Combobox(modify_window, textvariable=job_title_var, state="readonly",
                                                  values=["Sales Manager", "Salesperson", "Marketing Manager",
                                                          "Marketers", "Accountants", "Designers", "Handymen"])
                job_title_dropdown.grid(row=3, column=1)

                # Basic Salary Entry with Validation (Example)
                basic_salary_label = tk.Label(modify_window, text="Basic Salary:")
                basic_salary_label.grid(row=4, column=0)
                basic_salary_entry = tk.Entry(modify_window)
                basic_salary_entry.insert(0, str(employee._basic_salary))
                basic_salary_entry.grid(row=4, column=1)

                # Manager ID
                manager_ID_label = tk.Label(modify_window, text="Manager ID (Optional):")
                manager_ID_label.grid(row=5, column=0)
                manager_ID_entry = tk.Entry(modify_window)
                manager_ID_entry.insert(0, str(employee._manager_ID))
                manager_ID_entry.grid(row=5, column=1)


                # Apply Changes Button with Validation Call
                button = tk.Button(modify_window, text="Apply Changes",
                                   command=lambda: self.apply_employee_changes(modify_window, emp_id, name_entry.get(),
                                                                               department_var.get(),
                                                                               job_title_var.get(),
                                                                               basic_salary_entry.get(),
                                                                               manager_ID_entry.get()))
                button.grid(row=6, columnspan=2)

                # Display the modify_window
                modify_window.mainloop()
            else:
                messagebox.showerror("Error", "Employee not found")
        else:
            messagebox.showerror("Error", "No employee selected")

    def apply_employee_changes(self, modify_window, emp_id, name, department, job_title, basic_salary, manager_ID):
        employee = self.employees.get(emp_id)
        if employee:
            if name and department and job_title and basic_salary:
                # Update the employee's details
                employee._name = name
                employee._department = department
                employee._job_title = EmployeeType[job_title.replace(' ', '_').upper()]
                employee._basic_salary = int(basic_salary)
                employee._manager_ID = manager_ID
                # Save the updated data
                save_data(self.employees, "employees.pkl")
                # Update the treeview to reflect changes
                self.update_employee_tree()
                modify_window.destroy()
                messagebox.showinfo("Success", "Employee details updated successfully")
            else:
                messagebox.showerror("Error", "All fields are required")
        else:
            messagebox.showerror("Error", "Employee not found")

    def display_employee(self):
        emp_id = simpledialog.askinteger("Display Employee", "Enter Employee ID:")
        if emp_id is not None:
            employee = self.employees.get(emp_id)

            if employee:
                details = f"ID: {employee._employee_ID}\nName: {employee._name}\nDepartment: {employee._department}\nJob Title: {employee._job_title.value}\nBasic Salary: {employee._basic_salary}\nManager ID: {employee._manager_ID}"
                messagebox.showinfo("Employee Details", details)
            else:
                messagebox.showerror("Error", f"No employee found with ID: {emp_id}")
        else:
            messagebox.showerror("Error", "Invalid Employee ID")

    def display_client_management(self):
        for widget in self.management_frame.winfo_children():
            widget.destroy()

        tk.Label(self.management_frame, text="Best Events Management System",
                 font=("Arial", 16, "bold")).pack(pady=20)

        self.client_tree = ttk.Treeview(self.management_frame,
                                        columns=("Client ID", "Type", "Date", "Time", "Duration", "Venue"),
                                        show="headings")
        self.client_tree.heading("Client ID", text="Client ID")
        self.client_tree.heading("Type", text="Type")
        self.client_tree.heading("Date", text="Date")
        self.client_tree.heading("Time", text="Time")
        self.client_tree.heading("Duration", text="Duration")
        self.client_tree.heading("Venue", text="Venue")
        self.client_tree.pack(padx=10, pady=10, fill='both', expand=True)

        tk.Button(self.management_frame, text="Add Client", command=self.add_client).pack(side=tk.LEFT, padx=10,
                                                                                          pady=10)
        tk.Button(self.management_frame, text="Delete Client", command=self.delete_client).pack(side=tk.LEFT, padx=10,
                                                                                                pady=10)
        tk.Button(self.management_frame, text="Modify Client", command=self.modify_client).pack(side=tk.LEFT, padx=10,
                                                                                                pady=10)
        tk.Button(self.management_frame, text="Display Client Details", command=self.display_client_details).pack(
            side=tk.LEFT, padx=10, pady=10)

        tk.Button(self.management_frame, text="Back to Menu", command=self.display_main_menu).pack(side=tk.LEFT,
                                                                                                   padx=10, pady=10)

        self.update_client_tree()

    def update_client_tree(self):
        self.client_tree.delete(*self.client_tree.get_children())
        for client_id, details in self.clients_events.items():
            self.client_tree.insert("", "end", values=(
                client_id, details['type'], details['date'], details['time'], details['duration'], details['venue']))

    def add_client(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New Client")

        client_id = max(self.clients_events.keys(), default=0) + 1

        tk.Label(add_window, text="Assigned Client ID:").grid(row=0, column=0)
        tk.Label(add_window, text=str(client_id)).grid(row=0, column=1)

        tk.Label(add_window, text="Type:").grid(row=1, column=0)
        type_var = tk.StringVar()
        type_dropdown = ttk.Combobox(add_window, textvariable=type_var, state="readonly",
                                     values=["Wedding", "Birthday", "Themed Parties", "Graduation"])
        type_dropdown.grid(row=1, column=1)

        tk.Label(add_window, text="Date (yyyy-mm-dd):").grid(row=2, column=0)
        date_entry = tk.Entry(add_window)
        date_entry.grid(row=2, column=1)

        tk.Label(add_window, text="Time (hh:mm):").grid(row=3, column=0)
        time_entry = tk.Entry(add_window)
        time_entry.grid(row=3, column=1)

        tk.Label(add_window, text="Duration:").grid(row=4, column=0)
        duration_entry = tk.Entry(add_window)
        duration_entry.grid(row=4, column=1)

        tk.Label(add_window, text="Venue:").grid(row=5, column=0)
        venue_var = tk.StringVar()
        venue_dropdown = ttk.Combobox(add_window, textvariable=venue_var, state="readonly",
                                      values=["The Glasshouse", "Midtown", "Rose Gardens"])
        venue_dropdown.grid(row=5, column=1)

        tk.Button(add_window, text="Save Client",
                  command=lambda: self.save_new_client(add_window, client_id, type_var.get(), date_entry.get(),
                                                       time_entry.get(), duration_entry.get(), venue_var.get())).grid(
            row=6, columnspan=2)

    def save_new_client(self, add_window, client_id, type, date, time, duration, venue):
        if type and date and time and duration and venue:
            self.clients_events[client_id] = {'type': type, 'date': date, 'time': time, 'duration': duration,
                                              'venue': venue}
            save_data(self.clients_events, "clients_events.pkl")
            self.update_client_tree()
            add_window.destroy()
            messagebox.showinfo("Success", "Client added successfully")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def delete_client(self):
        selected_item = self.client_tree.selection()
        if selected_item:
            client_id = int(self.client_tree.item(selected_item, 'values')[0])
            if messagebox.askyesno("Confirm", "Do you want to delete this client?"):
                del self.clients_events[client_id]
                save_data(self.clients_events, "clients_events.pkl")
                self.update_client_tree()
                messagebox.showinfo("Success", "Client deleted successfully")
        else:
            messagebox.showerror("Error", "No client selected")

    def modify_client(self):
        selected_item = self.client_tree.selection()
        if selected_item:
            client_id = int(self.client_tree.item(selected_item, 'values')[0])
            client_details = self.clients_events.get(client_id)
            if client_details:
                modify_window = tk.Toplevel(self.master)
                modify_window.title("Modify Client Details")

                tk.Label(modify_window, text="Type:").grid(row=0, column=0)
                type_var = tk.StringVar(value=client_details['type'])
                type_dropdown = ttk.Combobox(modify_window, textvariable=type_var, state="readonly",
                                             values=["Wedding", "Birthday", "Themed Parties", "Graduation"])
                type_dropdown.grid(row=0, column=1)

                tk.Label(modify_window, text="Date (yyyy-mm-dd):").grid(row=1, column=0)
                date_entry = tk.Entry(modify_window)
                date_entry.insert(0, client_details['date'])
                date_entry.grid(row=1, column=1)

                tk.Label(modify_window, text="Time (hh:mm):").grid(row=2, column=0)
                time_entry = tk.Entry(modify_window)
                time_entry.insert(0, client_details['time'])
                time_entry.grid(row=2, column=1)

                tk.Label(modify_window, text="Duration:").grid(row=3, column=0)
                duration_entry = tk.Entry(modify_window)
                duration_entry.insert(0, client_details['duration'])
                duration_entry.grid(row=3, column=1)

                tk.Label(modify_window, text="Venue:").grid(row=4, column=0)
                venue_var = tk.StringVar(value=client_details['venue'])
                venue_dropdown = ttk.Combobox(modify_window, textvariable=venue_var, state="readonly",
                                              values=["The Glasshouse", "Midtown", "Rose Gardens"])
                venue_dropdown.grid(row=4, column=1)

                tk.Button(modify_window, text="Save Changes",
                          command=lambda: self.apply_client_changes(modify_window, client_id, type_var.get(),
                                                                    date_entry.get(), time_entry.get(),
                                                                    duration_entry.get(), venue_var.get())).grid(row=5,
                                                                                                                 columnspan=2)
            else:
                messagebox.showerror("Error", "Client not found")
        else:
            messagebox.showerror("Error", "No client selected")

    def apply_client_changes(self, modify_window, client_id, type, date, time, duration, venue):
        if type and date and time and duration and venue:
            self.clients_events[client_id] = {'type': type, 'date': date, 'time': time, 'duration': duration,
                                              'venue': venue}
            save_data(self.clients_events, "clients_events.pkl")
            self.update_client_tree()
            modify_window.destroy()
            messagebox.showinfo("Success", "Client details updated successfully")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def display_client_details(self):
        client_id = simpledialog.askinteger("Display Client", "Enter Client ID:")
        if client_id is not None:
            client_details = self.clients_events.get(client_id)
            if client_details:
                details = f"Type: {client_details['type']}\nDate: {client_details['date']}\nTime: {client_details['time']}\nDuration: {client_details['duration']} hours\nVenue: {client_details['venue']}"
                messagebox.showinfo("Client Details", f"Client ID: {client_id}\nDetails:\n{details}")
            else:
                messagebox.showerror("Error", f"No details found for client with ID: {client_id}")
        else:
            messagebox.showerror("Error", "Invalid Client ID")

    # Employee / Manager section fully completed.

    # Event Management (starting from client in the main menu)
    def display_event_management(self):
        for widget in self.management_frame.winfo_children():
            widget.destroy()

        tk.Label(self.management_frame, text="Best Events Management System",
                 font=("Arial", 16, "bold")).pack(pady=20)

        self.event_tree = ttk.Treeview(self.management_frame,
                                       columns=("Event ID", "Event Name", "Type", "Date", "Venue", "Theme", "Invoice"),
                                       show="headings")
        self.event_tree.heading("Event ID", text="Event ID")
        self.event_tree.heading("Event Name", text="Event Name")
        self.event_tree.heading("Type", text="Type")
        self.event_tree.heading("Date", text="Date")
        self.event_tree.heading("Venue", text="Venue")
        self.event_tree.heading("Theme", text="Theme")
        self.event_tree.heading("Invoice", text="Invoice")
        self.event_tree.pack(padx=10, pady=10, expand=True, fill='both')

        tk.Button(self.management_frame, text="Add Event", command=self.add_event).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.management_frame, text="Delete Event", command=self.delete_event).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.management_frame, text="Modify Event", command=self.modify_event).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.management_frame, text="Display Event Details", command=self.display_event_details).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Button(self.management_frame, text="Back to Menu", command=self.display_main_menu).pack(side=tk.LEFT,
                                                                                                   padx=10, pady=10)
        self.update_event_tree()

    def update_event_tree(self):
        self.event_tree.delete(*self.event_tree.get_children())
        for event_id, event in self.events.items():
            self.event_tree.insert("", "end",
                                   values=(event_id, event['name'], event['type'], event['date'], event['venue'],
                                           event['theme'], event['invoice']))

    def add_event(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New Event")

        event_id = max(self.events.keys(), default=0) + 1

        tk.Label(add_window, text="Event Name:").grid(row=0, column=0)
        event_name_entry = tk.Entry(add_window)
        event_name_entry.grid(row=0, column=1)

        tk.Label(add_window, text="Type:").grid(row=1, column=0)
        type_var = tk.StringVar()
        type_dropdown = ttk.Combobox(add_window, textvariable=type_var, state="readonly",
                                     values=["Wedding", "Birthday", "Themed Parties", "Graduation"])
        type_dropdown.grid(row=1, column=1)

        tk.Label(add_window, text="Date (YYYY-MM-DD):").grid(row=2, column=0)
        date_entry = tk.Entry(add_window)
        date_entry.grid(row=2, column=1)

        tk.Label(add_window, text="Venue:").grid(row=3, column=0)
        venue_var = tk.StringVar()
        venue_dropdown = ttk.Combobox(add_window, textvariable=venue_var, state="readonly",
                                      values=["The Glasshouse", "Midtown", "Rose Gardens"])
        venue_dropdown.grid(row=3, column=1)

        tk.Label(add_window, text="Theme:").grid(row=4, column=0)
        theme_entry = tk.Entry(add_window)
        theme_entry.grid(row=4, column=1)

        invoice_number = random.randint(5000, 25000)  # Assuming invoice should be random as before
        tk.Label(add_window, text="Invoice Number:").grid(row=5, column=0)
        tk.Label(add_window, text=str(invoice_number)).grid(row=5, column=1)

        tk.Button(add_window, text="Save Event", command=lambda: self.save_new_event(add_window, event_id, event_name_entry.get(), type_var.get(), date_entry.get(), venue_var.get(), theme_entry.get(), invoice_number)).grid(row=6, columnspan=2)

    def save_new_event(self, add_window, event_id, name, type_str, date, venue, theme, invoice):
        if name and type_str and date and venue and theme:
            new_event = {
                'name': name,
                'type': type_str,
                'date': date,
                'venue': venue,
                'theme': theme,
                'invoice': invoice
            }
            self.events[event_id] = new_event
            save_data(self.events, "events.pkl")
            self.update_event_tree()
            add_window.destroy()
            messagebox.showinfo("Success", "Event added successfully")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def delete_event(self):
        selected_item = self.event_tree.selection()
        if selected_item:
            event_id = int(self.event_tree.item(selected_item, 'values')[0])
            if messagebox.askyesno("Confirm", "Do you really want to delete this event?"):
                del self.events[event_id]
                save_data(self.events, "events.pkl")
                self.update_event_tree()
                messagebox.showinfo("Success", "Event deleted successfully")
        else:
            messagebox.showerror("Error", "No event selected")

    def modify_event(self):
        selected_item = self.event_tree.selection()
        if selected_item:
            event_id = int(self.event_tree.item(selected_item, 'values')[0])
            event = self.events.get(event_id)
            if event:
                modify_window = tk.Toplevel(self.master)
                modify_window.title("Modify Event Details")

                tk.Label(modify_window, text="Event Name:").grid(row=0, column=0)
                event_name_entry = tk.Entry(modify_window)
                event_name_entry.insert(0, event['name'])
                event_name_entry.grid(row=0, column=1)

                tk.Label(modify_window, text="Type:").grid(row=1, column=0)
                type_var = tk.StringVar(value=event['type'])
                type_dropdown = ttk.Combobox(modify_window, textvariable=type_var, state="readonly",
                values=["Wedding", "Birthday", "Themed Parties", "Graduation"])
                type_dropdown.grid(row=1, column=1)

                tk.Label(modify_window, text="Date (YYYY-MM-DD):").grid(row=2, column=0)
                date_entry = tk.Entry(modify_window)
                date_entry.insert(0, event['date'])
                date_entry.grid(row=2, column=1)

                tk.Label(modify_window, text="Venue:").grid(row=3, column=0)
                venue_var = tk.StringVar(value=event['venue'])
                venue_dropdown = ttk.Combobox(modify_window, textvariable=venue_var, state="readonly",
                                              values=["The Glasshouse", "Midtown", "Rose Gardens"])
                venue_dropdown.grid(row=3, column=1)

                tk.Label(modify_window, text="Theme:").grid(row=4, column=0)
                theme_entry = tk.Entry(modify_window)
                theme_entry.insert(0, event['theme'])
                theme_entry.grid(row=4, column=1)

                tk.Button(modify_window, text="Save Changes", command=lambda: self.apply_event_changes(modify_window, event_id, event_name_entry.get(), type_var.get(), date_entry.get(), venue_var.get(), theme_entry.get(), event['invoice'])).grid(row=5, columnspan=2)
            else:
                messagebox.showerror("Error", "Event not found")
        else:
            messagebox.showerror("Error", "No event selected")

    def apply_event_changes(self, modify_window, event_id, name, type, date, venue, theme, invoice):
        if name and type and date and venue and theme:
            updated_event = {'name': name, 'type': type, 'date': date, 'venue': venue, 'theme': theme, 'invoice': invoice}
            self.events[event_id] = updated_event
            save_data(self.events, "events.pkl")
            self.update_event_tree()
            modify_window.destroy()
            messagebox.showinfo("Success", "Event details updated successfully")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def display_event_details(self):
        selected_item = self.event_tree.selection()
        if selected_item:
            event_id = int(self.event_tree.item(selected_item, 'values')[0])
            event = self.events.get(event_id)
            if event:
                details = f"Event ID: {event_id}\nEvent Name: {event['name']}\nType: {event['type']}\nDate: {event['date']}\nVenue: {event['venue']}\nTheme: {event['theme']}\nInvoice: {event['invoice']}"
                messagebox.showinfo("Event Details", details)
            else:
                messagebox.showerror("Error", "No event found")
        else:
            messagebox.showerror("Error", "No event selected")



    def display_supplier_management(self):
        for widget in self.management_frame.winfo_children():
            widget.destroy()

        tk.Label(self.management_frame, text="Best Events Management System",
                 font=("Arial", 16, "bold")).pack(pady=20)

        self.supplier_tree = ttk.Treeview(self.management_frame,
                                          columns=("Supplier ID", "Name", "Contact Details", "Service"),
                                          show="headings")
        self.supplier_tree.heading("Supplier ID", text="Supplier ID")
        self.supplier_tree.heading("Name", text="Name")
        self.supplier_tree.heading("Service", text="Service")
        self.supplier_tree.heading("Contact Details", text="Contact Details")

        self.supplier_tree.pack(padx=10, pady=10, expand=True, fill='both')

        tk.Button(self.management_frame, text="Add Supplier", command=self.add_supplier).pack(side=tk.LEFT, padx=10,
                                                                                              pady=10)
        tk.Button(self.management_frame, text="Delete Supplier", command=self.delete_supplier).pack(side=tk.LEFT,
                                                                                                    padx=10, pady=10)
        tk.Button(self.management_frame, text="Modify Supplier", command=self.modify_supplier).pack(side=tk.LEFT,
                                                                                                    padx=10, pady=10)
        tk.Button(self.management_frame, text="Display Supplier Details", command=self.display_supplier_details).pack(
            side=tk.LEFT, padx=10, pady=10)

        tk.Button(self.management_frame, text="Back to Menu", command=self.display_main_menu).pack(side=tk.LEFT,
                                                                                                   padx=10, pady=10)

        self.update_supplier_tree()

    def update_supplier_tree(self):
        self.supplier_tree.delete(*self.supplier_tree.get_children())
        for supplier_id, supplier in self.suppliers.items():
            self.supplier_tree.insert("", "end", values=(
            supplier_id, supplier._name, supplier._service_type, supplier._contact_details))

    def add_supplier(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New Supplier")
        next_id = max(self.suppliers.keys(), default=0) + 1

        tk.Label(add_window, text="Supplier ID:").grid(row=0, column=0)
        tk.Label(add_window, text=str(next_id)).grid(row=0, column=1)

        tk.Label(add_window, text="Name:").grid(row=1, column=0)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=1, column=1)

        tk.Label(add_window, text="Type of Supplier:").grid(row=2, column=0)
        type_var = tk.StringVar()
        type_dropdown = ttk.Combobox(add_window, textvariable=type_var, state="readonly",
                                     values=["Catering", "Cleaning", "Decoration",
                                             "Entertainment", "Furniture"])
        type_dropdown.grid(row=2, column=1)

        tk.Label(add_window, text="Contact Details:").grid(row=3, column=0)
        contact_details_entry = tk.Entry(add_window)
        contact_details_entry.grid(row=3, column=1)

        tk.Button(add_window, text="Save Supplier",
                  command=lambda: self.save_new_supplier(add_window, next_id, name_entry.get(), type_var.get(),
                                                         contact_details_entry.get())).grid(row=4, columnspan=2)

    def save_new_supplier(self, add_window, supplier_id, name, service_type, contact_details):
        if name and service_type and contact_details:
            new_supplier = Supplier(supplier_id, name, service_type, contact_details)  # Now matches the constructor
            self.suppliers[supplier_id] = new_supplier
            save_data(self.suppliers, "suppliers.pkl")
            self.update_supplier_tree()
            add_window.destroy()
            messagebox.showinfo("Success", "Supplier added successfully")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def delete_supplier(self):
        selected_item = self.supplier_tree.selection()
        if selected_item:
            supplier_id = int(self.supplier_tree.item(selected_item, 'values')[0])
            if messagebox.askyesno("Confirm", "Do you really want to delete this supplier?"):
                del self.suppliers[supplier_id]
                save_data(self.suppliers, "suppliers.pkl")
                self.update_supplier_tree()
                messagebox.showinfo("Success", "Supplier deleted successfully")
        else:
            messagebox.showerror("Error", "No supplier selected")

    def modify_supplier(self):
        selected_item = self.supplier_tree.selection()
        if selected_item:
            supplier_id = int(self.supplier_tree.item(selected_item, 'values')[0])
            supplier = self.suppliers.get(supplier_id)
            if supplier:
                modify_window = tk.Toplevel(self.master)
                modify_window.title("Modify Supplier Details")

                tk.Label(modify_window, text="Name:").grid(row=0, column=0)
                name_entry = tk.Entry(modify_window)
                name_entry.insert(0, supplier._name)
                name_entry.grid(row=0, column=1)

                tk.Label(modify_window, text="Service:").grid(row=1, column=0)
                service_var = tk.StringVar(value=supplier._service_type)
                service_dropdown = ttk.Combobox(modify_window, textvariable=service_var, state="readonly",
                                                values=["Catering", "Cleaning", "Decoration",
                                                        "Entertainment", "Furniture"])
                service_dropdown.grid(row=1, column=1)

                tk.Label(modify_window, text="Contact Details:").grid(row=2, column=0)
                contact_details_entry = tk.Entry(modify_window)
                contact_details_entry.insert(0, supplier._contact_details)
                contact_details_entry.grid(row=2, column=1)

                tk.Button(modify_window, text="Save Changes",
                          command=lambda: self.apply_supplier_changes(modify_window, supplier_id, name_entry.get(),
                                                                      service_var.get(),
                                                                      contact_details_entry.get())).grid(row=3,
                                                                                                         columnspan=2)
            else:
                messagebox.showerror("Error", "Supplier not found")
        else:
            messagebox.showerror("Error", "No supplier selected")

    def apply_supplier_changes(self, modify_window, supplier_id, name, service, contact_details):
        if name and service and contact_details:
            supplier = self.suppliers.get(supplier_id)
            if supplier:
                supplier._name = name
                supplier._service_type = service
                supplier._contact_details = contact_details
                save_data(self.suppliers, "suppliers.pkl")
                self.update_supplier_tree()
                modify_window.destroy()
                messagebox.showinfo("Success", "Supplier details updated successfully")
            else:
                messagebox.showerror("Error", "Failed to update supplier details")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def display_supplier_details(self):
        selected_item = self.supplier_tree.selection()
        if selected_item:
            supplier_id = int(self.supplier_tree.item(selected_item, 'values')[0])
            supplier = self.suppliers.get(supplier_id)
            if supplier:
                details = f"Supplier ID: {supplier_id}\nName: {supplier._name}\nService: {supplier._contact_details}\n Contact: {supplier._service_type}"
                messagebox.showinfo("Supplier Details", details)
            else:
                messagebox.showerror("Error", "No supplier found")
        else:
            messagebox.showerror("Error", "No supplier selected")

    def display_guest_management(self):
        """Display the guest management interface."""
        # Clear any existing widgets in the management frame
        for widget in self.management_frame.winfo_children():
            widget.destroy()

        # Create a label for the guest management system
        tk.Label(self.management_frame, text="Best Events Management System",
                 font=("Arial", 16, "bold")).pack(pady=20)

        # Create the treeview for displaying guests with appropriate column headings
        self.guest_tree = ttk.Treeview(self.management_frame,
                                       columns=("Name", "Guest ID", "Contact Details"),
                                       show="headings")
        self.guest_tree.heading("Guest ID", text="Guest ID")
        self.guest_tree.heading("Name", text="Name")
        self.guest_tree.heading("Contact Details", text="Contact Details")
        self.guest_tree.pack(padx=10, pady=10, expand=True, fill='both')

        # Adding buttons for managing guests
        tk.Button(self.management_frame, text="Add Guest", command=self.add_guest).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.management_frame, text="Delete Guest", command=self.delete_guest).pack(side=tk.LEFT, padx=10,
                                                                                              pady=10)
        tk.Button(self.management_frame, text="Modify Guest", command=self.modify_guest).pack(side=tk.LEFT, padx=10,
                                                                                              pady=10)
        tk.Button(self.management_frame, text="Display Guest Details", command=self.display_guest_details).pack(
            side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.management_frame, text="Back to Menu", command=self.display_main_menu).pack(side=tk.LEFT,
                                                                                                   padx=10, pady=10)

        # Update the guest tree with current data
        self.update_guest_tree()

    def update_guest_tree(self):
        """Refresh the guest display tree."""
        self.guest_tree.delete(*self.guest_tree.get_children())
        # Populate the treeview with guest data
        for guest_id, guest in self.guests.items():
            self.guest_tree.insert("", "end", values=(guest._guest_ID, guest._name, guest._contact_details))

    def add_guest(self):
        """Add a new guest."""
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New Guest")
        guest_id = max(self.guests.keys(), default=0) + 1

        tk.Label(add_window, text="Guest ID:").grid(row=0, column=0)
        guest_id_entry = tk.Entry(add_window)
        guest_id_entry.insert(0, guest_id)
        guest_id_entry.grid(row=0, column=1)

        tk.Label(add_window, text="Name:").grid(row=1, column=0)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=1, column=1)

        tk.Label(add_window, text="Contact Details:").grid(row=2, column=0)
        contact_details_entry = tk.Entry(add_window)
        contact_details_entry.grid(row=2, column=1)

        tk.Button(add_window, text="Save Guest",
                  command=lambda: self.save_new_guest(add_window, int(guest_id_entry.get()), name_entry.get(),
                                                      contact_details_entry.get())).grid(row=3, columnspan=2)

    def save_new_guest(self, add_window, guest_id, name, contact_details):
        """Save the newly added guest information."""
        if name and contact_details:
            new_guest = Guest(guest_id, name, contact_details)
            self.guests[guest_id] = new_guest
            save_data(self.guests, "guests.pkl")
            self.update_guest_tree()
            add_window.destroy()
            messagebox.showinfo("Success", "Guest added successfully")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def delete_guest(self):
        """Delete a guest from the guest list."""
        selected_item = self.guest_tree.selection()
        if selected_item:
            # Retrieve the guest ID directly from the selected item
            guest_id = self.guest_tree.item(selected_item, 'values')[0]
            if messagebox.askyesno("Confirm", "Do you really want to delete this guest?"):
                # Delete the guest from the guest list
                del self.guests[guest_id]
                # Save the updated guest list
                save_data(self.guests, "guests.pkl")
                # Update the guest display tree
                self.update_guest_tree()
                # Display success message
                messagebox.showinfo("Success", "Guest deleted successfully")
        else:
            # Display error message if no guest is selected
            messagebox.showerror("Error", "No guest selected")

    def modify_guest(self):
        """Modify an existing guest's details."""
        # Get the selected guest
        selected_item = self.guest_tree.selection()
        if selected_item:
            # Retrieve the guest ID from the selected item
            guest_id = int(self.guest_tree.item(selected_item, 'values')[0])
            # Get the guest object from the guest ID
            guest = self.guests.get(guest_id)
            if guest:
                # Create a window for modifying guest details
                modify_window = tk.Toplevel(self.master)
                modify_window.title("Modify Guest Details")

                # Display current guest details in entry fields for modification
                tk.Label(modify_window, text="Guest ID:").grid(row=0, column=0)
                guest_id_entry = tk.Entry(modify_window)
                guest_id_entry.insert(0, guest_id)
                guest_id_entry.config(state='disabled')
                guest_id_entry.grid(row=0, column=1)

                tk.Label(modify_window, text="Name:").grid(row=1, column=0)
                name_entry = tk.Entry(modify_window)
                name_entry.insert(0, guest.name)
                name_entry.grid(row=1, column=1)

                tk.Label(modify_window, text="Contact Details:").grid(row=2, column=0)
                contact_details_entry = tk.Entry(modify_window)
                contact_details_entry.insert(0, guest.contact_details)
                contact_details_entry.grid(row=2, column=1)

                # Button to save changes to guest details
                tk.Button(modify_window, text="Save Changes",
                          command=lambda: self.apply_guest_changes(modify_window, guest_id, name_entry.get(),
                                                                   contact_details_entry.get())).grid(row=3,
                                                                                                      columnspan=2)
            else:
                # Display error message if guest not found
                messagebox.showerror("Error", "Guest not found")
        else:
            # Display error message if no guest is selected
            messagebox.showerror("Error", "No guest selected")

    def apply_guest_changes(self, modify_window, guest_id, name, contact_details):
        #Apply changes to an existing guest's details.
        if name and contact_details:
            guest = self.guests.get(guest_id)
            if guest:
                guest._name = name
                guest._contact_details = contact_details
                save_data(self.guests, "guests.pkl")
                self.update_guest_tree()
                modify_window.destroy()
                messagebox.showinfo("Success", "Guest details updated successfully")
            else:
                messagebox.showerror("Error", "Failed to update guest details")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def display_guest_details(self):
        #Display details of a specific guest
        guest_id = simpledialog.askinteger("Display Guest", "Enter Guest ID:")
        if guest_id is not None:
            guest = self.guests.get(guest_id)
            if guest:
                details = f"ID: {guest._name}\nName: {guest._guest_ID}\nContact Details: {guest._contact_details}"
                messagebox.showinfo("Guest Details", details)
            else:
                messagebox.showerror("Error", f"No guest found with ID: {guest_id}")
        else:
            messagebox.showerror("Error", "Invalid Guest ID")

    def manage_venues(self):
        """Display the venue management interface."""
        try:
            self.management_frame.pack_forget()
            self.venue_frame = tk.Frame(self.master)
            self.venue_frame.pack(padx=10, pady=10)

            # Create a label for the venue management system
            tk.Label(self.venue_frame, text="Best Events Management System",
                     font=("Arial", 16, "bold")).pack(pady=20)

            # Create the treeview for displaying venues with appropriate column headings
            self.venue_tree = ttk.Treeview(self.venue_frame, columns=(
            "Venue ID", "Name", "Address", "Contact Details", "Min Guests", "Max Guests"), show="headings")
            self.venue_tree.heading("Venue ID", text="Venue ID")
            self.venue_tree.heading("Name", text="Name")
            self.venue_tree.heading("Address", text="Address")
            self.venue_tree.heading("Contact Details", text="Contact Details")
            self.venue_tree.heading("Min Guests", text="Min Guests")
            self.venue_tree.heading("Max Guests", text="Max Guests")
            self.venue_tree.pack(padx=10, pady=10, fill='both', expand=True)
            self.update_venue_tree()

            # Adding buttons for managing venues
            tk.Button(self.venue_frame, text="Add Venue", command=self.add_venue).pack(side=tk.LEFT, padx=10, pady=10)
            tk.Button(self.venue_frame, text="Delete Venue", command=self.delete_venue).pack(side=tk.LEFT, padx=10,
                                                                                             pady=10)
            tk.Button(self.venue_frame, text="Modify Venue", command=self.modify_venue).pack(side=tk.LEFT, padx=10,
                                                                                             pady=10)
            tk.Button(self.venue_frame, text="Display Venue Details", command=self.display_venue_details).pack(
                side=tk.LEFT, padx=10, pady=10)
            tk.Button(self.venue_frame, text="Back to Menu", command=self.display_main_menu).pack(side=tk.LEFT, padx=10,
                                                                                                  pady=10)
        except Exception as e:
            messagebox.showerror("Error", "Failed to manage venues: " + str(e))
            self.display_main_menu()

    def update_venue_tree(self):
        try:
            self.venue_tree.delete(*self.venue_tree.get_children())
            for venue_id, venue in self.venues.items():
                self.venue_tree.insert("", "end", values=(venue._venue_id, venue._name, venue._address,
                                                          venue._contact_details, venue._min_guests, venue._max_guests))
        except Exception as e:
            messagebox.showerror("Error", "Failed to update venue data: " + str(e))

    def add_venue(self):
        try:
            add_window = tk.Toplevel(self.master)
            add_window.title("Add New Venue")
            # Provide a default value of 0 for max() when the sequence is empty
            next_venue_id = max((int(vid) for vid in self.venues.keys()), default=0) + 1

            tk.Label(add_window, text="Venue ID:").grid(row=0, column=0)
            venue_id_entry = tk.Entry(add_window)
            venue_id_entry.insert(0, str(next_venue_id))
            venue_id_entry.config(state='readonly')
            venue_id_entry.grid(row=0, column=1)

            tk.Label(add_window, text="Name: ").grid(row=1, column=0)
            name_entry = tk.Entry(add_window)
            name_entry.grid(row=1, column=1)

            tk.Label(add_window, text="Address:").grid(row=2, column=0)
            address_entry = tk.Entry(add_window)
            address_entry.grid(row=2, column=1)

            tk.Label(add_window, text="Contact Details:").grid(row=3, column=0)
            contact_details_entry = tk.Entry(add_window)
            contact_details_entry.grid(row=3, column=1)

            tk.Label(add_window, text="Min Guests:").grid(row=4, column=0)
            min_guests_entry = tk.Entry(add_window)
            min_guests_entry.grid(row=4, column=1)

            tk.Label(add_window, text="Max Guests:").grid(row=5, column=0)
            max_guests_entry = tk.Entry(add_window)
            max_guests_entry.grid(row=5, column=1)

            tk.Button(add_window, text="Save Venue",
                      command=lambda: self.save_new_venue(next_venue_id, name_entry.get(), address_entry.get(),
                                                          contact_details_entry.get(), min_guests_entry.get(),
                                                          max_guests_entry.get(), add_window)).grid(row=6, columnspan=2)
        except Exception as e:
            messagebox.showerror("Error", "Failed to add new venue: " + str(e))
            if 'add_window' in locals():
                add_window.destroy()

    def save_new_venue(self, venue_id, name, address, contact_details, min_guests, max_guests, window):
        try:
            if name and address and contact_details and min_guests and max_guests:
                new_venue = Venue(venue_id, name, address, contact_details, min_guests, max_guests)
                self.venues[venue_id] = new_venue
                save_data(self.venues, "venues.pkl")
                self.update_venue_tree()
                window.destroy()
                messagebox.showinfo("Success", "Venue added successfully")
            else:
                messagebox.showerror("Error", "All fields are required!")
        except Exception as e:
            messagebox.showerror("Error", "Failed to save new venue: " + str(e))
            if 'window' in locals():
                window.destroy()

    def delete_venue(self):
        try:
            selected_item = self.venue_tree.selection()
            if selected_item:
                venue_id = int(self.venue_tree.item(selected_item, 'values')[0])
                if venue_id in self.venues:
                    if messagebox.askyesno("Confirm", "Do you want to delete this venue?"):
                        del self.venues[venue_id]
                        save_data(self.venues, "venues.pkl")
                        self.update_venue_tree()
                        messagebox.showinfo("Success", "Venue deleted successfully")
                else:
                    messagebox.showerror("Error", "Venue not found")
            else:
                messagebox.showerror("Error", "No venue selected")
        except Exception as e:
            messagebox.showerror("Error", "Failed to delete venue: " + str(e))

    def modify_venue(self):
        try:
            selected_item = self.venue_tree.selection()
            if selected_item:
                venue_id_str = self.venue_tree.item(selected_item, 'values')[0]
                venue_id = int(venue_id_str)
                venue = self.venues.get(venue_id)
                if venue:
                    modify_window = tk.Toplevel(self.master)
                    modify_window.title("Modify Venue")

                    tk.Label(modify_window, text="Name:").grid(row=1, column=0)
                    name_entry = tk.Entry(modify_window)
                    name_entry.insert(0, venue._name)
                    name_entry.grid(row=1, column=1)

                    tk.Label(modify_window, text="Address:").grid(row=2, column=0)
                    address_entry = tk.Entry(modify_window)
                    address_entry.insert(0, venue._address)
                    address_entry.grid(row=2, column=1)

                    tk.Label(modify_window, text="Contact Details:").grid(row=3, column=0)
                    contact_details_entry = tk.Entry(modify_window)
                    contact_details_entry.insert(0, venue._contact_details)
                    contact_details_entry.grid(row=3, column=1)

                    tk.Label(modify_window, text="Min Guests:").grid(row=4, column=0)
                    min_guests_entry = tk.Entry(modify_window)
                    min_guests_entry.insert(0, venue._min_guests)
                    min_guests_entry.grid(row=4, column=1)

                    tk.Label(modify_window, text="Max Guests:").grid(row=5, column=0)
                    max_guests_entry = tk.Entry(modify_window)
                    max_guests_entry.insert(0, venue._max_guests)
                    max_guests_entry.grid(row=5, column=1)

                    tk.Button(modify_window, text="Save Changes", command=lambda: self.save_new_venue(
                        venue_id, name_entry.get(), address_entry.get(), contact_details_entry.get(),
                        min_guests_entry.get(), max_guests_entry.get(), modify_window)).grid(row=6, columnspan=2)
                else:
                    messagebox.showerror("Error", "Venue not found")
            else:
                messagebox.showerror("Error", "No venue selected")
        except Exception as e:
            messagebox.showerror("Error", "Failed to modify venue details: " + str(e))
            if 'modify_window' in locals():
                modify_window.destroy()

    def display_venue_details(self):
        try:
            venue_id = simpledialog.askinteger("Display Venue", "Enter Venue ID:")
            if venue_id is not None:
                venue = self.venues.get(venue_id)
                if venue:
                    details = f"Venue ID: {venue._venue_id}\nName: {venue._name}\nAddress: {venue._address}\nContact Details: {venue._contact_details}\nMin Guests: {venue._min_guests}\nMax Guests: {venue._max_guests}"
                    messagebox.showinfo("Venue Details", details)
                else:
                    messagebox.showerror("Error", f"No venue found with ID: {venue_id}")
            else:
                messagebox.showerror("Error", "Invalid Venue ID")
        except Exception as e:
            messagebox.showerror("Error", "Failed to display venue details: " + str(e))
