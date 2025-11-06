"""
Budget Manager untuk mengelola anggaran dan target keuangan
"""
from datetime import datetime
from typing import Dict, List
from account import Account

class Budget:
    """Class untuk mengelola budget per kategori"""
    
    def __init__(self, category: str, monthly_limit: float):
        self.category = category
        self.monthly_limit = monthly_limit
        self.created_date = datetime.now()
        
    def check_usage(self, account: Account, month: int, year: int) -> dict:
        """Cek penggunaan budget untuk bulan tertentu"""
        monthly_expenses = [
            t for t in account.transactions 
            if (t.transaction_type == "expense" and 
                t.category == self.category and
                t.date.month == month and 
                t.date.year == year)
        ]
        
        total_spent = sum(t.amount for t in monthly_expenses)
        remaining = self.monthly_limit - total_spent
        usage_percentage = (total_spent / self.monthly_limit) * 100 if self.monthly_limit > 0 else 0
        
        return {
            "category": self.category,
            "limit": self.monthly_limit,
            "spent": total_spent,
            "remaining": remaining,
            "usage_percentage": usage_percentage,
            "is_over_budget": total_spent > self.monthly_limit
        }
    
    def __str__(self):
        return f"Budget {self.category}: Rp {self.monthly_limit:,.0f}/bulan"

class FinancialGoal:
    """Class untuk target keuangan jangka panjang"""
    
    def __init__(self, name: str, target_amount: float, target_date: datetime):
        self.name = name
        self.target_amount = target_amount
        self.target_date = target_date
        self.saved_amount = 0.0
        self.created_date = datetime.now()
        
    def add_savings(self, amount: float) -> bool:
        """Menambah tabungan untuk goal ini"""
        if amount <= 0:
            return False
        
        self.saved_amount += amount
        return True
    
    def get_progress(self) -> dict:
        """Mendapatkan progress goal"""
        progress_percentage = (self.saved_amount / self.target_amount) * 100 if self.target_amount > 0 else 0
        remaining_amount = self.target_amount - self.saved_amount
        days_remaining = (self.target_date - datetime.now()).days
        
        daily_savings_needed = remaining_amount / max(days_remaining, 1) if days_remaining > 0 else 0
        
        return {
            "name": self.name,
            "target_amount": self.target_amount,
            "saved_amount": self.saved_amount,
            "remaining_amount": remaining_amount,
            "progress_percentage": progress_percentage,
            "days_remaining": max(days_remaining, 0),
            "daily_savings_needed": daily_savings_needed,
            "is_achieved": self.saved_amount >= self.target_amount
        }
    
    def __str__(self):
        progress = self.get_progress()
        return f"Goal: {self.name} - {progress['progress_percentage']:.1f}% (Rp {self.saved_amount:,.0f}/{self.target_amount:,.0f})"

class BudgetManager:
    """Class untuk mengelola budget dan financial goals"""
    
    def __init__(self):
        self.budgets: Dict[str, Budget] = {}
        self.financial_goals: List[FinancialGoal] = []
    
    def add_budget(self, category: str, monthly_limit: float) -> bool:
        """Menambah budget untuk kategori"""
        if monthly_limit <= 0:
            print("❌ Limit budget harus lebih dari 0")
            return False
        
        self.budgets[category] = Budget(category, monthly_limit)
        print(f"✅ Budget untuk '{category}' berhasil ditambahkan: Rp {monthly_limit:,.0f}/bulan")
        return True
    
    def add_financial_goal(self, name: str, target_amount: float, target_date: datetime) -> bool:
        """Menambah financial goal"""
        if target_amount <= 0:
            print("❌ Target amount harus lebih dari 0")
            return False
        
        if target_date <= datetime.now():
            print("❌ Target date harus di masa depan")
            return False
        
        goal = FinancialGoal(name, target_amount, target_date)
        self.financial_goals.append(goal)
        print(f"✅ Financial goal '{name}' berhasil ditambahkan")
        return True
    
    def check_all_budgets(self, account: Account, month: int, year: int) -> List[dict]:
        """Cek semua budget untuk bulan tertentu"""
        budget_status = []
        
        for budget in self.budgets.values():
            status = budget.check_usage(account, month, year)
            budget_status.append(status)
        
        return budget_status
    
    def get_budget_alerts(self, account: Account, month: int, year: int) -> List[str]:
        """Mendapatkan alert untuk budget yang hampir habis atau over"""
        alerts = []
        budget_status = self.check_all_budgets(account, month, year)
        
        for status in budget_status:
            if status["is_over_budget"]:
                alerts.append(f"🚨 OVER BUDGET: {status['category']} - Lebih Rp {abs(status['remaining']):,.0f}")
            elif status["usage_percentage"] >= 80:
                alerts.append(f"⚠️ WARNING: {status['category']} - {status['usage_percentage']:.1f}% terpakai")
        
        return alerts
    
    def save_for_goal(self, goal_name: str, amount: float, account: Account, description: str = "") -> bool:
        """Menyimpan uang untuk financial goal tertentu"""
        goal = next((g for g in self.financial_goals if g.name == goal_name), None)
        
        if not goal:
            print(f"❌ Financial goal '{goal_name}' tidak ditemukan")
            return False
        
        # Catat sebagai expense dari akun utama
        expense_description = description or f"Tabungan untuk {goal_name}"
        if account.add_expense(amount, expense_description, "Savings"):
            goal.add_savings(amount)
            print(f"✅ Berhasil menabung Rp {amount:,.0f} untuk goal '{goal_name}'")
            return True
        
        return False
    
    def get_all_goals_progress(self) -> List[dict]:
        """Mendapatkan progress semua financial goals"""
        return [goal.get_progress() for goal in self.financial_goals]