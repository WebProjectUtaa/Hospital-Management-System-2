Write-Host "Starting all microservices..."

Start-Process -NoNewWindow -FilePath "python" -ArgumentList "auth_service/main.py"
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "appointment_service/main.py"
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "doctor_service/main.py"
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "lab_test_service/main.py"
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "login_service/main.py"
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "notification_service/main.py"
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "nurse_service/main.py"
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "patient_service/main.py"
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "registration_service/main.py"
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "admin_service/main.py"

Write-Host "All microservices sta. Press Ctrl+C to stop."
