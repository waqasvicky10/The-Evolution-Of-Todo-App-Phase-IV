# Phase IV Verification Commands

## Prerequisites Check
```powershell
# Verify Minikube is installed
minikube version

# Verify kubectl is installed
kubectl version --client

# Verify Helm is installed
helm version

# Verify Docker is running
docker ps
```

## Helm Chart Validation ✅
```powershell
# Lint backend chart
helm lint charts/todo-backend/
# Expected: "1 chart(s) linted, 0 chart(s) failed"

# Lint frontend chart
helm lint charts/todo-frontend/
# Expected: "1 chart(s) linted, 0 chart(s) failed"

# Dry-run backend installation
helm install todo-backend charts/todo-backend/ --dry-run --debug

# Dry-run frontend installation
helm install todo-frontend charts/todo-frontend/ --dry-run --debug
```

## Deployment Test Commands
```powershell
# 1. Start Minikube
minikube start --driver=docker --cpus=2 --memory=3072mb

# 2. Configure Docker environment for Minikube
& minikube docker-env --shell powershell | Invoke-Expression

# 3. Build backend image
docker build -f docker/backend.Dockerfile -t todo-backend:latest .

# 4. Build frontend image
docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .

# 5. Verify images
docker images | Select-String "todo"

# 6. Create secrets (copy template first)
cp k8s/secrets-template.yaml k8s/secrets.yaml
# Edit k8s/secrets.yaml with actual values, then:
kubectl apply -f k8s/secrets.yaml

# 7. Deploy backend
helm install todo-backend charts/todo-backend/

# 8. Deploy frontend
helm install todo-frontend charts/todo-frontend/

# 9. Check deployment status
kubectl get pods
kubectl get services
kubectl get all

# 10. Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=120s
kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=120s

# 11. Get frontend URL
minikube service todo-frontend --url
```

## Health Check Commands
```powershell
# Backend health check (port-forward method)
kubectl port-forward deployment/todo-backend 8000:8000
# Then visit: http://localhost:8000/health

# Frontend health check
minikube service todo-frontend --url
# Open the URL in browser

# Check pod logs
kubectl logs -f deployment/todo-backend
kubectl logs -f deployment/todo-frontend

# Describe pods for detailed status
kubectl describe pod -l app=todo-backend
kubectl describe pod -l app=todo-frontend
```

## Cleanup Commands
```powershell
# Uninstall Helm releases
helm uninstall todo-backend
helm uninstall todo-frontend

# Delete secrets
kubectl delete secret todo-backend-secrets

# Stop Minikube
minikube stop

# Delete Minikube cluster (optional)
minikube delete
```

## Expected Results

### Successful Deployment
- Both pods in `Running` status within 1-2 minutes
- Backend health endpoint returns: `{"status": "healthy"}`
- Frontend loads in browser with login/register page
- No `ImagePullBackOff` or `CrashLoopBackOff` errors

### Helm Lint
- Backend: 0 failures (icon recommendation is optional)
- Frontend: 0 failures

### Service Access
- Frontend accessible via `minikube service todo-frontend --url`
- Backend accessible internally to frontend at `http://todo-backend:8000`
