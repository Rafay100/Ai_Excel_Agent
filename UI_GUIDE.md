# UI Guide - AI Excel Agent

## 🎨 Modern Interface Overview

The AI Excel Agent features a **beautiful, modern UI** designed for optimal user experience and productivity.

---

## 🏠 Main Interface

### Header Section
```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║           📊 AI Excel Agent                              ║
║   Intelligent Data Analysis Powered by AI                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```
- **Gradient purple theme** with professional styling
- Clear branding and purpose statement

---

## 📋 Sidebar Features

### ⚙️ Settings Panel
- **🔑 API Key Input**: Secure password field for OpenAI API key
- Real-time validation and confirmation

### 📁 File Upload
- **Drag & Drop** zone with visual feedback
- Supported formats: `.xlsx`, `.xls`, `.xlsm`
- **📋 Load Sample Data**: One-click demo data loading

### ⚡ Quick Actions
```
┌─────────────────────────────────────┐
│  📊 Summary  │  🧹 Clean           │
├─────────────────────────────────────┤
│  📈 Chart    │  💾 Export          │
└─────────────────────────────────────┘
```
- Instant access to common operations
- Color-coded buttons with icons

---

## 📊 Data Overview (Metrics)

When data is loaded, **4 KPI cards** display:

| Metric | Description |
|--------|-------------|
| **Total Rows** | Count of all data rows |
| **Columns** | Number of columns |
| **Memory (MB)** | Dataset memory usage |
| **Duplicates** | Count of duplicate rows |

Cards have **hover animations** and gradient backgrounds.

---

## 💬 Chat Interface

### Main Tabs

#### 1. **Chat Tab** (Default)
```
┌──────────────────────────────────────────┐
│  💬 Ask Questions                        │
├──────────────────────────────────────────┤
│  ┌────────────────────────────────────┐  │
│  │ 👤 You: Show me total sales       │  │
│  └────────────────────────────────────┘  │
│  ┌────────────────────────────────────┐  │
│  │ 🤖 AI: The total sales are...     │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

**Features:**
- Color-coded messages (purple for user, white for AI)
- Message history persistence
- Real-time typing indicators
- Quick query suggestions

#### 2. **Data Tab**
Three sub-tabs:

**📋 Data View**
- Interactive dataframe display
- Sortable columns
- Download CSV button

**📊 Columns Info**
```
┌─────────────┬────────────┬──────────────┬────────────┐
│ Column Name │ Data Type  │ Non-Null     │ Null Count │
├─────────────┼────────────┼──────────────┼────────────┤
│ Product     │ object     │ 100          │ 0          │
│ Price       │ float64    │ 98           │ 2          │
└─────────────┴────────────┴──────────────┴────────────┘
```

**⚠️ Issues**
- Missing values warning with details
- Duplicate rows alert
- Data quality indicators

#### 3. **Charts Tab**
- Full-width chart display
- Interactive Plotly charts
- Chart builder controls

---

## ⚡ Quick Queries

Pre-built query buttons for common tasks:

```
┌────────────────┬─────────────────┬──────────────────┐
│ 📊 Data Summary│ 🔢 Statistics   │ 📈 Top Values    │
├────────────────┼─────────────────┼──────────────────┤
│ 🧹 Remove Dupes│ 📉 Null Check   │ 💾 Export        │
└────────────────┴─────────────────┴──────────────────┘
```

Each button:
- Executes immediately on click
- Shows results in chat
- Updates data if needed

---

## 📈 Chart Builder

### Visual Chart Creation

```
┌─────────────────────────┬─────────────────────────┐
│  Chart Type: [bar ▼]    │      Preview            │
│                         │                         │
│  X Axis: [Region ▼]     │   [Chart renders        │
│                         │    here on click]       │
│  Y Axis: [Sales ▼]      │                         │
│                         │                         │
│  Title: [My Chart]      │  🎨 Generate Chart      │
│                         │  [Close]                │
└─────────────────────────┴─────────────────────────┘
```

**Supported Chart Types:**
- Bar Chart
- Line Chart
- Pie Chart
- Scatter Plot
- Histogram
- Box Plot
- Area Chart

---

## 🧹 Data Cleaning

### Cleaning Options

```
┌─────────────────────────────────────────────┐
│  ☐ Remove rows with null values            │
│  ☐ Remove duplicate rows                   │
│  ☐ Fill null values                        │
│  ☐ Fix data types automatically            │
│                                             │
│  [✅ Apply Cleaning]  [Cancel]              │
└─────────────────────────────────────────────┘
```

**Results Display:**
- Success message with count of actions
- JSON details of operations performed
- Updated data summary

---

## 🎨 Design Elements

### Color Scheme
```
Primary Gradient: #667eea → #764ba2 (Purple)
Success: #28a745 (Green)
Warning: #ffc107 (Yellow)
Error: #dc3545 (Red)
Info: #17a2b8 (Cyan)
```

### Typography
- **Font**: Inter (Google Fonts)
- Headers: 700 weight
- Body: 400 weight
- Labels: 500 weight, uppercase

### Animations
- Hover lift effect on cards
- Smooth transitions (0.3s)
- Gradient backgrounds
- Box shadows with depth

### Responsive Layout
- Wide layout for desktop
- Collapsible sidebar
- Mobile-friendly tabs
- Adaptive chart sizing

---

## 📱 Dashboard Page

Access via: `frontend/dashboard.py`

### KPI Row
5 metric cards in a row showing:
1. Total Rows
2. Columns
3. Duplicates
4. Missing Values
5. Memory (MB)

### Analytics Charts
- **Distribution Overview**: Histogram
- **Correlation Heatmap**: Feature correlations
- **Box Plot Analysis**: Statistical distribution
- **Data Quality**: Stacked bar chart

---

## 🚀 Usage Tips

### Best Practices

1. **Start with Sample Data**
   - Click "Load Sample Data" to explore features
   - No file upload needed for testing

2. **Use Quick Queries First**
   - Get instant results without typing
   - Learn query patterns

3. **Check Data Tab**
   - Review column info before analysis
   - Check for data quality issues

4. **Build Charts Visually**
   - Use Chart Builder for custom visualizations
   - Preview before finalizing

5. **Export Results**
   - Download cleaned data
   - Share charts and insights

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Focus Chat Input | Click in chat box |
| Send Message | Enter key |
| Upload File | Drag & drop |

---

## 🔧 Customization

### Modify Theme Colors

Edit `frontend/ui.py`, find the CSS section:

```css
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

