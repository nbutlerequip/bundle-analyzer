# 🌐 Bundle Analyzer Web App - Complete Guide

## 📋 What You Got

A **full web application** for supersession-enhanced bundle analysis!

Users access it through a browser - no software installation needed (except for the server).

---

## 🚀 Quick Start (Run Locally)

### Option 1: Double-Click Launch (Easiest)

1. **Download all files:**
   - `webapp_bundle_analyzer.py`
   - `START_WEBAPP.bat`
   - `requirements.txt`

2. **Put them in a folder:**
   ```
   C:\BundleWebApp\
   ├── webapp_bundle_analyzer.py
   ├── START_WEBAPP.bat
   └── requirements.txt
   ```

3. **Double-click:** `START_WEBAPP.bat`

4. **Browser opens automatically** to: `http://localhost:8501`

5. **Upload your Excel files** or put them in `data/` folder

That's it! ✅

---

### Option 2: Command Line

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run webapp_bundle_analyzer.py
```

Then open: `http://localhost:8501`

---

## 👥 Multi-User Access

### Local Network (Same Office)

**Run on ONE computer, everyone accesses it:**

1. Run the app on a computer that stays on (your PC or a server)

2. Find your computer's IP address:
   ```
   ipconfig
   ```
   Look for: `192.168.x.x`

3. Tell users to go to:
   ```
   http://192.168.x.x:8501
   ```

4. Everyone in your office can now access it!

**Pros:**
- ✅ One installation
- ✅ Everyone uses same data
- ✅ Easy to maintain

**Cons:**
- ❌ Computer must stay on
- ❌ Only works on local network

---

## ☁️ Deploy to Cloud (Internet Access)

### Option A: Streamlit Community Cloud (FREE!)

**Perfect for:** Up to 50 users, free forever

**Steps:**

1. **Create GitHub Account** (free)
   - Go to github.com
   - Sign up

