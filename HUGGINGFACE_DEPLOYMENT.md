# 🚀 Deploy AI Excel Agent on Hugging Face Spaces - Complete Guide

## ✅ Prerequisites

- GitHub account
- Hugging Face account (free)
- OpenAI API Key (for AI features)

---

## 📋 Step-by-Step Deployment

### **Step 1: Commit and Push to GitHub**

Open terminal in your project folder and run:

```bash
cd D:\Ai_Excel_Agent
git add .
git commit -m "Add Hugging Face Spaces deployment files"
git push origin main
```

> **Note:** If you haven't set up git yet:
> ```bash
> git init
> git add .
> git commit -m "Initial commit"
> git branch -M main
> git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
> git push -u origin main
> ```

---

### **Step 2: Create Hugging Face Space**

1. **Go to:** https://huggingface.co/spaces
2. **Click:** "Create new Space" (top right)
3. **Fill in the details:**
   - **Space name:** `ai-excel-agent` (or your preferred name)
   - **License:** MIT
   - **SDK:** `Streamlit`
   - **Visibility:** Public (free) or Private
4. **Click:** "Create Space"

---

### **Step 3: Connect GitHub Repository**

After creating the Space:

1. **Click on:** "Files" tab in your new Space
2. **Click:** "Add file" → "Import from GitHub"
3. **Select your repository:** `Ai_Excel_Agent`
4. **Select branch:** `main`
5. **Click:** "Import"

> **Alternative Method - Manual Upload:**
> 1. Download your project as ZIP from GitHub
> 2. Extract files
> 3. Drag and drop all files to Hugging Face file uploader
> 4. Click "Commit changes to main"

---

### **Step 4: Add OpenAI API Key**

1. **Go to:** Your Space settings (click "Settings" tab)
2. **Scroll to:** "Variables and secrets"
3. **Click:** "New secret"
4. **Add:**
   - **Name:** `OPENAI_API_KEY`
   - **Value:** `sk-proj-xxxxxxxxxxxxxxxxxxxx` (your actual API key)
5. **Click:** "Save"

---

### **Step 5: Update Requirements (Important!)**

In your Space's "Files" tab:

1. **Click on:** `requirements.txt`
2. **Click:** "Edit"
3. **Replace content with:** `requirements_spaces.txt` content
4. **Click:** "Commit changes to main"

Or create a new file called `requirements.txt` with this content:

```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
python-multipart>=0.0.6
pydantic>=2.5.3
pandas>=2.2.0
openpyxl>=3.1.2
xlsxwriter>=3.1.9
langchain>=0.1.0
langchain-community>=0.0.10
langchain-core>=0.1.10
langchain-openai>=0.0.2
matplotlib>=3.8.2
plotly>=5.18.0
kaleido>=0.2.1
streamlit>=1.29.0
python-dotenv>=1.0.0
aiofiles>=23.2.1
```

---

### **Step 6: Configure the App**

1. **Go to:** "Files" tab
2. **Click on:** `app.py`
3. **Verify** it has this content:

```python
"""
AI Excel Agent - Single File App for Hugging Face Spaces
"""
import sys
from pathlib import Path

# Add backend and frontend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))
sys.path.insert(0, str(Path(__file__).parent / 'frontend'))

# Run the UI
exec(open('frontend/ui.py', encoding='utf-8').read())
```

4. **Click:** "Commit" if any changes made

---

### **Step 7: Set app.py as Entry Point**

1. **Go to:** Settings tab of your Space
2. **Find:** "App Configuration" or "Entry Point"
3. **Set:** `app.py` as the main file
4. **Save** changes

---

### **Step 8: Wait for Deployment**

1. **Go to:** "App" tab
2. **Wait 2-5 minutes** for:
   - Dependencies installation
   - Build process
   - App startup

You'll see:
- 🟡 Building (in progress)
- 🟢 Running (success!)
- 🔴 Error (check logs)

---

### **Step 9: Test Your Live App**

Once running, you'll see:

1. **Your app URL:** `https://huggingface.co/spaces/YOUR_USERNAME/ai-excel-agent`
2. **Test features:**
   - Upload Excel file
   - Enter API key (if not set as secret)
   - Ask questions
   - Generate charts

---

## 🔧 Troubleshooting

### **Issue: Build Failed**

**Solution:**
1. Click "Logs" tab
2. Check error message
3. Common fixes:
   - Update `requirements.txt`
   - Check file paths in `app.py`
   - Ensure all files uploaded

### **Issue: Module Not Found**

**Solution:**
Make sure `backend/` and `frontend/` folders are uploaded correctly with all files.

### **Issue: OpenAI API Error**

**Solution:**
1. Verify API key in Secrets
2. Check API key has credits
3. Test with small file first

### **Issue: File Upload Not Working**

**Solution:**
Hugging Face Spaces has storage limits. Files are temporary and deleted after session.

---

## 📊 Free Tier Limits

| Feature | Limit |
|---------|-------|
| **Storage** | 1GB |
| **CPU** | 2 vCPU |
| **RAM** | 16GB |
| **Monthly Hours** | Unlimited (with pauses) |
| **File Upload** | Up to 500MB |

> **Note:** Free spaces pause after 48 hours of inactivity. Just refresh to restart.

---

## 🎉 Success!

Your AI Excel Agent is now live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/ai-excel-agent
```

**Share it with the world!** 🚀

---

## 📝 Optional: Custom Domain

To add a custom domain:

1. Go to Space Settings
2. Scroll to "Custom Domain"
3. Add your domain
4. Configure DNS records

---

## 🔐 Security Best Practices

- ✅ Never commit API keys to GitHub
- ✅ Use Hugging Face Secrets for sensitive data
- ✅ Keep dependencies updated
- ✅ Monitor usage in Settings

---

## 📞 Support

- **Hugging Face Docs:** https://huggingface.co/docs/hub/spaces
- **Streamlit Docs:** https://docs.streamlit.io/
- **Your Project Issues:** GitHub repo issues tab

---

**Built with ❤️ by Syed Rafay**