Change hex codes to your brand colors.

### Add Custom Metrics

In `render_metrics()` function:

```python
with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{custom_value}</div>
        <div class="metric-label">Your Label</div>
    </div>
    """, unsafe_allow_html=True)
```

### Extend Quick Queries

Add to `render_quick_queries()`:

```python
("🎯 Your Query", "Your natural language query")
```

---

## 📸 UI Components Reference

### Message Styles

**User Message:**
- Purple gradient background
- White text
- Rounded corners (asymmetric)
- Shadow with purple tint

**AI Message:**
- White background
- Dark text
- Left border accent
- Subtle shadow

### Button Styles

**Primary Button:**
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
color: white;
box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
```

**Hover State:**
```css
transform: translateY(-2px);
box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
```

---

## 🎯 User Flow

```
1. Upload File → 2. View Summary → 3. Ask Questions
                                              ↓
5. Export Results ← 4. Create Charts ← 3. Ask Questions
```

### Step-by-Step

1. **Upload**: Drag file or use sample data
2. **Review**: Check metrics and data preview
3. **Analyze**: Chat with AI or use quick queries
4. **Visualize**: Build charts in Charts tab
5. **Export**: Download results as CSV/Excel

---

## 💡 Pro Tips

1. **Tab Navigation**: Use tabs to organize workflow
2. **Chat History**: Scroll up to see previous Q&A
3. **Data Quality**: Check Issues tab first
4. **Chart Reuse**: Generated charts persist in session
5. **Clean First**: Run data cleaning before analysis

---

## 🆘 Troubleshooting

### UI Not Loading
- Clear browser cache
- Check Streamlit version: `pip show streamlit`
- Restart Streamlit server

### Charts Not Displaying
- Ensure plotly is installed: `pip install plotly`
- Check browser console for errors
- Try different chart type

### Chat Not Responding
- Verify API key is set
- Check internet connection
- Review chat history for errors

---

**Enjoy the beautiful, powerful UI! 🎨**
