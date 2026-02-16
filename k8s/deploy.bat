@echo off
REM Windows deployment script for Kubernetes

echo ========================================
echo Todo App - Kubernetes Deployment Script
echo ========================================
echo.

REM Step 1: Start Minikube
echo [1/6] Starting Minikube cluster...
minikube status >nul 2>&1
if %errorlevel% neq 0 (
    echo Minikube is not running. Starting...
    minikube start
) else (
    echo Minikube is already running.
)
echo.

REM Step 2: Build Docker images
echo [2/6] Building Docker images...
cd ..
docker build -t todo-backend:latest -f backend/Dockerfile .
if %errorlevel% neq 0 (
    echo ERROR: Failed to build backend image
    exit /b 1
)

docker build -t todo-frontend:latest -f frontend/Dockerfile .
if %errorlevel% neq 0 (
    echo ERROR: Failed to build frontend image
    exit /b 1
)
echo Docker images built successfully.
echo.

REM Step 3: Load images into Minikube
echo [3/6] Loading images into Minikube...
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
echo Images loaded into Minikube.
echo.

REM Step 4: Apply Kubernetes manifests
echo [4/6] Deploying to Kubernetes...
cd k8s
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f pvc.yaml
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml
echo Kubernetes resources created.
echo.

REM Step 5: Wait for pods to be ready
echo [5/6] Waiting for pods to be ready...
kubectl wait --for=condition=ready pod -l app=todo-backend -n todo-app --timeout=120s
kubectl wait --for=condition=ready pod -l app=todo-frontend -n todo-app --timeout=120s
echo.

REM Step 6: Display access information
echo [6/6] Deployment complete!
echo.
echo ========================================
echo Access Information:
echo ========================================
kubectl get pods -n todo-app
echo.
kubectl get services -n todo-app
echo.
echo To access the frontend, run:
echo   minikube service frontend-service -n todo-app
echo.
echo To access the backend API directly, run:
echo   kubectl port-forward -n todo-app svc/backend-service 8000:8000
echo.
echo ========================================
