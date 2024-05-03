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

    # Function that adds a new employee to the database (activated once the user presses add employee)
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




if __name__ == "__main__":
    root = tk.Tk()
    app = CompanySystemGUI(root)
    root.mainloop()
