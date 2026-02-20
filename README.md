# Appointment System

A multi-tenant appointment management system backend built with Python, FastAPI, and SQLite3. Designed to be sold to companies — each company is identified by a `company_id` so appointments are scoped per company. Includes JWT-based authentication with role-based access control.

## Tech Stack

- **Language:** Python 3.11+
- **Framework:** FastAPI + Uvicorn
- **Database:** SQLite3 (stored at `/testbed/db/appointment_system.db`)
- **Validation:** Pydantic v2
- **Authentication:** JWT (PyJWT) + bcrypt password hashing

## Architecture

The project follows an **N-Layered Architecture** with clear separation of concerns:

```
backend/
├── main.py                                  # FastAPI app entry point
├── requirements.txt                         # Python dependencies
├── api/                                     # Presentation Layer
│   ├── controllers/
│   │   ├── appointment_controller.py        #   Appointment API routes
│   │   ├── auth_controller.py               #   Auth API routes (register/login)
│   │   └── offering_controller.py           #   Offering API routes
│   └── dependencies/
│       └── auth_dependency.py               #   JWT auth & role-check dependencies
├── business/                                # Business Logic Layer
│   └── services/
│       ├── appointment_service.py           #   Appointment business rules
│       ├── auth_service.py                  #   Auth logic (register/login/JWT/seed)
│       └── offering_service.py             #   Offering business rules
├── data_access/                             # Data Access Layer
│   ├── db_context.py                        #   SQLite connection & schema init
│   └── repositories/
│       ├── appointment_repository.py        #   Appointment CRUD
│       ├── offering_repository.py           #   Offering CRUD
│       └── user_repository.py               #   User CRUD
└── models/                                  # Models Layer
    ├── entities/
    │   ├── appointment.py                   #   Appointment domain entity
    │   ├── offering.py                      #   Offering domain entity
    │   └── user.py                          #   User domain entity
    ├── dtos/
    │   ├── appointment_dto.py               #   Appointment request/response DTOs
    │   ├── auth_dto.py                      #   Auth request/response DTOs
    │   └── offering_dto.py                  #   Offering request/response DTOs
    └── enums/
        ├── appointment_status.py            #   Appointment status enum
        └── role.py                          #   User role enum
```

### Layer Responsibilities

| Layer | Purpose |
|-------|---------|
| **Presentation** (`api/`) | HTTP routing, request/response handling, auth dependencies |
| **Business Logic** (`business/`) | Business rules, validation, JWT token management |
| **Data Access** (`data_access/`) | Database connections and CRUD operations |
| **Models** (`models/`) | Entities, DTOs, and enums shared across layers |

## Authentication & Authorization

### Default Admin Account

