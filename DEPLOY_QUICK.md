# 🚀 QUICK DEPLOYMENT GUIDE - Hugging Face Spaces

## ⚡ 5-Minute Deployment

### 1️⃣ Push to GitHub
```bash
git add .
git commit -m "Ready for Hugging Face deployment"
git push origin main
```

### 2️⃣ Create Space
1. Go to: **https://huggingface.co/spaces**
2. Click: **"Create new Space"**
3. Fill in:
   - **Name:** `ai-excel-agent`
   - **SDK:** `Streamlit`
   - **Visibility:** `Public`
4. Click: **"Create Space"**

### 3️⃣ Import from GitHub
1. In your Space, click **"Files"** tab
2. Click **"Add file"** → **"Import from GitHub"**
3. Select your repo: `Ai_Excel_Agent`
4. Click: **"Import"**

### 4️⃣ Add API Key
1. Go to **"Settings"** tab
2. Scroll to **"Variables and secrets"**
3. Click **"New secret"**
4. Add:
   - **Name:** `OPENAI_API_KEY`
   - **Value:** Your OpenAI API key
5. Click: **"Save"**

### 5️⃣ Update Requirements
1. Go to **"Files"** tab
2. Click `requirements.txt` → Edit
3. Replace with content from `requirements_spaces.txt`
4. Click **"Commit changes"**

### 6️⃣ Wait & Test
1. Go to **"App"** tab
2. Wait 2-5 minutes for build
3. Test your live app!

---

## 🎯 Your Live URL
```
https://huggingface.co/spaces/YOUR_USERNAME/ai-excel-agent
```

---

## 📁 Files Created for Deployment

✅ `app.py` - Main entry point for Hugging Face
✅ `requirements_spaces.txt` - Optimized requirements
✅ `.gitattributes` - Git LFS configuration
✅ `.streamlit/secrets.toml` - Local testing template
✅ `HUGGINGFACE_DEPLOYMENT.md` - Detailed guide

---

## ❓ Need Help?

Read full guide: **`HUGGINGFACE_DEPLOYMENT.md`**

---

**Good luck! 🚀**
