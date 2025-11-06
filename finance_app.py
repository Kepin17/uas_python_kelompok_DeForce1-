"""
Finance App - User Interface dan Controller
"""
import os
import json
from datetime import datetime, timedelta
from typing import Optional
from account import Account, Transaction

class FinanceApp:
    """Main application class untuk Personal Finance App"""
    
    def __init__(self):
        self.account: Optional[Account] = None
        self.is_running = True
        self.data_file = "finance_data.json"
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def save_data_to_json(self) -> bool:
        """Simpan data akun ke file JSON"""
        if not self.account:
            return False
        
        try:
            data = {
                "account": {
                    "owner_name": self.account.owner_name,
                    "balance": self.account.balance,
                    "created_date": self.account.created_date.isoformat(),
                    "transactions": []
                }
            }
            
            # Convert transactions to dictionary
            for transaction in self.account.transactions:
                transaction_data = {
                    "id": transaction.id,
                    "amount": transaction.amount,
                    "description": transaction.description,
                    "transaction_type": transaction.transaction_type,
                    "category": transaction.category,
                    "date": transaction.date.isoformat()
                }
                data["account"]["transactions"].append(transaction_data)
            
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    def load_data_from_json(self) -> bool:
        """Load data akun dari file JSON"""
        try:
            if not os.path.exists(self.data_file):
                return False
            
            with open(self.data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if "account" not in data:
                return False
            
            account_data = data["account"]
            
            # Create account
            self.account = Account(
                account_data["owner_name"],
                0  # Set initial balance to 0, will be calculated from transactions
            )
            
            # Set created date
            self.account.created_date = datetime.fromisoformat(account_data["created_date"])
            
            # Load transactions
            self.account.transactions = []
            balance = 0
            
            for trans_data in account_data["transactions"]:
                transaction = Transaction(
                    trans_data["amount"],
                    trans_data["description"],
                    trans_data["transaction_type"],
                    trans_data["category"]
                )
                transaction.id = trans_data["id"]
                transaction.date = datetime.fromisoformat(trans_data["date"])
                
                self.account.transactions.append(transaction)
                
                # Calculate balance
                if transaction.transaction_type == "income":
                    balance += transaction.amount
                else:
                    balance -= transaction.amount
            
            self.account.balance = balance
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def export_to_csv(self) -> bool:
        """Export transaksi ke file CSV"""
        if not self.account or not self.account.transactions:
            print("❌ Tidak ada data untuk di-export!")
            return False
        
        try:
            import csv
            filename = f"finance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Tanggal', 'Jenis', 'Kategori', 'Deskripsi', 'Jumlah', 'Saldo']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                
                running_balance = 0
                for transaction in self.account.transactions:
                    if transaction.transaction_type == "income":
                        running_balance += transaction.amount
                        amount_display = f"+{transaction.amount:,.0f}"
                    else:
                        running_balance -= transaction.amount
                        amount_display = f"-{transaction.amount:,.0f}"
                    
                    writer.writerow({
                        'Tanggal': transaction.date.strftime('%d/%m/%Y %H:%M'),
                        'Jenis': transaction.transaction_type.capitalize(),
                        'Kategori': transaction.category,
                        'Deskripsi': transaction.description,
                        'Jumlah': amount_display,
                        'Saldo': f"{running_balance:,.0f}"
                    })
            
            print(f"✅ Data berhasil di-export ke: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting to CSV: {e}")
            return False
    
    def display_header(self):
        """Menampilkan header aplikasi"""
        print("=" * 60)
        print("💰 PERSONAL FINANCE MANAGER 💰".center(60))
        print("=" * 60)
        if self.account:
            print(f"👤 {self.account.owner_name}")
            print(f"💳 Saldo: Rp {self.account.get_balance():,.0f}")
        print("=" * 60)
    
    def setup_account(self):
        """Setup akun baru atau login"""
        print("\n🏦 SETUP AKUN")
        print("-" * 20)
        
        # Check if data file exists
        if os.path.exists(self.data_file):
            print("📁 Data tersimpan ditemukan!")
            load_choice = input("🔄 Load data yang sudah ada? (y/n): ").lower()
            
            if load_choice == 'y':
                if self.load_data_from_json():
                    print(f"✅ Data berhasil dimuat untuk {self.account.owner_name}")
                    print(f"💳 Saldo: Rp {self.account.get_balance():,.0f}")
                    print(f"📝 Transaksi: {len(self.account.transactions)}")
                    input("\n📱 Tekan Enter untuk melanjutkan...")
                    return True
                else:
                    print("❌ Gagal memuat data. Membuat akun baru...")
        
        # Create new account
        name = input("👤 Masukkan nama Anda: ").strip()
        if not name:
            print("❌ Nama tidak boleh kosong!")
            return False
        
        try:
            initial_balance = float(input("💰 Saldo awal (Rp): ") or "0")
            if initial_balance < 0:
                print("❌ Saldo awal tidak boleh negatif!")
                return False
        except ValueError:
            print("❌ Saldo awal harus berupa angka!")
            return False
        
        self.account = Account(name, initial_balance)
        print(f"✅ Akun berhasil dibuat untuk {name}")
        
        # Auto-save new account
        if self.save_data_to_json():
            print("💾 Data akun tersimpan otomatis")
        
        input("\n📱 Tekan Enter untuk melanjutkan...")
        return True
    
    def display_main_menu(self):
        """Menampilkan menu utama"""
        print("\n📋 MENU UTAMA")
        print("-" * 20)
        print("1. 💵 Tambah Pemasukan")
        print("2. 💸 Tambah Pengeluaran") 
        print("3. 📊 Lihat Saldo & Riwayat")
        print("4. 📈 Laporan Keuangan")
        print("5. ⚙️  Pengaturan")
        print("0. 🚪 Keluar")
        print("-" * 20)
    
    def add_income(self):
        """Menu tambah pemasukan"""
        print("\n💵 TAMBAH PEMASUKAN")
        print("-" * 25)
        
        try:
            amount = float(input("💰 Jumlah (Rp): "))
            category = input("🏷️  Kategori (default: Income): ").strip() or "Income"
            
            # Gunakan kategori sebagai deskripsi
            description = f"Pemasukan - {category}"
            
            if self.account.add_income(amount, description, category):
                # Auto-save after successful transaction
                if self.save_data_to_json():
                    print("💾 Data tersimpan otomatis")
            
        except ValueError:
            print("❌ Jumlah harus berupa angka!")
        
        input("\n📱 Tekan Enter untuk kembali...")
    
    def add_expense(self):
        """Menu tambah pengeluaran"""
        print("\n💸 TAMBAH PENGELUARAN")
        print("-" * 25)
        
        # Suggest common categories
        print("💡 Kategori umum: Makanan, Transportasi, Belanja, Hiburan, Tagihan, Kesehatan")
        
        try:
            amount = float(input("💰 Jumlah (Rp): "))
            category = input("🏷️  Kategori (default: Expense): ").strip() or "Expense"
            
            # Gunakan kategori sebagai deskripsi
            description = f"Pengeluaran - {category}"
            
            if self.account.add_expense(amount, description, category):
                # Auto-save after successful transaction
                if self.save_data_to_json():
                    print("💾 Data tersimpan otomatis")
            
        except ValueError:
            print("❌ Jumlah harus berupa angka!")
        
        input("\n📱 Tekan Enter untuk kembali...")