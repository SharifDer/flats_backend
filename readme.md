# Sakan Sanaa Backend

This is the backend service for the **Sakan Sanaa** web application, built using FastAPI. It manages user authentication, apartment listings, and data integration with Firebase and Cloudinary.

## Features

- User registration and login via Firebase
- JWT-based authentication
- Apartment posting with image uploads
- Apartment search and detail view
- Status updates for apartment listings

## Tech Stack

- **FastAPI** – Web framework
- **Firebase** – Authentication
- **Cloudinary** – Image storage
- **Pydantic** – Request and response models

## API Endpoints

### Auth

- `POST /auth/create-user`  
  Create a new Firebase user and a corresponding database record.

- `POST /auth/login`  
  Authenticate and receive JWT token.

### Apartments

- `POST /apartments`  
  Create a new apartment (requires auth).  
  **Payload:** multipart/form-data with title, type, address, price, images, etc.

- `GET /apartments`  
  List apartments with filters.  
  **Query Params:** defined in `ReqApartments`.

- `GET /apartments/details`  
  Fetch detailed info for a specific apartment.

- `PATCH /apartments/status`  
  Update the status of an apartment (requires auth).

## Project Structure
backend/
├── app/                     # Authentication, routing, and request handling
│   ├── auth.py
│   ├── data_fetcher.py
│   
├── services/                # Business logic and integration layers
│   ├── apartment_services.py
│   ├── storage_cloudinary.py
│   └── user_services.py
├── config.py                # Centralized configuration and route constants
├── app_dtypes/              # Pydantic request and response models
│   ├── request_dtypes.py
│   └── response_dtypes.py
└── fastapi_app.py                  # FastAPI app entry point


