# 🎓 School Management System (SMS)

A comprehensive, full-featured **School Management System** built with **Django 6.0** — designed to streamline school administration, communication, and daily operations across multiple user roles.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

---

## ✨ Features

### 🔐 Role-Based Access Control
- **Admin** — Full system control, manage all modules
- **Teacher/Staff** — Class management, attendance, grading, leave applications
- **Student** — View grades, attendance, timetable, fees, homework
- **Parent** — Monitor child's academic progress
- **Driver** — Transport management

### 📚 Core Modules

| Module | Description |
|--------|-------------|
| **Student Management** | Admission, profiles, photo upload, parent linking |
| **Staff Management** | Employee records, designations, departments, photo upload |
| **Academics** | Classes, subjects, timetable, homework, exams & grading |
| **Attendance** | Daily attendance tracking for students |
| **Finance** | Fee structures, invoices, payment tracking |
| **Transport** | Drivers, vehicles, routes, fuel & maintenance logs |
| **Notifications** | Announcements and activity logging |

### 🖼️ Profile & Photo Management
- Upload photos for students, teachers, and drivers via the admin panel
- Photos displayed in admin list views with circular thumbnails
- Profile pages show uploaded photos with elegant fallback to initials

### 🎨 Modern UI
- Beautiful, responsive dashboard with glassmorphism design
- Role-specific dashboards with relevant statistics
- Profile pages for every user role
- Click-to-toggle dropdown menus
- Smooth animations and micro-interactions

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shashi7367/School-management-system-.git
   cd School-management-system-
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install django Pillow
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```
Open 👉 https://school-management-system-3qlo.vercel.app/


---

## 📁 Project Structure

```
SMS/
├── core/               # Authentication, dashboard routing, base templates
├── students/           # Student & parent management
├── staff/              # Teacher/staff management, leave, payslips
├── academics/          # Classes, subjects, exams, timetable, homework
├── finance/            # Fee structures, invoices, payments
├── transport/          # Drivers, vehicles, routes, maintenance/fuel logs
├── sms_project/        # Django project settings & root URL config
├── static/             # CSS, JS, images
├── templates/          # Shared templates (login pages)
├── media/              # Uploaded photos (auto-created)
└── manage.py
```

---

## 🔑 User Roles & Login

| Role | Login URL | Access |
|------|-----------|--------|
| Admin | `/admin/` | Full system administration |
| Teacher | `/login/teacher/` | Classes, grades, attendance, leave |
| Student | `/login/student/` | Dashboard, grades, fees, timetable |
| Transport Manager | `/login/transport/` | Vehicles, routes, drivers |

---

## 🛠️ Tech Stack

- **Backend:** Django 6.0 (Python)
- **Database:** SQLite (default, easily swappable to PostgreSQL)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Image Processing:** Pillow
- **Admin Theme:** Django Jazzmin
- **Icons:** Font Awesome 6



---

## 📧 Email Notifications

The system automatically sends welcome emails with login credentials when new students, teachers, or drivers are added through the admin panel.

Configure email settings in `sms_project/settings.py`:
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 👨‍💻 Author

**Shashi Ranjan**

- GitHub: [@shashi7367](https://github.com/shashi7367)

---

<p align="center">
  Made with ❤️ using Django
</p>
