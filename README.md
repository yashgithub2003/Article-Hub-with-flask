# 📝 Article Hub – Flask Article Platform

A secure and easy-to-use article publishing platform built with **Flask**, **MySQL**, and **Bootstrap**. Users can register, log in, create, edit, and delete their own articles with rich-text support.

---

## 🚀 Features

* User Registration & Login (with password hashing)
* Secure Authentication (session-based)
* Create, Edit & Delete Articles
* Rich Text Editor (CKEditor)
* User-specific Dashboard
* MySQL Database Integration
* CSRF Protection (Flask-WTF)
* XSS Protection (Bleach sanitization)
* Clean & Responsive UI (Bootstrap)

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Frontend:** HTML, Jinja2, Bootstrap
* **Database:** MySQL
* **Forms & Validation:** Flask-WTF, WTForms
* **Security:** Passlib, Bleach

---

## 📂 Project Structure

```
project/
│
├── app.py
├── templates/
│   ├── layout.html
│   ├── home.html
│   ├── about.html
│   ├── articles.html
│   ├── article.html
│   ├── dashboard.html
│   ├── add_article.html
│   ├── edit_article.html
│   └── includes/
│       ├── navbar.html
│       └── _messages.html
│
├── static/
│   └── css/
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/article-hub.git
cd article-hub
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install flask flask-mysqldb flask-wtf passlib bleach
```

### 4️⃣ Configure MySQL Database

Create a database named `myflaskapp` and run:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    username VARCHAR(50),
    password VARCHAR(255)
);

CREATE TABLE articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200),
    body TEXT,
    author VARCHAR(50),
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Update MySQL config in `app.py` if needed:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'myflaskapp'
```

---

## ▶️ Run the App

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

## 🔐 Security Highlights

* Passwords are hashed using **sha256_crypt**
* HTML content is sanitized using **Bleach** to prevent XSS
* Routes are protected using login decorators
* CSRF protection enabled via **Flask-WTF**
* Users can only edit/delete their own articles

---

## 📸 Screens (Optional)

Add screenshots here to make the project more attractive:

```
Home Page
Dashboard
Add Article Page
Edit Article Page
```

---

## 🧪 Example Routes

| Route                  | Description    |
| ---------------------- | -------------- |
| `/`                    | Home Page      |
| `/about`               | About Page     |
| `/register`            | Register User  |
| `/login`               | Login User     |
| `/dashboard`           | User Dashboard |
| `/add_article`         | Add Article    |
| `/edit_article/<id>`   | Edit Article   |
| `/delete_article/<id>` | Delete Article |

---

## 🌟 Future Improvements

* User profile page
* Article categories & tags
* Search functionality
* Pagination
* Comments system
* Like / bookmark articles

---

## 👨‍💻 Author

Developed by **Your Name**
📧 Email: [your@email.com](mailto:your@email.com)
🌐 GitHub: [https://github.com/yourusername](https://github.com/yourusername)

---

## 📄 License

This project is for educational purposes. You are free to use and modify it.

---

> If you like this project, don’t forget to ⭐ star the repository!
