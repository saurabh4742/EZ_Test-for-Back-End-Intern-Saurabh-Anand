# Secure File Sharing API

## Overview
A FastAPI backend for secure file sharing between users with different roles (ops, client). Supports user registration, email verification, JWT authentication, file upload (local), and secure download links.

---

## Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set environment variables
- `JWT_SECRET`: Secret key for JWT
- `ENCRYPTION_KEY`: 32-byte base64 key for Fernet
- `EMAIL_SENDER`: Email address for sending verification
- `EMAIL_PASSWORD`: App password for email sender
- `BASE_URL`: Public base URL of your API (e.g., http://localhost:8000)

### 3. Start the server
```bash
uvicorn app.main:app --reload
```

---

## API Reference

### 1. **User Signup**
- **Endpoint:** `POST /auth/signup`
- **Body (JSON):**
  ```json
  {
    "email": "user@example.com",
    "password": "yourpassword",
    "role": "ops" // or "client"
  }
  ```
- **Response:**
  ```json
  { "message": "Signup successful. Check your email to verify.", "verification_url": "..." }
  ```
- **Postman:**
  - Set method to POST, URL to `/auth/signup`, body to raw JSON as above.

---

### 2. **Email Verification**
- **Endpoint:** `GET /auth/verify-email/{token}`
- **How to use:**
  - Click the verification link sent to your email after signup, or paste it in your browser/Postman.
- **Response:**
  ```json
  { "message": "Email verified successfully" }
  ```

---

### 3. **User Login**
- **Endpoint:** `POST /auth/login`
- **Body (JSON):**
  ```json
  {
    "email": "user@example.com",
    "password": "yourpassword",
    "role": "ops" // or "client"
  }
  ```
- **Response:**
  ```json
  { "access_token": "...", "token_type": "bearer" }
  ```
- **Postman:**
  - Set method to POST, URL to `/auth/login`, body to raw JSON as above.
  - Copy the `access_token` for use in authenticated requests.

---

### 4. **File Upload (Ops Only)**
- **Endpoint:** `POST /ops/upload`
- **Auth:** Bearer token (must be an `ops` user)
- **Body (form-data):**
  - Key: `file` (type: File)
- **Allowed file types:** `.pptx`, `.docx`, `.xlsx`
- **Response:**
  ```json
  { "message": "File uploaded successfully" }
  ```
- **Postman:**
  - Set method to POST, URL to `/ops/upload`.
  - In Authorization tab, select Bearer Token and paste your `access_token`.
  - In Body tab, select form-data, add a key `file` (type: File), and choose a file.

---

### 5. **List Uploaded Files (Client Only)**
- **Endpoint:** `GET /client/files`
- **Auth:** Bearer token (must be a `client` user)
- **Response:**
  ```json
  [
    {
      "id": "uuid",
      "filename": "example.docx",
      "uploader_id": "uuid",
      "upload_time": "2024-06-01T12:00:00"
    },
    ...
  ]
  ```
- **Postman:**
  - Set method to GET, URL to `/client/files`.
  - In Authorization tab, select Bearer Token and paste your `access_token`.

---

### 6. **Generate Download Link (Client Only)**
- **Endpoint:** `GET /client/download-file/{file_id}`
- **Auth:** Bearer token (must be a `client` user)
- **Response:**
  ```json
  { "download_url": "/client/download/{token}" }
  ```
- **Postman:**
  - Set method to GET, URL to `/client/download-file/{file_id}`.
  - In Authorization tab, select Bearer Token and paste your `access_token`.

---

### 7. **Download File (Client Only)**
- **Endpoint:** `GET /client/download/{token}`
- **Auth:** Bearer token (must be a `client` user)
- **Response:**
  - Returns file metadata and path (you may want to update this to return the file directly).
- **Postman:**
  - Set method to GET, URL to `/client/download/{token}`.
  - In Authorization tab, select Bearer Token and paste your `access_token`.

---

## Authentication in Postman
1. Register and verify a user (as `ops` or `client`).
2. Log in to get your `access_token`.
3. For protected endpoints, go to Authorization tab, select Bearer Token, and paste your token.

---

## Notes
- Only `ops` users can upload files.
- Only `client` users can list and download files.
- Only `.pptx`, `.docx`, `.xlsx` files are allowed for upload.
- Files are stored in the local `uploads/` directory.
- Email verification is required before login.

---

## Example .env file
```
JWT_SECRET=your_jwt_secret
ENCRYPTION_KEY=your_fernet_key
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_email_app_password
BASE_URL=http://localhost:8000
```

---
4. **Start the server with Uvicorn**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 80 --reload
   ```
