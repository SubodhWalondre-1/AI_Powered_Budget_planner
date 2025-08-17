import smtplib
import time
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize sentiment analyzer
try:
    nltk.download('vader_lexicon', quiet=True)
    sia = SentimentIntensityAnalyzer()
except:
    print("NLTK initialization failed - sentiment analysis disabled")
    sia = None

# Global dictionaries and lists
need_d = {}
sorted_need_d = {}
want_d = {}
sorted_want_d = {}
financial_history = []
budget = 0

class AIConsultant:
    @staticmethod
    def analyze_spending_sentiment(description):
        """Use NLP to analyze emotional tone of spending descriptions"""
        if not sia:
            return "Sentiment analysis unavailable"
        sentiment = sia.polarity_scores(description)
        if sentiment['compound'] >= 0.05:
            return "Positive spending (likely good value)"
        elif sentiment['compound'] <= -0.05:
            return "Negative spending (potential waste)"
        else:
            return "Neutral spending"

    @staticmethod
    def predict_future_savings(history, months=3):
        """Predict future savings based on historical savings data"""
        savings_history = [h for h in history if h.get('type') == 'savings']
        
        if len(savings_history) < 2:
            return "Insufficient savings data for prediction (need 2+ months)"
        
        X = np.array(range(len(savings_history))).reshape(-1, 1)
        y = np.array([h['amount'] for h in savings_history])
        
        model = LinearRegression()
        model.fit(X, y)
        
        future = model.predict(np.array(range(len(savings_history), 
                                     len(savings_history)+months)).reshape(-1, 1))
        return [round(f, 2) for f in future]

    @staticmethod
    def detect_spending_patterns(history):
        """Identify spending patterns and categories"""
        patterns = {
            'needs': [],
            'wants': [],
            'savings': []
        }
        
        for item in history:
            if item.get('type') == 'need':
                patterns['needs'].append(item['amount'])
            elif item.get('type') == 'want':
                patterns['wants'].append(item['amount'])
            elif item.get('type') == 'savings':
                patterns['savings'].append(item['amount'])
        
        analysis = {}
        for category, amounts in patterns.items():
            if amounts:
                analysis[category] = {
                    'total': sum(amounts),
                    'average': sum(amounts)/len(amounts),
                    'count': len(amounts)
                }
        return analysis

    @staticmethod
    def optimize_savings_plan(income, expenses, goals):
        """AI-driven savings optimization"""
        disposable_income = income - sum(expenses.values())
        recommendations = []
        
        # Basic 50/30/20 rule recommendation
        needs_spending = income * 0.5
        wants_spending = income * 0.3
        savings_recommended = income * 0.2
        
        recommendations.append(f"Standard budget recommendation: Needs ₹{needs_spending:.2f}, Wants ₹{wants_spending:.2f}, Save ₹{savings_recommended:.2f}")
        
        # Personalized recommendation based on goals
        if 'emergency' in goals:
            recommendations.append("Boost emergency fund by reducing wants by 10%")
        if 'retirement' in goals:
            recommendations.append("Consider increasing retirement savings by 5% of income")
        
        return recommendations

def needs_wants(diff, sav):
    print("\n\n*****Please enter the list of your NEEDS*****")
    print("Describe each need and our AI will help analyze them.")
    size = int(input("\nEnter the number of needs you have: "))
    
    for i in range(1, size + 1):
        print(f"\nNeed {i}:")
        need = input("Description (e.g., 'rent for apartment'): ")
        price = float(input("Estimated cost: ₹"))
        
        # AI priority suggestion
        priority = int(input("Priority (1-10, 10=most important): "))
        need_d[priority] = [need, price, 'need']
        
        # Add to financial history
        financial_history.append({
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'type': 'need',
            'description': need,
            'amount': price,
            'priority': priority
        })
    
    print("\n\n*****Please enter the list of your WANTS*****")
    size = int(input("\nEnter the number of wants you have: "))
    
    for i in range(1, size + 1):
        print(f"\nWant {i}:")
        want = input("Description (e.g., 'dining out'): ")
        price = float(input("Estimated cost: ₹"))
        
        # AI priority suggestion
        priority = int(input("Priority (1-10, 10=most wanted): "))
        want_d[priority] = [want, price, 'want']
        
        # Add to financial history
        financial_history.append({
            'date': datetime.now().strftime("%Y-%m-%d"),
            'type': 'want',
            'description': want,
            'amount': price,
            'priority': priority
        })

def display_ai_insights():
    """Show AI-generated insights about spending"""
    print("\n\n=== AI FINANCIAL INSIGHTS ===")
    
    # Spending patterns
    patterns = AIConsultant.detect_spending_patterns(financial_history)
    print("\nSpending Patterns:")
    for category, data in patterns.items():
        print(f"{category.capitalize()}: {data['count']} items, Total: ₹{data['total']:.2f}, Avg: ₹{data['average']:.2f}")
    
    # Savings prediction
    predictions = AIConsultant.predict_future_savings(financial_history)
    print(f"\nSavings Projection (next 3 months): {predictions}")
    
    # Sentiment analysis
    if sia:
        print("\nSpending Emotional Analysis:")
        for item in financial_history[-5:]:
            if item['type'] in ['need', 'want']:
                analysis = AIConsultant.analyze_spending_sentiment(item['description'])
                print(f"{item['description'][:20]}...: {analysis}")

