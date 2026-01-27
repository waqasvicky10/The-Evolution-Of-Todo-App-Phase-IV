@echo off
echo ========================================
echo Test Authentication Endpoints
echo ========================================
echo.

echo Testing registration with new email...
echo.

curl -X POST "http://127.0.0.1:8000/api/auth/register" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\": \"testuser@example.com\", \"password\": \"Test1234!\", \"password_confirmation\": \"Test1234!\"}"

echo.
echo.
echo If you see 409 error, email exists - try login instead:
echo.

curl -X POST "http://127.0.0.1:8000/api/auth/login" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\": \"testuser@example.com\", \"password\": \"Test1234!\"}"

echo.
echo.
pause
