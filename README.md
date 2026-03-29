# 🚀 Academic Cell API – Event & Testing Management

<div align="center">

![Python](https://img.shields.io/badge/python-v3.12+-blue.svg)
![Django](https://img.shields.io/badge/django-v5.0+-092e20.svg)
![DRF](https://img.shields.io/badge/DRF-v3.15+-red.svg)
![AWS](https://img.shields.io/badge/AWS%20S3-FF9900.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**A high-performance REST API for university event management with a focus on QA Automation and Cloud Scalability**

[🧪 Testing Strategy](#-testing-strategy-qa-focus) • [☁️ Cloud Integration](#-cloud-infrastructure) • [🛠️ Setup](#-installation-and-setup) • [🗄️ Database](#️-database-structure)

</div>

---

## 📖 General Overview

This backend system, developed with **Django** and **Django Rest Framework**, was designed to manage the "Célula Académica" (Academic Cell) at my university. It handles complex relationships between events, speakers, and student enrollments, ensuring data integrity through a robust **Automated Testing Suite**.

### 🎯 Key Features

- ⚡ **RESTful Architecture**: Optimized endpoints for high-performance data retrieval.
- ☁️ **Stateless Media**: Full integration with **AWS S3** for image and file hosting.
- 🔐 **Token Security**: Secure authentication and Role-Based Access Control (RBAC).
- 🧪 **QA Driven**: Built-in integration tests for every critical business flow.

---

## 🧪 Testing Strategy (QA Focus)

As an engineer with a focus on quality, I implemented a layered testing strategy to ensure zero-regression during development.

### 📊 **Test Coverage Areas**
<table>
<tr>
<td width="50%">

### 🔗 **Integration Testing**
- ✅ **CRUD Validation**: Testing `POST`, `GET`, `PUT`, and `DELETE` on all resources.
- ✅ **Status Code Compliance**: Ensuring strict adherence to HTTP standards.
- ✅ **Payload Integrity**: Validating JSON responses against expected schemas.

</td>
<td width="50%">

### 🖱️ **Functional & E2E**
- ✅ **Selenium IDE**: Automated UI flows for critical user journeys.
- ✅ **Authentication**: Testing Token generation and expiration.
- ✅ **Permissions**: Ensuring non-admin users cannot modify sensitive data.

</td>
</tr>
</table>

### 💻 **Integration Test Example**

```python
# Path: eventos/tests/test_integration.py
class ConcursoListCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('api_concursos_list_create')
        self.concurso_data = {
            'nombre': 'Programming Contest',
            'valor_inscripcion': '10.00',
            'competencia_individual': True,
        }

    @tag('integration')
    def test_create_concurso(self):
        response = self.client.post(self.url, self.concurso_data, format='json')
        print(f'Response Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Concurso.objects.get().nombre, 'Programming Contest')
```

---

## ☁️ Cloud Infrastructure

To ensure scalability, the project is configured to handle media files in the cloud using **AWS S3** rather than local storage.

### 📦 **AWS S3 Configuration**
```python
# settings.py configuration snippet
INSTALLED_APPS += ['storages']

AWS_STORAGE_BUCKET_NAME = 'celula-academica-bucket'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
```

---

## 🏗️ System Architecture

| Layer | Technology | Description |
|-------|------------|-------------|
| **Backend** | Django 5.0 | Core logic and ORM management |
| **API** | DRF 3.15 | Serialization and REST Endpoints |
| **Storage** | AWS S3 | External asset hosting (Images/Docs) |
| **Database** | PostgreSQL | Relational data persistence |
| **Server** | Gunicorn/Uvicorn | High-concurrency WSGI/ASGI servers |

---

## 🗄️ Database Structure

### 📊 Main Tables Summary

<details>
<summary><b>🏦 Table: eventos_concurso</b></summary>

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int4` | Primary Key |
| `nombre` | `varchar` | Contest name |
| `valor_inscripcion` | `decimal` | Cost to enter |
| `fecha_inicio` | `date` | Start date |

</details>

<details>
<summary><b>👤 Table: users_customuser</b></summary>

| Field | Type | Description |
|-------|------|-------------|
| `id` | `uuid` | Primary Key |
| `email` | `varchar` | Unique identifier |
| `categoria_id` | `int4` | Foreign Key -> Groups |

</details>

---

## 🛠️ Installation and Setup

### Prerequisites
- Python 3.12+
- AWS Credentials (for S3 storage)
- PostgreSQL Database

### 🚀 Quick Setup

```bash
# 1. Clone the repository
git clone [https://github.com/Dionisio202/back-celula-academica.git](https://github.com/Dionisio202/back-celula-academica.git)
cd back-celula-academica

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Migrations
python manage.py migrate

# 4. Run Integration Tests
python manage.py test --tag=integration
```

---

## 🛡️ Dependencies Highlights

```text
asgiref==3.8.1       # Async support for Python
boto3==1.34.131      # AWS SDK for Python
django-storages      # S3 Backend for Django media
djangorestframework  # REST API Development Framework
psycopg2-binary      # PostgreSQL database adapter
```

---

<div align="center">

### ⭐ If you find this QA-focused backend useful, give it a star!

</div>
