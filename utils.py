"""
Utilities untuk Personal Finance App
"""
import json
import os
from datetime import datetime
from typing import Dict, Any

class DataManager:
    """Class untuk mengelola penyimpanan dan loading data"""
    
    @staticmethod
    def save_to_file(data: Dict[Any, Any], filename: str = "finance_data.json") -> bool:
        """Simpan data ke file JSON"""
        try:
            # Convert datetime objects to string for JSON serialization
            json_data = DataManager._serialize_data(data)
            
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(json_data, file, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    @staticmethod
    def load_from_file(filename: str = "finance_data.json") -> Dict[Any, Any]:
        """Load data dari file JSON"""
        try:
            if not os.path.exists(filename):
                return {}
            
            with open(filename, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
            
            # Convert string dates back to datetime objects
            return DataManager._deserialize_data(json_data)
        
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return {}
    
    @staticmethod
    def _serialize_data(obj):
        """Convert datetime objects to strings for JSON"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {key: DataManager._serialize_data(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [DataManager._serialize_data(item) for item in obj]
        else:
            return obj
    
    @staticmethod
    def _deserialize_data(obj):
        """Convert ISO strings back to datetime objects"""
        if isinstance(obj, str):
            try:
                return datetime.fromisoformat(obj)
            except ValueError:
                return obj
        elif isinstance(obj, dict):
            return {key: DataManager._deserialize_data(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [DataManager._deserialize_data(item) for item in obj]
        else:
            return obj

class InputValidator:
    """Class untuk validasi input user"""
    
    @staticmethod
    def validate_amount(amount_str: str) -> tuple[bool, float]:
        """Validasi input jumlah uang"""
        try:
            amount = float(amount_str.replace(',', '').replace('.', ''))
            if amount < 0:
                return False, 0.0
            return True, amount
        except (ValueError, TypeError):
            return False, 0.0
    
    @staticmethod
    def validate_date(day: int, month: int, year: int) -> bool:
        """Validasi tanggal"""
        try:
            datetime(year, month, day)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_name(name: str) -> bool:
        """Validasi nama (tidak kosong dan tidak hanya whitespace)"""
        return bool(name and name.strip())

class Formatter:
    """Class untuk formatting output"""
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """Format angka menjadi format mata uang Rupiah"""
        return f"Rp {amount:,.0f}".replace(',', '.')
    
    @staticmethod
    def format_percentage(percentage: float, decimal_places: int = 1) -> str:
        """Format persentase"""
        return f"{percentage:.{decimal_places}f}%"
    
    @staticmethod
    def format_date(date: datetime, format_str: str = "%d/%m/%Y") -> str:
        """Format tanggal"""
        return date.strftime(format_str)
    
    @staticmethod
    def create_progress_bar(percentage: float, length: int = 20) -> str:
        """Buat progress bar ASCII"""
        filled = int(percentage / 100 * length)
        bar = "█" * filled + "░" * (length - filled)
        return f"[{bar}] {percentage:.1f}%"

class CategoryManager:
    """Class untuk mengelola kategori default"""
    
    DEFAULT_INCOME_CATEGORIES = [
        "Gaji", "Bonus", "Freelance", "Investasi", "Hadiah", "Lain-lain"
    ]
    
    DEFAULT_EXPENSE_CATEGORIES = [
        "Makanan & Minuman", "Transportasi", "Belanja", "Hiburan", 
        "Tagihan", "Kesehatan", "Pendidikan", "Investasi", "Tabungan",
        "Darurat", "Lain-lain"
    ]
    
    @classmethod
    def get_income_categories(cls) -> list[str]:
        """Mendapatkan daftar kategori pemasukan"""
        return cls.DEFAULT_INCOME_CATEGORIES.copy()
    
    @classmethod
    def get_expense_categories(cls) -> list[str]:
        """Mendapatkan daftar kategori pengeluaran"""
        return cls.DEFAULT_EXPENSE_CATEGORIES.copy()
    
    @classmethod
    def suggest_category(cls, description: str, transaction_type: str = "expense") -> str:
        """Suggest kategori berdasarkan deskripsi"""
        description_lower = description.lower()
        
        if transaction_type == "income":
            if any(word in description_lower for word in ["gaji", "salary", "upah"]):
                return "Gaji"
            elif any(word in description_lower for word in ["bonus", "tunjangan"]):
                return "Bonus"
            elif any(word in description_lower for word in ["freelance", "project", "kontrak"]):
                return "Freelance"
            else:
                return "Lain-lain"
        
        else:  # expense
            if any(word in description_lower for word in ["makan", "makanan", "minum", "restaurant", "cafe"]):
                return "Makanan & Minuman"
            elif any(word in description_lower for word in ["bensin", "ojek", "grab", "gojek", "parkir", "tol"]):
                return "Transportasi"
            elif any(word in description_lower for word in ["beli", "shopping", "belanja", "baju", "sepatu"]):
                return "Belanja"
            elif any(word in description_lower for word in ["listrik", "air", "internet", "pulsa", "tagihan"]):
                return "Tagihan"
            elif any(word in description_lower for word in ["obat", "dokter", "rumah sakit", "kesehatan"]):
                return "Kesehatan"
            elif any(word in description_lower for word in ["bioskop", "game", "hiburan", "karaoke"]):
                return "Hiburan"
            else:
                return "Lain-lain"