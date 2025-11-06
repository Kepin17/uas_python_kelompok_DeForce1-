"""
Account class untuk mengelola akun keuangan
"""
from datetime import datetime
from typing import List, Optional

class Transaction:
    """Class untuk merepresentasikan transaksi"""
    
    def __init__(self, amount: float, description: str, transaction_type: str, category: str = ""):
        self.id = id(self)  # Simple ID menggunakan object id
        self.amount = amount
        self.description = description
        self.transaction_type = transaction_type.lower()  # 'income' atau 'expense'
        self.category = category
        self.date = datetime.now()
        
    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d %H:%M')} - {self.transaction_type.capitalize()}: {self.description} - Rp {self.amount:,.0f}"
    
    def __repr__(self):
        return f"Transaction(amount={self.amount}, description='{self.description}', type='{self.transaction_type}')"

class Account:
    """Class untuk mengelola akun keuangan personal"""
    
    def __init__(self, owner_name: str, initial_balance: float = 0.0):
        self.owner_name = owner_name
        self.balance = initial_balance
        self.transactions: List[Transaction] = []
        self.created_date = datetime.now()
        
    def add_income(self, amount: float, description: str, category: str = "Income") -> bool:
        """Menambah pemasukan"""
        if amount <= 0:
            print("❌ Jumlah pemasukan harus lebih dari 0")
            return False
            
        transaction = Transaction(amount, description, "income", category)
        self.transactions.append(transaction)
        self.balance += amount
        print(f"✅ Pemasukan berhasil ditambahkan: Rp {amount:,.0f}")
        return True
    
    def add_expense(self, amount: float, description: str, category: str = "Expense") -> bool:
        """Menambah pengeluaran"""
        if amount <= 0:
            print("❌ Jumlah pengeluaran harus lebih dari 0")
            return False
            
        if amount > self.balance:
            print(f"❌ Saldo tidak mencukupi. Saldo saat ini: Rp {self.balance:,.0f}")
            return False
            
        transaction = Transaction(amount, description, "expense", category)
        self.transactions.append(transaction)
        self.balance -= amount
        print(f"✅ Pengeluaran berhasil dicatat: Rp {amount:,.0f}")
        return True
    
    def get_balance(self) -> float:
        """Mendapatkan saldo saat ini"""
        return self.balance
    
    def get_transaction_history(self, limit: Optional[int] = None) -> List[Transaction]:
        """Mendapatkan riwayat transaksi"""
        if limit:
            return self.transactions[-limit:]
        return self.transactions
    
    def get_monthly_summary(self, month: int, year: int) -> dict:
        """Mendapatkan ringkasan bulanan"""
        monthly_transactions = [
            t for t in self.transactions 
            if t.date.month == month and t.date.year == year
        ]
        
        total_income = sum(t.amount for t in monthly_transactions if t.transaction_type == "income")
        total_expense = sum(t.amount for t in monthly_transactions if t.transaction_type == "expense")
        
        return {
            "month": month,
            "year": year,
            "total_income": total_income,
            "total_expense": total_expense,
            "net_income": total_income - total_expense,
            "transaction_count": len(monthly_transactions)
        }
    
    def get_category_summary(self) -> dict:
        """Mendapatkan ringkasan per kategori"""
        category_summary = {}
        
        for transaction in self.transactions:
            category = transaction.category
            if category not in category_summary:
                category_summary[category] = {"income": 0, "expense": 0, "count": 0}
            
            if transaction.transaction_type == "income":
                category_summary[category]["income"] += transaction.amount
            else:
                category_summary[category]["expense"] += transaction.amount
            
            category_summary[category]["count"] += 1
        
        return category_summary
    
    def __str__(self):
        return f"Akun: {self.owner_name} | Saldo: Rp {self.balance:,.0f} | Transaksi: {len(self.transactions)}"