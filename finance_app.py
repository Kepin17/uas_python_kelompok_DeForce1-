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
    
    def view_balance_and_history(self):
        """Menu lihat saldo dan riwayat"""
        print(f"\n📊 SALDO & RIWAYAT")
        print("-" * 25)
        print(f"💳 Saldo Saat Ini: Rp {self.account.get_balance():,.0f}")
        print(f"📅 Akun dibuat: {self.account.created_date.strftime('%d/%m/%Y %H:%M')}")
        
        transactions = self.account.get_transaction_history()
        if not transactions:
            print("\n📝 Belum ada transaksi")
        else:
            print(f"\n📝 Riwayat Transaksi ({len(transactions)} transaksi):")
            print("-" * 60)
            
            # Show last 10 transactions
            recent_transactions = transactions[-10:]
            for transaction in reversed(recent_transactions):
                icon = "💵" if transaction.transaction_type == "income" else "💸"
                print(f"{icon} {transaction}")
            
            if len(transactions) > 10:
                print(f"\n... dan {len(transactions) - 10} transaksi lainnya")
        
        input("\n📱 Tekan Enter untuk kembali...")
    
    def financial_reports(self):
        """Menu laporan keuangan"""
        print("\n📈 LAPORAN KEUANGAN")
        print("-" * 25)
        
        current_date = datetime.now()
        
        # Monthly summary
        monthly_summary = self.account.get_monthly_summary(current_date.month, current_date.year)
        print(f"\n📅 Ringkasan Bulan {current_date.strftime('%B %Y')}:")
        print(f"   💵 Total Pemasukan: Rp {monthly_summary['total_income']:,.0f}")
        print(f"   💸 Total Pengeluaran: Rp {monthly_summary['total_expense']:,.0f}")
        print(f"   📊 Net Income: Rp {monthly_summary['net_income']:,.0f}")
        print(f"   🔢 Jumlah Transaksi: {monthly_summary['transaction_count']}")
        
        # Category summary
        category_summary = self.account.get_category_summary()
        if category_summary:
            print(f"\n🏷️  Ringkasan per Kategori:")
            for category, data in category_summary.items():
                net = data["income"] - data["expense"]
                print(f"   {category}: Net Rp {net:,.0f} ({data['count']} transaksi)")
        
        input("\n📱 Tekan Enter untuk kembali...")
    

    def settings_menu(self):
        """Menu pengaturan"""
        while True:
            print("\n⚙️  PENGATURAN")
            print("-" * 15)
            print("1. 👤 Ganti Nama")
            print("2. 💾 Export ke CSV")
            print("3. 📁 Simpan Data Manual")
            print("4. 🔄 Load Data")
            print("5. 📊 Info Data")
            print("6. 🔙 Kembali")
            
            choice = input("\n🔢 Pilih menu (1-6): ").strip()
            
            if choice == "1":
                new_name = input("👤 Nama baru: ").strip()
                if new_name:
                    old_name = self.account.owner_name
                    self.account.owner_name = new_name
                    
                    # Auto-save after name change
                    if self.save_data_to_json():
                        print(f"✅ Nama berhasil diubah dari '{old_name}' ke '{new_name}'")
                        print("💾 Data tersimpan otomatis")
                    else:
                        print(f"✅ Nama berhasil diubah dari '{old_name}' ke '{new_name}'")
                        print("⚠️ Gagal menyimpan perubahan")
                else:
                    print("❌ Nama tidak boleh kosong!")
                    
            elif choice == "2":
                print("\n💾 EXPORT DATA KE CSV")
                print("-" * 25)
                if self.export_to_csv():
                    print("📁 File CSV berisi semua transaksi dengan detail lengkap")
                
            elif choice == "3":
                print("\n📁 SIMPAN DATA MANUAL")
                print("-" * 25)
                if self.save_data_to_json():
                    print("✅ Data berhasil disimpan ke finance_data.json")
                else:
                    print("❌ Gagal menyimpan data")
                    
            elif choice == "4":
                print("\n🔄 LOAD DATA")
                print("-" * 15)
                confirm = input("⚠️ Load data akan mengganti data saat ini. Lanjutkan? (y/n): ").lower()
                if confirm == 'y':
                    if self.load_data_from_json():
                        print("✅ Data berhasil dimuat ulang")
                    else:
                        print("❌ Gagal memuat data atau file tidak ditemukan")
                        
            elif choice == "5":
                print("\n📊 INFO DATA")
                print("-" * 15)
                print(f"📁 File data: {self.data_file}")
                print(f"📄 Status file: {'Ada' if os.path.exists(self.data_file) else 'Tidak ada'}")
                if os.path.exists(self.data_file):
                    file_size = os.path.getsize(self.data_file)
                    print(f"📏 Ukuran file: {file_size} bytes")
                    mod_time = datetime.fromtimestamp(os.path.getmtime(self.data_file))
                    print(f"⏰ Terakhir diubah: {mod_time.strftime('%d/%m/%Y %H:%M:%S')}")
                
            elif choice == "6":
                break
            else:
                print("❌ Pilihan tidak valid!")
            
            input("\n📱 Tekan Enter untuk kembali...")
    
    def run(self):
        """Menjalankan aplikasi"""
        self.clear_screen()
        
        # Setup account first
        if not self.setup_account():
            return
        
        # Main loop
        while self.is_running:
            self.clear_screen()
            self.display_header()
            self.display_main_menu()
            
            choice = input("\n🔢 Pilih menu (0-5): ").strip()
            
            if choice == "1":
                self.add_income()
            elif choice == "2":
                self.add_expense()
            elif choice == "3":
                self.view_balance_and_history()
            elif choice == "4":
                self.financial_reports()
            elif choice == "5":
                self.settings_menu()
            elif choice == "0":
                # Final save before exit
                print("\n💾 Menyimpan data...")
                if self.save_data_to_json():
                    print("✅ Data tersimpan dengan aman")
                else:
                    print("⚠️ Gagal menyimpan data")
                
                print("\n👋 Terima kasih telah menggunakan Personal Finance Manager!")
                print("💡 Jangan lupa kelola keuangan dengan bijak!")
                self.is_running = False
            else:
                print("❌ Pilihan tidak valid!")
                input("📱 Tekan Enter untuk coba lagi...")