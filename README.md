# 🏥 HealthyLife — AI-Driven Healthcare & Online Consultation Platform

HealthyLife is a full-stack healthcare platform designed to enable secure online consultations, intelligent diagnostics, doctor onboarding, and AI-powered patient support.

The platform focuses on scalability, security, and performance optimization, providing a real-world healthcare workflow simulation with production-ready backend architecture.

---

## 🚀 Key Features

- 🔐 Secure authentication with OTP verification and password hashing
- 👥 Role-Based Access Control (RBAC) for admin and users
- 🩺 Doctor onboarding and approval workflow with automated employee ID generation
- 📅 Appointment scheduling engine with availability validation and conflict prevention
- 🎥 Dynamic video consultation link generation using UUID-based meeting IDs
- 🤖 AI virtual nurse chatbot for conversational medical guidance
- 🧠 AI diagnostic prediction model using machine learning
- 📊 Admin analytics dashboard with aggregation insights
- ⭐ Feedback system with rating analytics
- 🧹 Automated cleanup of expired sessions, OTPs, and availability slots
- ⚡ Search request throttling to reduce duplicate queries
- 🗄️ MySQL connection pooling for optimized database performance

---

## 🧠 AI Capabilities

- Disease prediction using machine learning with feature vector encoding
- Conversational AI chatbot powered by LLM APIs
- Data-driven insights through analytics dashboards

---

## 🏗️ Architecture

The backend follows a **Modular Monolithic Architecture** with clear separation of:

- Routes
- Services
- Models
- Database Layer

This structure ensures maintainability, scalability, and clean code organization.

---

## 🔐 Security Features

- OTP-based authentication
- Password hashing
- Server-side session management (MySQL)
- Role-based authorization
- Secure cookie configuration
- Environment-based secrets management

---

## ⚡ Performance Optimizations

- MySQL connection pooling
- Request throttling (0.5s cooldown)
- Async email handling using background threads
- Indexed queries for faster lookups
- Gunicorn worker configuration for concurrency

---

## 🛠️ Tech Stack

**Backend:** Python • Flask • REST APIs  
**Database:** MySQL • Connection Pooling  
**AI / ML:** Scikit-learn • Pandas • NumPy  
**Frontend:** HTML • CSS • JavaScript  
**Infrastructure:** Gunicorn • Docker • Environment Variables  

### Infrastructure

- Gunicorn
- Docker (optional deployment)
- Environment variables

## 📊 Scalability

The system is optimized to handle concurrent traffic using worker processes, connection pooling, and request throttling, ensuring stable performance under load.

---

## 📌 Installation Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Mahboob-Attar/HealthyLife-Online-Consultation-Platform.git
cd HealthyLife-Online-Consultation-Platform
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables

Create a .env file in the root directory:

```bash
# Flask
SECRET_KEY=your_secret_key

# Database
DB_HOST=localhost
DB_USER=your_user
DB_PASS=your_password
DB_NAME=healthydb

# Email SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your_email
SMTP_PASS=your_password

# Admin
ADMIN_EMAIL=admin_email
ADMIN_PASSWORD=admin_password

# AI API
OPENROUTER_KEY=your_api_key
```

### 4️⃣ Run Application

```bash
python -m server.run
```

App will be available at: http://localhost:00.00.0.0000

---

## 🐳 Docker Deployment (Optional)

You can run HealthyLife using Docker without installing dependencies manually.

---

### 📦 Prerequisites

Make sure Docker is installed on your system.

Check installation:

```bash
docker --version
```

🏗️ Build Docker Image

```bash
docker build -t healthylife .
```

🚀 Run Container

```bash
docker run -p 5000:5000 healthylife
```

📈 Future Improvements

Kubernetes auto-scaling

Redis caching

Async task queue (Celery)

Full load testing

Microservices architecture

👤 Author

Mahiboob Isak Attar

GitHub: https://github.com/Mahboob-Attar

LinkedIn: https://www.linkedin.com/in/mahboob-attar

Email: mahboobattar78@gmail.com
