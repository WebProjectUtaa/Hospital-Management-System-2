import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.doctor_service import DoctorService

@pytest.mark.asyncio
async def test_get_doctor_appointments():
    # Mock veritabanı bağlantısı
    mock_conn = AsyncMock()
    mock_cursor = AsyncMock()

    # async with için gerekli yapılandırma
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.__aenter__.return_value = mock_cursor
    mock_cursor.__aexit__.return_value = None

    # Test için beklenen dönüş değeri
    mock_cursor.fetchall.return_value = [
        {"appointment_id": 1, "patient_id": 1, "appointment_date": "2024-12-30", "appointment_time": "10:00:00", "reason": "Checkup", "status": "confirmed"}
    ]

    # DoctorService fonksiyonunu çağırma
    appointments = await DoctorService.get_doctor_appointments(mock_conn, 1)

    # Beklenen değerleri kontrol etme
    assert len(appointments) == 1
    assert appointments[0]["appointment_id"] == 1
    assert appointments[0]["reason"] == "Checkup"
    assert appointments[0]["status"] == "confirmed"
