

from finance_app import FinanceApp

def main():
    """
    Fungsi utama untuk menjalankan Personal Finance App
    """
    try:
        print("🚀 Memulai Personal Finance Manager...")
        
        # Inisialisasi dan jalankan aplikasi
        app = FinanceApp()
        app.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Aplikasi dihentikan oleh user")
        print("💡 Terima kasih telah menggunakan Personal Finance Manager!")
    except Exception as e:
        print(f"\n❌ Terjadi error: {e}")
        print("🔧 Silakan restart aplikasi")
    finally:
        print("\n🏁 Program selesai")

if __name__ == "__main__":
    main()