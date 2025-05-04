# 📘 Student Management System (SMS)

The **Student Management System (SMS)** is a desktop-based application built with **Python** and **PyQt5**. It enables admins and regular users to manage student information and system users via an intuitive graphical interface.

---

## Table of Contents
- [Features](#features)  
- [Modules](#modules)  
- [User Roles](#user-roles)  
- [How It Works](#how-it-works)  
- [File Descriptions](#file-descriptions)  
- [Dependencies](#dependencies)

---

## Features
- Login system with secure password hashing (**SHA-256**)
- Admin and user roles with access control
- Add, update, delete, and search student records
- Admin-only user management panel (add/delete users)
- Clean and responsive GUI using **PyQt5**
- **SQLite** database integration

---

## Modules

| File Name         | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| `login_window.py` | Handles user login, connects to the authentication logic, redirects by role |
| `student_panel.py`| Displays student records with search, add, update, and delete functionalities |
| `admin_panel.py`  | Admin-only interface to view, add, and delete users                          |
| `sms_backend.py`  | Core logic: handles DB operations (CRUD + authentication)                    |
| `main_window.py`  | Main layout controller, loads interface tabs depending on user role          |
| `app.py`          | Application entry point, launches the PyQt5 login window                     |

---

## User Roles

### Admin
- ✅ Full access to both student and user management panels  
- ✅ Can create and delete system users  
- ✅ Can fully manage student records  

### User
- 🔒 Limited to viewing and searching student data  
- ❌ Cannot add, update, or delete students  
- ❌ Cannot access user management features  

---

## How It Works

### Login Phase
- `LoginWindow` authenticates users using `sms_backend.authenticate()`
- On successful login, launches `MainWindow` based on user role

### Dashboard Routing
- `MainWindow` displays:
  - **Student Panel** for all users
  - **Admin Panel** only for admin users

### Student Management
- Admins can **add**, **update**, and **delete** student records  
- All users can **search** and **view** records using flexible criteria  

### User Management (Admin Only)
- Admins can:
  - View current system users  
  - Add new users with **hashed passwords**  
  - Delete existing users  

---

## File Descriptions

| File Name         | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| `login_window.py` | Login window logic with redirection to main system                         |
| `student_panel.py`| Interface for managing students (CRUD & search)                            |
| `admin_panel.py`  | Interface for managing users (admins only)                                 |
| `sms_backend.py`  | Handles SQLite database operations and authentication                      |
| `main_window.py`  | Main GUI controller that loads tabs depending on the role                  |
| `app.py`          | Application entry point, starts the login window                           |

---

## Dependencies

- Python 3.x  
- PyQt5  
- SQLite3 (comes with Python)  
- `hashlib` (for password hashing)

**Note:**  
Ensure all `.py` files are in the same directory.  
The database `school.db` will be auto-generated if it does not exist.


