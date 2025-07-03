import pytest
from httpx import AsyncClient
from app.main import app
import uuid
import io

@pytest.mark.asyncio
async def test_upload_file():
    # Register and verify an ops user
    email = f"ops_{uuid.uuid4()}@example.com"
    payload = {"email": email, "password": "TestPassword123!", "role": "ops"}
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        resp = await ac.post("/auth/signup", json=payload)
        assert resp.status_code == 200
        token = resp.json()["verification_url"].split("/")[-1]
        await ac.get(f"/auth/verify-email/{token}")
        login_resp = await ac.post("/auth/login", json=payload)
        assert login_resp.status_code == 200
        access_token = login_resp.json()["access_token"]
        # Upload file
        file_content = b"Test file content"
        files = {"file": ("test.docx", io.BytesIO(file_content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        upload_resp = await ac.post(
            "/ops/upload",
            files=files,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert upload_resp.status_code == 200
        assert upload_resp.json()["message"] == "File uploaded successfully"
        # Save for next test
        test_upload_file.ops_token = access_token

@pytest.mark.asyncio
async def test_list_files():
    # Register and verify a client user
    email = f"client_{uuid.uuid4()}@example.com"
    payload = {"email": email, "password": "TestPassword123!", "role": "client"}
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        resp = await ac.post("/auth/signup", json=payload)
        assert resp.status_code == 200
        token = resp.json()["verification_url"].split("/")[-1]
        await ac.get(f"/auth/verify-email/{token}")
        login_resp = await ac.post("/auth/login", json=payload)
        assert login_resp.status_code == 200
        access_token = login_resp.json()["access_token"]
        # List files
        files_resp = await ac.get(
            "/client/files",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert files_resp.status_code == 200
        files_list = files_resp.json()
        assert isinstance(files_list, list)
        if files_list:
            test_list_files.file_id = files_list[0]["id"]
        test_list_files.client_token = access_token

@pytest.mark.asyncio
async def test_download_file():
    file_id = getattr(test_list_files, "file_id", None)
    client_token = getattr(test_list_files, "client_token", None)
    assert file_id is not None and client_token is not None
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Generate download link
        link_resp = await ac.get(
            f"/client/download-file/{file_id}",
            headers={"Authorization": f"Bearer {client_token}"}
        )
        assert link_resp.status_code == 200
        download_url = link_resp.json()["download_url"]
        token = download_url.split("/")[-1]
        # Download file
        download_resp = await ac.get(
            f"/client/download/{token}",
            headers={"Authorization": f"Bearer {client_token}"}
        )
        assert download_resp.status_code == 200
        assert "filename" in download_resp.json()
