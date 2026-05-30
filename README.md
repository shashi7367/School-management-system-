# 🎓 School Management System (SMS)

A comprehensive, full-featured **School Management System** built with **Django 6.0**, designed to streamline academic and administrative operations for educational institutions. The platform provides role-based access, centralized data management, attendance tracking, examination management, fee handling, transport monitoring, and communication tools through a modern web interface.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![SQLite](https://img.shields.io/badge/SQLite-Database-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Project Overview

Managing school operations manually can be time-consuming, error-prone, and difficult to scale. This project provides a centralized digital solution that automates student management, staff administration, attendance tracking, academic activities, fee management, and transportation services.

The system supports multiple user roles including administrators, teachers, students, parents, and drivers, ensuring secure access and efficient workflow management.

---

## 🎯 Problem Statement

Educational institutions often face challenges such as:

* Manual record management
* Attendance tracking inefficiencies
* Difficulty in monitoring student performance
* Communication gaps between school and parents
* Complex fee and transport management
* Lack of centralized data access

### Solution

The School Management System addresses these challenges by providing:

✅ Centralized data management

✅ Role-based access control

✅ Automated attendance and grading

✅ Fee and payment tracking

✅ Transport monitoring

✅ Parent-student communication support

✅ Real-time administrative insights

---

# ✨ Key Features

## 🔐 Role-Based Access Control

### 👨‍💼 Admin

* Full system administration
* Manage students, staff, classes, and fees
* Generate reports
* Monitor all activities

### 👩‍🏫 Teacher / Staff

* Manage attendance
* Upload grades
* Assign homework
* Apply for leave
* View schedules

### 🎓 Student

* View attendance records
* Access grades and exam results
* Check timetable
* Monitor fee status
* View homework assignments

### 👨‍👩‍👧 Parent

* Track child performance
* Monitor attendance
* View examination results
* Stay updated with school activities

### 🚌 Driver

* Manage transport operations
* View assigned routes
* Update vehicle status

---

# 📚 Core Modules

| Module             | Description                                       |
| ------------------ | ------------------------------------------------- |
| Student Management | Admission, profiles, parent linking, photo upload |
| Staff Management   | Employee records, departments, designations       |
| Academics          | Subjects, classes, timetable, exams, grading      |
| Attendance         | Daily attendance tracking and monitoring          |
| Finance            | Fee structures, invoices, payment management      |
| Transport          | Drivers, vehicles, routes, maintenance logs       |
| Notifications      | Announcements and activity tracking               |
| User Management    | Authentication and role-based permissions         |

---

# 🖼️ Profile & Media Management

### Features

* Student photo uploads
* Teacher profile management
* Driver profile images
* Circular thumbnail previews
* Initial-based avatar fallback
* Media file management through Django

---

# 🎨 Modern User Interface

* Responsive design
* Glassmorphism-inspired dashboard
* Role-specific dashboards
* Interactive statistics cards
* Dropdown navigation menus
* Smooth animations
* Mobile-friendly layouts
* User profile pages

---

# 🏗️ System Architecture

```text
Users
 │
 ▼
Authentication & Authorization
 │
 ▼
Role-Based Dashboard
 │
 ├── Student Management
 ├── Staff Management
 ├── Academics
 ├── Attendance
 ├── Finance
 ├── Transport
 └── Notifications
 │
 ▼
SQLite Database
```

---

# 🛠️ Technology Stack

## Backend

* Python
* Django 6.0

## Database

* SQLite
* PostgreSQL (Supported)

## Frontend

* HTML5
* CSS3
* JavaScript

## Libraries & Tools

* Pillow
* Django Jazzmin
* Font Awesome 6

## Version Control

* Git
* GitHub

---

# 📂 Project Structure

```text
SMS/
├── core/
│   ├── authentication
│   ├── dashboard routing
│   └── base templates
│
├── students/
│   ├── student management
│   └── parent management
│
├── staff/
│   ├── employee management
│   ├── leave system
│   └── payslips
│
├── academics/
│   ├── classes
│   ├── subjects
│   ├── timetable
│   ├── homework
│   └── examinations
│
├── finance/
│   ├── fee structures
│   ├── invoices
│   └── payments
│
├── transport/
│   ├── drivers
│   ├── vehicles
│   ├── routes
│   └── maintenance logs
│
├── static/
├── templates/
├── media/
├── sms_project/
└── manage.py
```

---

# 🚀 Installation & Setup

## Prerequisites

* Python 3.10+
* pip
* Git

### Clone Repository

```bash
git clone https://github.com/shashi7367/School-management-system-.git
cd School-management-system-
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install django Pillow
```

### Apply Migrations

```bash
python manage.py migrate
```

### Create Admin User

```bash
python manage.py createsuperuser
```

### Run Server

```bash
python manage.py runserver
```

### Open Application

```text
http://127.0.0.1:8000/
```

---

# 🔑 Login Access

| Role              | URL               | Access                 |
| ----------------- | ----------------- | ---------------------- |
| Admin             | /admin/           | Full System Access     |
| Teacher           | /login/teacher/   | Academics & Attendance |
| Student           | /login/student/   | Results & Dashboard    |
| Transport Manager | /login/transport/ | Vehicles & Routes      |

---

# 📧 Email Notification System

The application automatically sends welcome emails when:

* New students are added
* New teachers are registered
* New drivers are onboarded

Configure email settings:

```python
EMAIL_HOST_USER = "your-email@gmail.com"
EMAIL_HOST_PASSWORD = "your-app-password"
```

---

# 📊 Benefits

### For Schools

* Reduced paperwork
* Improved administrative efficiency
* Better record management

### For Teachers

* Simplified attendance tracking
* Faster grading process

### For Students

* Easy access to academic records
* Transparent performance monitoring

### For Parents

* Real-time academic updates
* Better engagement with school activities

---

# 🔮 Future Scope

The system can be enhanced with several advanced features:

### 🤖 AI & Analytics

* AI-powered student performance prediction
* Attendance trend analysis
* Personalized learning recommendations
* Academic risk detection

### 📱 Mobile Applications

* Android application
* iOS application
* Parent mobile portal
* Teacher mobile dashboard

### 💳 Online Payments

* Razorpay integration
* Stripe integration
* UPI fee payments
* Automatic receipt generation

### 📡 Real-Time Features

* Live notifications
* Real-time messaging
* In-app communication system
* Push notifications

### ☁️ Cloud Deployment

* AWS deployment
* Azure deployment
* Docker containerization
* Kubernetes support

### 🎥 Smart Classroom Integration

* Online class management
* Video conferencing integration
* Digital assignments
* Learning Management System (LMS)

### 🚌 Smart Transport

* GPS vehicle tracking
* Route optimization
* Parent live tracking
* Driver mobile app

### 🔐 Security Enhancements

* Two-Factor Authentication (2FA)
* Biometric attendance
* Face recognition system
* Advanced audit logging

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit changes

```bash
git commit -m "Add new feature"
```

4. Push changes

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

---

# 👨‍💻 Author

## Shashi Ranjan Kumar

B.Tech Computer Science & Engineering
Lovely Professional University (LPU)

### Connect With Me

GitHub: https://github.com/shashi7367

---

# 📜 License

This project is developed for educational, academic, and portfolio purposes. Feel free to fork, modify, and extend the project according to your requirements.

---

## ⭐ Support

If you found this project useful, please consider giving it a **Star ⭐** on GitHub.

Your support motivates future improvements and new features!