A default admin user is **automatically seeded** on first startup:

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin123` |
| Email | `admin@appointment-system.com` |

> ⚠️ **Change the default admin password immediately in production.**

### Roles

| Role | Description |
|------|-------------|
| `admin` | Full access — manages all companies, accounts, offerings, and appointments |
| `company` | Scoped to their own company — can create offerings and manage their own appointments |

> **Note:** End users (customers) do not need accounts. They browse open offerings and create appointments directly via public endpoints.

### Access Control Matrix

| Endpoint | Public | ADMIN | COMPANY |
|----------|--------|-------|---------|
| `POST /api/auth/login` | ✅ | ✅ | ✅ |
| `POST /api/auth/register` | ❌ | ✅ | ❌ |
| `GET /api/auth/me` | ❌ | ✅ | ✅ |
| `POST /api/offerings/` | ❌ | ❌ | ✅ |
| `GET /api/offerings/company/{id}` | ✅ (open only) | ✅ (open only) | ✅ (open only) |
| `GET /api/offerings/` | ❌ | ❌ | ✅ (own, all statuses) |
| `GET /api/offerings/{id}` | ❌ | ✅ (any) | ✅ (own company) |
| `PUT /api/offerings/{id}` | ❌ | ✅ (any) | ✅ (own company) |
| `POST /api/appointments/` | ✅ | ✅ | ✅ |
| `GET /api/appointments/` | ❌ | ✅ (all) | ✅ (own company) |
| `GET /api/appointments/{id}` | ❌ | ✅ (all) | ✅ (own company) |
| `PUT /api/appointments/{id}` | ❌ | ✅ (all) | ✅ (own company) |

### How It Works

1. On first startup, a default **admin** account is created automatically
2. The admin logs in via `POST /api/auth/login` to get a JWT token
3. The admin creates company accounts via `POST /api/auth/register` (🔒 admin only)
4. Companies log in and **create offerings** that describe what they provide
5. Customers browse a company's **open offerings** via the public `GET /api/offerings/company/{id}` endpoint
6. Customers create appointments by choosing an offering via the **public** `POST /api/appointments/` endpoint
7. Admins and companies can **edit** appointments and offerings

## Data Models

### User

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Auto-generated primary key |
| `username` | string | Unique username |
| `password_hash` | string | bcrypt-hashed password |
| `email` | string | Unique email address |
| `role` | enum | `admin`, `company` |
| `company_id` | integer/null | Company association (required for `company` role) |
| `created_date` | datetime | Auto-set to UTC now on creation |

### Offering

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Auto-generated primary key |
| `company_id` | integer | The company that owns this offering |
| `description` | string | Text description displayed to users |
| `is_open` | boolean | Whether the offering is available for booking |
| `created_date` | datetime | Auto-set to UTC now on creation |

### Appointment

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Auto-generated primary key |
| `company_id` | integer | Identifies which company the appointment belongs to |
| `offering_id` | integer | Reference to the offering being booked (must be open) |
| `customer_name` | string | Name of the customer |
| `customer_phone` | string | Phone number of the customer |
| `customer_email` | string | Email address of the customer (validated) |
| `start_date` | datetime | Appointment start time |
| `end_date` | datetime | Appointment end time |
| `created_date` | datetime | Auto-set to UTC now on creation |
| `status` | enum | `pending`, `approved`, `denied`, `cancelled`, `deleted` |

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/login` | Login and get JWT token |
| `POST` | `/api/auth/register` | Create admin/company account (🔒 admin only) |
| `GET` | `/api/auth/me` | Get current user info (🔒 authenticated) |

### Offerings

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/offerings/` | Create offering (🔒 company only) |
| `GET` | `/api/offerings/company/{company_id}` | List open offerings for a company (🌐 public) |
| `GET` | `/api/offerings/` | List own offerings — all statuses (🔒 company) |
| `GET` | `/api/offerings/{id}` | Get offering by ID (🔒 admin, company) |
| `PUT` | `/api/offerings/{id}` | Update offering (🔒 admin, company) |

### Appointments

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/appointments/` | Create appointment (🌐 public — offering must be open) |
| `GET` | `/api/appointments/` | List appointments (🔒 admin, company) |
| `GET` | `/api/appointments/{id}` | Get appointment by ID (🔒 admin, company) |
| `PUT` | `/api/appointments/{id}` | Update appointment (🔒 admin, company) |

## Usage Examples

### 1. Login as admin

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

### 2. Create a company account (admin only)

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <admin_token>" \
  -d '{
    "username": "acme_corp",
    "password": "securepass123",
    "email": "admin@acme.com",
    "role": "company",
    "company_id": 1
  }'
```

### 3. Create an offering (company only)

```bash
curl -X POST http://localhost:8000/api/offerings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <company_token>" \
  -d '{
    "description": "30-minute consultation"
  }'
```

### 4. Browse open offerings (public)

```bash
curl http://localhost:8000/api/offerings/company/1
```

### 5. Create appointment (public — no auth needed)

```bash
curl -X POST http://localhost:8000/api/appointments/ \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": 1,
    "offering_id": 1,
    "customer_name": "John Doe",
    "customer_phone": "+1234567890",
    "customer_email": "john@example.com",
    "start_date": "2026-03-01T10:00:00",
    "end_date": "2026-03-01T11:00:00"
  }'
```

### 6. Update appointment (admin or company)

```bash
curl -X PUT http://localhost:8000/api/appointments/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "status": "approved"
  }'
```

## Getting Started

### Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### Run the Server

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

The API documentation (Swagger UI) is available at: `http://localhost:8000/docs`