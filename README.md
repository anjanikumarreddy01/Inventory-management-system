Inventory Management System
A comprehensive desktop application built with Python and Tkinter for managing retail inventory, sales, and employee data.
This system features role-based access with separate, feature-rich dashboards for Admins and Employees.

📑 Table of Contents
About The Project

Screenshots

Features

Getting Started

Prerequisites

Installation & Setup

Database Configuration

Usage

Deployment

📌 About The Project
This project is a complete inventory management solution designed to streamline retail operations. It provides a robust backend powered by MySQL and an intuitive graphical interface built with Tkinter.

The application separates users into two roles:

Administrators: Manage products, suppliers, categories, employees, and view sales data.

Employees: Simplified interface focused on sales workflow, billing, and customer transactions.

This ensures data security and an efficient workflow for all users.

Built With:

Python 3

Tkinter

Pillow (PIL)

PyMySQL

qrcode

MySQL Server

🖼️ Screenshots
Login Screen	Admin Dashboard	Employee Billing Dashboard

login page:
[![Screenshot-2025-08-19-150538.png](https://i.postimg.cc/yxNXmQK8/Screenshot-2025-08-19-150538.png)](https://postimg.cc/xJWzYPqw)
admin dashboard:
[![Screenshot-2025-09-06-201627.png](https://i.postimg.cc/MGzwB4X2/Screenshot-2025-09-06-201627.png)](https://postimg.cc/219gR042)
employee bashboard:
[![Screenshot-2025-09-06-201824.png](https://i.postimg.cc/bY4snyh7/Screenshot-2025-09-06-201824.png)](https://postimg.cc/dDmsPKD6)
bill genrated in employee bashboard:
[![Screenshot-2025-08-21-224800.png](https://i.postimg.cc/bvvzMWP0/Screenshot-2025-08-21-224800.png)](https://postimg.cc/Mnh2fsvX)
sales button view in admin dashboard:
[![Screenshot-2025-08-19-151345.png](https://i.postimg.cc/FsgNKNsg/Screenshot-2025-08-19-151345.png)](https://postimg.cc/ZCR17kNC)

🚀 Features
🔑 Admin Role :
Secure Login with role-based access.

Central Dashboard for quick metrics.

Full CRUD operations on Employees, Products, Suppliers, and Categories.

Sales Monitoring with bill inspection.

Tax Management system.

👨‍💼 Employee Role :
Secure Employee Login.

Billing Dashboard for fast checkouts.

Product Search and Shopping Cart.

Bill Generation with discounts and tax.

QR Code generation for each bill.

Automated stock updates.

⚙️ Getting Started
Follow these steps to set up the project on your local machine.

-> first remove the icon folder and paste those icon images in main folder(inventory management system folder) if not it will give error to you.

✅ Prerequisites
Python 3.8+

MySQL Server

Git

🔽 Installation & Setup
Clone the repository:

Copy code
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
Create a virtual environment:

Copy code
python -m venv .venv
Activate it:

Windows: .\.venv\Scripts\activate

macOS/Linux: source .venv/bin/activate

Create requirements.txt and install dependencies:

Copy code:
pip freeze > requirements.txt
pip install -r requirements.txt

🗄️ Database Configuration
The application requires a MySQL database named inventory_system.

Connect to MySQL and create the database:

Copy code:
CREATE DATABASE IF NOT EXISTS inventory_system;
USE inventory_system;
Create the required tables (example for employee_data):

Copy code
CREATE TABLE employee_data (
  empid INT NOT NULL,
  name VARCHAR(100),
  email VARCHAR(100),
  gender VARCHAR(50),
  dob VARCHAR(30),
  contact VARCHAR(30),
  employement_type VARCHAR(50),
  education VARCHAR(50),
  work_shift VARCHAR(50),
  address VARCHAR(100),
  doj VARCHAR(30),
  salary VARCHAR(50),
  usertype VARCHAR(50),
  password VARCHAR(50),
  PRIMARY KEY (empid)
);
(Repeat for suppliers, categories, products, and tax tables as per your schema.)

Update your MySQL connection details in employees.py inside the connect_database() function.

▶️ Usage
Run the login script from the root directory:

Copy code:
python Login_page.py
You can then log in as Admin or Employee depending on your created users.

📦 Deployment
To package into an executable:

Install PyInstaller:

Copy code:
pip install pyinstaller
Build executable:

Copy code:
pyinstaller --onefile --windowed --add-data "images;images" Login_page.py
The final .exe will be in the dist/ folder.