def visualization():
    """Generate visualizations of spending data"""
    if not financial_history:
        return
    
    # Prepare data
    categories = {
        'Needs': sum(item['amount'] for item in financial_history if item.get('type') == 'need'),
        'Wants': sum(item['amount'] for item in financial_history if item.get('type') == 'want'),
        'Savings': sum(item['amount'] for item in financial_history if item.get('type') == 'savings')
    }
    
    # Filter out zero categories
    categories = {k:v for k,v in categories.items() if v > 0}
    
    if not categories:
        return
    
    # Pie chart
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
    plt.title("Spending Distribution")
    
    # Priority vs Amount scatter
    plt.subplot(1, 2, 2)
    expenses = [item for item in financial_history if item.get('type') in ['need', 'want']]
    if expenses:
        priorities = [item['priority'] for item in expenses]
        amounts = [item['amount'] for item in expenses]
        plt.scatter(priorities, amounts)
        plt.xlabel('Priority')
        plt.ylabel('Amount (₹)')
        plt.title('Priority vs Spending Amount')
    
    plt.tight_layout()
    plt.savefig('budget_analysis.png')
    print("\nBudget visualization saved as 'budget_analysis.png'")

def calculation(diff, sav):
    spent = 0
    affordable_items = []
    
    print("\n\n=== BUDGET ALLOCATION RESULTS ===")
    print("\nPrioritized Needs:")
    for priority, (name, price, _) in sorted(sorted_need_d.items(), reverse=True):
        if diff - price >= 0:
            diff -= price
            spent += price
            affordable_items.append(name)
            print(f"✓ ₹{price:.2f} for {name} (Priority {priority})")
        else:
            print(f"✗ ₹{price:.2f} for {name} - exceeds remaining budget")
    
    print("\nPrioritized Wants:")
    for priority, (name, price, _) in sorted(sorted_want_d.items(), reverse=True):
        if diff - price >= 0:
            diff -= price
            spent += price
            affordable_items.append(name)
            print(f"✓ ₹{price:.2f} for {name} (Priority {priority})")
        else:
            print(f"✗ ₹{price:.2f} for {name} - exceeds remaining budget")
    
    # Record savings
    actual_savings = sav + diff
    financial_history.append({
        'date': datetime.now().strftime("%Y-%m-%d"),
        'type': 'savings',
        'description': 'Monthly savings deposit',
        'amount': actual_savings,
        'priority': 10
    })
    
    print("\n=== FINAL SUMMARY ===")
    print(f"Total Budget: ₹{budget:.2f}")
    print(f"Total Allocated: ₹{spent:.2f}")
    print(f"Planned Savings: ₹{sav:.2f}")
    print(f"Actual Savings: ₹{actual_savings:.2f} (₹{diff:.2f} remaining)")
    
    if input("\nWould you like to receive this plan by email? (y/n): ").lower() == 'y':
        send_email(affordable_items, spent, actual_savings)

def send_email(items, spent, savings):
    email = input("Enter your email address: ")
    
    # Create message
    subject = "Your AI-Generated Budget Plan"
    body = ("=== AI-POWERED BUDGET PLAN ===\n\n"
           f"Total Spending: ₹{spent:.2f}\n"
           f"Total Savings: ₹{savings:.2f}\n\n"
           "Prioritized Items to Purchase:\n")
    body += "\n".join(f"- {item}" for item in items)
    
    # Add AI recommendations
    body += "\n\nAI Recommendations:\n"
    patterns = AIConsultant.detect_spending_patterns(financial_history)
    for category, data in patterns.items():
        body += (f"- Your {category} spending totals ₹{data['total']:.2f} "
                f"with average ₹{data['average']:.2f} per item\n")
    
    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("budgetcalcpy@gmail.com", "zqprcutbzhlsbhzd")
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail("budgetcalcpy@gmail.com", email, message)
        server.quit()
        print("Budget plan sent to your email!")
    except Exception as e:
        print(f"Error sending email: {e}")

def start():
    global budget, sorted_need_d, sorted_want_d
    
    print("\n******** AI-Powered Monthly Budget Planner ********")
    print("This planner uses AI to analyze your spending patterns and optimize savings.\n")
    
    budget = float(input("Please enter your Monthly budget: ₹"))
    saving_goal = float(input("Monthly savings goal: ₹"))
    financial_goals = input("Financial goals (comma separated, e.g., emergency,vacation,retirement): ").lower().split(',')
    
    diff = budget - saving_goal
    
    if saving_goal > budget:
        saving_goal = budget * 0.2
        print(f"\nAdjusting savings goal to 20% of budget: ₹{saving_goal:.2f}")
        diff = budget - saving_goal
    
    needs_wants(diff, saving_goal)
    
    # Sort needs and wants by priority
    sorted_need_d = dict(sorted(need_d.items(), key=lambda item: item[0], reverse=True))
    sorted_want_d = dict(sorted(want_d.items(), key=lambda item: item[0], reverse=True))
    
    print("\nAI is analyzing your financial data...")
    time.sleep(1)
    
    display_ai_insights()
    
    # Generate savings optimization recommendations
    expenses = {**{k: v[1] for k, v in sorted_need_d.items()},
                **{k: v[1] for k, v in sorted_want_d.items()}}
    recommendations = AIConsultant.optimize_savings_plan(budget, expenses, financial_goals)
    print("\nAI Savings Recommendations:")
    for rec in recommendations:
        print(f"- {rec}")
    
    calculation(diff, saving_goal)
    visualization()

if __name__ == "__main__":
    start()