@echo off
REM Phase IV Deployment Script
echo ========================================
echo Todo App - Phase IV Kubernetes Deployment
echo ========================================
echo.

REM 1. Start Minikube
echo [1/5] Checking Minikube status...
minikube status >nul 2>&1
if %errorlevel% neq 0 (
    echo Minikube is not running. Starting...
    minikube start
) else (
    echo Minikube is running.
)
echo.

REM 2. Build Docker Images
echo [2/5] Building Docker images...
cd ..\..
if not exist backend\Dockerfile (
    echo ERROR: Cannot find backend\Dockerfile. Run this script from phase_iv\scripts
    exit /b 1
)

echo Building Backend (Optimized)...
docker build -t todo-backend:optimized -f backend/Dockerfile .
if %errorlevel% neq 0 (
    echo ERROR: Backend build failed
    exit /b 1
)

echo Building Frontend (Optimized)...
docker build -t todo-frontend:optimized -f frontend/Dockerfile .
if %errorlevel% neq 0 (
    echo ERROR: Frontend build failed
    exit /b 1
)
echo Images built successfully.
echo.

REM 3. Load Images to Minikube
echo [3/5] Loading images into Minikube...
echo Loading Backend...
minikube image load todo-backend:optimized
echo Loading Frontend...
minikube image load todo-frontend:optimized
echo Images loaded.
echo.

REM 4. Deploy with Helm
echo [4/5] Deploying with Helm...
cd phase_iv
helm lint helm\todo-app
if %errorlevel% neq 0 (
    echo WARNING: Helm lint found issues. Proceeding anyway...
)

echo Installing/Upgrading Release...
helm upgrade --install todo-app helm\todo-app --namespace todo-app --create-namespace
echo Deployment commands sent.
echo.

REM 5. Verification
echo [5/5] Verifying Deployment...
echo Waiting for pods to spark to life...
kubectl wait --for=condition=ready pod -l app=todo-app -n todo-app --timeout=120s

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo Access URLs:
minikube service frontend-service -n todo-app --url
echo.
echo To access the frontend, open the URL above.
echo To check backend health: kubectl port-forward -n todo-app svc/backend-service 8000:8000
echo.
pause
