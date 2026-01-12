# How to Deploy Phase III to Vercel

You can deploy the Phase III Digital App to Vercel for free!

## Prerequisite
Your code must be on GitHub (it is).

## Steps
1. **Login to Vercel**: Go to [vercel.com](https://vercel.com) and login with GitHub.
2. **Add New Project**: Click "Add New..." -> "Project".
3. **Import Repository**: Find `The-Evolution-Of-Todo-App` and click "Import".
4. **Configure Project**:
   - **Framework Preset**: Select "Other" (or let it autodect, likely "Other").
   - **Root Directory**: **Click Edit** and select `phase_iii`. This is CRITICAL.
5. **Envrionment Variables (Optional)**: None needed for the demo.
6. **Deploy**: Click "Deploy".

## Important Note on Database
Vercel Serverless Functions are ephemeral (read-only).
- The app uses `SQLite`.
- On Vercel, the database will be created in `/tmp`.
- **DATA WILL RESET** every time the server restarts (which happens frequently on Vercel).
- This is fine for a **Demo**, but for a real app, you should connect a persistent database like Supabase or Turso.

## Troubleshooting
If the backend fails:
- Check "Logs" in Vercel Dashboard.
- Ensure `Root Directory` was set to `phase_iii`.
