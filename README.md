# 🧠 AI-Powered Monthly Budget Planner  

This is a Python-based **AI Budget Planner** that helps you:  
- Track **Needs, Wants, and Savings**  
- Get **AI-based insights** into spending patterns  
- Perform **Sentiment Analysis** on expense descriptions  
- Predict **future savings** using Machine Learning  
- Receive **budget visualization graphs**  
- Get **personalized AI recommendations** for financial goals  
- Optionally, send your budget plan to your email 📧  

---

## 📦 Requirements  

Before running this project, make sure you have installed the following dependencies:  

```bash
pip install matplotlib
pip install scikit-learn
pip install numpy
pip install nltk
```

### Additional setup:
- **NLTK Data**: This project uses the `vader_lexicon` for sentiment analysis. It will be downloaded automatically when you run the script.  
- **Email Feature**: The script uses Gmail’s SMTP. You need to:
  1. Enable **“App Passwords”** in your Gmail account.  
  2. Replace the `server.login("budgetcalcpy@gmail.com", "zqprcutbzhlsbhzd")` with your own Gmail and app password if you want to send budget reports by email.  

---

## ▶️ How to Run  

### **Option 1: Run from Command Prompt (CMD)**
1. Save the script as `budget_planner.py`.  
2. Open CMD in the folder where the file is saved.  
3. Run the script with:  
   ```bash
   python budget_planner.py
   ```

---

### **Option 2: Run from Visual Studio Code**
1. Open **Visual Studio Code**.  
2. Create a new project folder and place `budget_planner.py` inside.  
3. Make sure you have installed **Python extension** in VS Code.  
4. Open a terminal in VS Code (`Ctrl + ~`).  
5. Run:  
   ```bash
   python budget_planner.py
   ```

---

## 📊 Features  
- **AI Spending Analysis** → Detects positive, negative, or neutral spending patterns.  
- **Future Savings Prediction** → Predicts next 3 months using Linear Regression.  
- **Visualizations** → Generates `budget_analysis.png` with charts.   
- **Email Delivery** → Sends budget summary to your email.  

---

## ⚠️ Notes  
- Works with **Python 3.7+**  
- If email feature fails, check firewall or Gmail app password settings.  
- Recommended: Run in a **virtual environment** to avoid conflicts.  