2. **Upload Your Files to GitHub:**
   - Create new repository (public)
   - Upload these files:
     - `webapp_bundle_analyzer.py`
     - `requirements.txt`
     - (Don't upload your Excel data files publicly!)

3. **Deploy on Streamlit Cloud:**
   - Go to share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Click "Deploy"

4. **Get Your URL:**
   ```
   https://yourapp.streamlit.app
   ```

5. **Share this URL** with your team!

**Data Handling:**
- Users upload their own Excel files
- OR you can use Streamlit secrets for permanent data

**Cost:** FREE
**Time to deploy:** 10 minutes

---

### Option B: Company Server / Azure / AWS

**Perfect for:** Enterprise, sensitive data, 100+ users

**Deploy on Windows Server:**

```bash
# On the server
git clone your-repo
cd bundle-analyzer
pip install -r requirements.txt

# Run in background
streamlit run webapp_bundle_analyzer.py --server.port 80
```

**Access at:** `http://yourserver.com`

**Or use:**
- **Azure Web Apps** ($10-50/month)
- **AWS EC2** ($10-50/month)
- **Heroku** ($7/month)

---

## 📊 How to Use the Web App

### Main Features:

**1. Upload Files**
```
Sidebar → "Upload Files"
→ Upload supersession Excel files
→ Upload bundle analysis file
→ Click "Run Analysis"
```

**2. View Statistics**
- Total bundles analyzed
- % with supersession history
- Average confidence boost
- Revenue potential

**3. Filter Results**
- Minimum confidence threshold
- With/without history
- Actionable vs not actionable
- Search by part number

**4. Explore Top 50**
- See detailed cards for top 10
- Full table for top 50
- Sort and filter

**5. Download Results**
- Excel file with 3 sheets
- Summary, Top 50, All Results
- Click "Download Excel File"

---

## 🔧 Advanced Configuration

### Use Existing Data Files

Instead of uploading every time:

1. Create `data/` folder next to the .py file:
   ```
   BundleWebApp/
   ├── webapp_bundle_analyzer.py
   ├── START_WEBAPP.bat
   └── data/
       ├── Supercedes_1.xlsx
       ├── Supercedes_2.xlsx
       └── Bundle_Analysis.xlsx
   ```

2. In the app, select **"Use Existing Files"**

3. Click "Run Analysis"

**Benefit:** Data stays on server, users don't need to upload

---

### Customize Appearance

Edit `webapp_bundle_analyzer.py`:

**Change colors:**
```python
# Line ~30 - Change the blue gradient
background: linear-gradient(135deg, #YOUR_COLOR 0%, #YOUR_COLOR 100%);
```

**Change company name:**
```python
# Line ~50 - Update company name
<p style="font-size: 0.8rem;">Your Company Name | v2.0</p>
```

**Change logo:**
Add your logo image and update line ~48

---

## 🔒 Security & Authentication

### Add Password Protection

For Streamlit Cloud or server deployment:

```python
# Add at top of webapp_bundle_analyzer.py
import streamlit as st

def check_password():
    def password_entered():
        if st.session_state["password"] == "your_password_here":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if not check_password():
    st.stop()

# Rest of your app code...
```

---

## 📱 Mobile Access

The web app is **mobile-responsive**!

Users can access from:
- ✅ Desktop computers
- ✅ Laptops
- ✅ Tablets
- ✅ Phones (with limitations on large tables)

Same URL works on all devices!

---

## ⚡ Performance Tips

### For Large Data Files:

1. **Use existing files** (don't upload every time)
2. **Pre-filter data** before analysis
3. **Increase memory** if needed:
   ```bash
   streamlit run webapp_bundle_analyzer.py --server.maxUploadSize 500
   ```

### For Many Users:

1. Deploy on **cloud with auto-scaling**
2. Use **caching** (already implemented)
3. Consider **database** instead of Excel files

---

## 🔄 Updating the App

### If Running Locally:

1. Stop the app (Ctrl+C)
2. Replace `webapp_bundle_analyzer.py` with new version
3. Restart with `START_WEBAPP.bat`

### If Deployed on Cloud:

1. Update file on GitHub
2. Streamlit Cloud auto-updates
3. Done!

---

## 🆚 Comparison: Local vs Cloud

| Feature | Local (Your PC) | Network (Office Server) | Cloud (Internet) |
|---------|----------------|------------------------|------------------|
| **Setup Time** | 5 min | 15 min | 10 min |
| **Cost** | Free | Free | Free-$50/mo |
| **Users** | Just you | Office only | Unlimited |
| **Access** | Your PC only | Local network | Anywhere |
| **Uptime** | When PC on | When server on | 24/7 |
| **Security** | Very secure | Secure | Need to add |
| **Data** | On your PC | On server | Upload or cloud |

---

## 📞 Troubleshooting

### "Port 8501 already in use"

**Solution:**
```bash
streamlit run webapp_bundle_analyzer.py --server.port 8502
```
Then use: `http://localhost:8502`

### "Module not found: streamlit"

**Solution:**
```bash
pip install streamlit pandas openpyxl
```

### Can't access from other computers

**Solution:**
```bash
streamlit run webapp_bundle_analyzer.py --server.address 0.0.0.0
```

### App is slow

**Solutions:**
- Use smaller Excel files
- Put data files in `data/` folder (don't upload)
- Deploy on faster server

---

## 🎯 Recommended Setup by Team Size

**1-5 users:** Run locally, share screen when needed

**5-20 users:** Run on office network server

**20-50 users:** Deploy to Streamlit Cloud (free)

**50+ users:** Deploy to company cloud (Azure/AWS)

---

## 📚 Next Steps

1. **Try it locally** - Double-click `START_WEBAPP.bat`
2. **Test with your team** - Share local network URL
3. **Deploy to cloud** - If everyone loves it
4. **Add features** - Let me know what you need!

---

## ✨ What's Included

**Built-in features:**
- ✅ File upload (drag & drop)
- ✅ Interactive filtering
- ✅ Search functionality
- ✅ Excel download
- ✅ Responsive design
- ✅ Progress indicators
- ✅ Error handling
- ✅ Mobile support

**What you can add:**
- Authentication/passwords
- Database integration
- Email reports
- Scheduled auto-runs
- API endpoints
- Custom branding

---

**Questions? Want help deploying? Let me know!** 🚀
