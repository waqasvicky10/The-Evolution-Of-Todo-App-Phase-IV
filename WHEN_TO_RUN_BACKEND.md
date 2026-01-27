# 🔄 When to Run Backend

## ✅ Quick Answer

### For Phase III (Gradio App):
**NO backend needed!** The Gradio app is **standalone** and uses its own SQLite database.

### For Phase II (Next.js Frontend):
**YES, backend needed first!** The Next.js frontend connects to the FastAPI backend.

---

## 🎯 Phase III (Gradio App) - Standalone

### Run ONLY:
```powershell
cd E:\heckathon-2
python gradio_app.py
```

**No backend needed because:**
- ✅ Uses its own SQLite database (`todo.db`)
- ✅ Has its own Phase III agent
- ✅ Has its own MCP tools
- ✅ Completely independent

---

## 🎯 Phase II (Next.js + FastAPI) - Needs Backend

### Step 1: Start Backend FIRST
```powershell
cd E:\heckathon-2\backend
uvicorn app.main:app --reload
```

**Backend runs on:** http://localhost:8000

### Step 2: Then Start Frontend
```powershell
cd E:\heckathon-2\frontend
npm run dev
```

**Frontend runs on:** http://localhost:3000

---

## 📋 Summary

| Phase | App | Backend Needed? | Command |
|-------|-----|----------------|---------|
| **Phase III** | Gradio App | ❌ NO | `python gradio_app.py` |
| **Phase II** | Next.js Frontend | ✅ YES | Backend first, then frontend |

---

## 🚀 For Your Phase III Submission

**You only need:**
```powershell
cd E:\heckathon-2
python gradio_app.py
```

**That's it!** No backend, no frontend needed.

The Gradio app is completely standalone for Phase III.

---

## 💡 If You Want to Test Phase II Too

If you want to test the Next.js frontend (Phase II), then:

1. **Start Backend:**
   ```powershell
   cd E:\heckathon-2\backend
   uvicorn app.main:app --reload
   ```

2. **Start Frontend (in new terminal):**
   ```powershell
   cd E:\heckathon-2\frontend
   npm run dev
   ```

But for **Phase III submission**, you don't need this!
