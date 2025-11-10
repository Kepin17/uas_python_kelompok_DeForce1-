import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from typing import Optional
from account import Account, Transaction

# Configuration
st.set_page_config(
    page_title="Personal Finance Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for blue and white theme with better contrast
st.markdown("""
<style>
    /* Main theme colors - Clean White & Blue */
    .stApp {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%);
        color: #1e40af;
    }
    
    /* Main content container - Clean white with subtle shadow */
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(30, 64, 175, 0.08);
        border: 1px solid rgba(59, 130, 246, 0.1);
        color: #1e40af;
    }
    
    /* Sidebar styling - Elegant blue gradient */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
        color: white;
        box-shadow: 4px 0 20px rgba(30, 64, 175, 0.15);
    }
    
    /* Header styling - Premium blue gradient */
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 40px rgba(30, 64, 175, 0.25);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Card styling - Clean white with blue accents */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #fefeff 50%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(30, 64, 175, 0.12);
        border: 2px solid rgba(59, 130, 246, 0.2);
        border-left: 6px solid #3b82f6;
        margin-bottom: 1.5rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 50px rgba(30, 64, 175, 0.2);
        border-color: rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 50%, #e0f2fe 100%);
    }
    
    /* Button styling - Premium blue with white text */
    .stButton > button {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 0.8rem 1.5rem;
        font-weight: 700;
        font-size: 14px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(30, 64, 175, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #3b82f6 100%);
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 12px 40px rgba(30, 64, 175, 0.5);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    /* Form styling - Clean white with blue accents */
    .stNumberInput > div > div > input {
        border: 2px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        background: linear-gradient(135deg, #ffffff 0%, #fefeff 100%) !important;
        color: #1e40af !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 12px 16px !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.08) !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15), 0 8px 25px rgba(59, 130, 246, 0.15) !important;
        outline: none !important;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%) !important;
        color: #1d4ed8 !important;
        transform: translateY(-2px) !important;
    }
    
    .stNumberInput > div > div > input::placeholder {
        color: rgba(30, 64, 175, 0.6) !important;
    }
    
    .stTextInput > div > div > input {
        border: 2px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        background: linear-gradient(135deg, #ffffff 0%, #fefeff 100%) !important;
        color: #1e40af !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 12px 16px !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.08) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15), 0 8px 25px rgba(59, 130, 246, 0.15) !important;
        outline: none !important;
        background-color: #f0f9ff !important;
        color: #1d4ed8 !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
    }
    
    /* Select box styling with better contrast */
    .stSelectbox > div > div {
        background-color: white !important;
        color: #1e40af !important;
        border: 2px solid #cbd5e1;
        border-radius: 8px;
    }
    
    .stSelectbox > div > div > div {
        background-color: white !important;
        color: #1e40af !important;
        border: none;
    }
    
    .stSelectbox > div > div > div:focus-within {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Selectbox dropdown options with better contrast */
    .stSelectbox [role="listbox"] {
        background-color: white !important;
        border: 2px solid #cbd5e1;
        border-radius: 8px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    }
    
    .stSelectbox [role="option"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        color: #1e40af !important;
        padding: 14px 18px !important;
        border: none !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        border-bottom: 1px solid #e0e7ff !important;
        transition: all 0.2s ease !important;
    }
    
    .stSelectbox [role="option"]:hover {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        color: #1d4ed8 !important;
        font-weight: 600 !important;
        transform: translateX(4px) !important;
    }
    
    .stSelectbox [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Selectbox main display with vibrant colors */
    .stSelectbox > div > div > div[data-baseweb="select"] {
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%) !important;
        color: #1e40af !important;
        border: 2px solid #93c5fd !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 6px 12px !important;
        box-shadow: 0 2px 6px rgba(59, 130, 246, 0.15) !important;
    }
    
    .stSelectbox > div > div > div[data-baseweb="select"]:hover {
        border-color: #3b82f6 !important;
        background: linear-gradient(135deg, #f0f9ff 0%, #dbeafe 100%) !important;
        color: #1d4ed8 !important;
        transform: translateY(-1px) !important;
    }
    
    .stSelectbox > div > div > div[data-baseweb="select"] > div {
        color: #1e40af !important;
        font-weight: 600 !important;
        background-color: transparent !important;
    }
    
    /* Selectbox input container */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        border-radius: 10px !important;
    }
    
    /* Form labels with vibrant colors */
    .stNumberInput > label,
    .stTextInput > label,
    .stSelectbox > label {
        color: #1e40af !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        margin-bottom: 6px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        text-shadow: 0 1px 2px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Message styling with better contrast */
    .stSuccess {
        background-color: #ecfdf5 !important;
        border: 2px solid #10b981 !important;
        color: #065f46 !important;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .stError {
        background-color: #fef2f2 !important;
        border: 2px solid #ef4444 !important;
        color: #991b1b !important;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .stInfo {
        background-color: #eff6ff !important;
        border: 2px solid #3b82f6 !important;
        color: #1e40af !important;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .stWarning {
        background-color: #fffbeb !important;
        border: 2px solid #f59e0b !important;
        color: #92400e !important;
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Tab styling with better contrast */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white !important;
        border-radius: 10px;
        border: 2px solid #cbd5e1;
        padding: 12px 20px;
        color: #475569 !important;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f1f5f9 !important;
        border-color: #3b82f6;
        color: #1e40af !important;
        transform: translateY(-1px);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white !important;
        border-color: #3b82f6;
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
    }
    
    /* Text contrast improvements - vibrant blue text */
    .stMarkdown, .stText, p, div, span {
        color: #1e40af !important;
        font-weight: 500 !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
    }
    
    /* Form labels */
    label {
        color: #374151 !important;
        font-weight: 600 !important;
    }
    
    /* Subheader styling */
    .stSubheader {
        color: #1e40af !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar content text */
    .css-1d391kg .stMarkdown {
        color: white !important;
    }
    
    /* Metric styling */
    .metric-container {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* Chart background */
    .js-plotly-plot .plotly .modebar {
        background-color: white !important;
    }
    
    /* Form container */
    .stForm {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Custom text colors - vibrant blue headings */
    h1, h2, h3, h4, h5, h6 {
        color: #1e40af !important;
        font-weight: 700 !important;
        text-shadow: 0 1px 3px rgba(30, 64, 175, 0.1) !important;
    }
    
    /* Table styling with vibrant blue theme */
    .stDataFrame {
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%) !important;
        border: 2px solid #93c5fd !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15) !important;
    }
    
    .stDataFrame table {
        background-color: transparent !important;
        width: 100% !important;
    }
    
    .stDataFrame thead th {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        color: #1e40af !important;
        font-weight: 800 !important;
        padding: 15px 18px !important;
        border-bottom: 3px solid #3b82f6 !important;
        text-align: left !important;
        font-size: 15px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stDataFrame tbody td {
        color: #1e40af !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
        padding: 12px 18px !important;
        border-bottom: 1px solid #e0e7ff !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .stDataFrame tbody tr:hover {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2) !important;
    }
    
    .stDataFrame tbody tr:hover td {
        color: #1d4ed8 !important;
        background-color: transparent !important;
        font-weight: 600 !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        color: #374151 !important;
        font-weight: 500 !important;
    }
    
    /* Form submit button styling */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-size: 14px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    
    .stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #047857 0%, #059669 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #6d28d9 0%, #7c3aed 100%) !important;
        transform: translateY(-1px);
    }
    
    /* Additional selectbox styling with vibrant theme */
    .stSelectbox div[role="combobox"] {
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%) !important;
        color: #1e40af !important;
        border: 2px solid #93c5fd !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1) !important;
    }
    
    .stSelectbox div[role="combobox"]:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2) !important;
        background: linear-gradient(135deg, #f0f9ff 0%, #dbeafe 100%) !important;
        color: #1d4ed8 !important;
    }
    
    /* Selectbox text visibility with blue colors */
    .stSelectbox [data-baseweb="select"] span {
        color: #1e40af !important;
        font-weight: 600 !important;
        background-color: transparent !important;
    }
    
    .stSelectbox [data-baseweb="select"] div {
        color: #1e40af !important;
        background-color: transparent !important;
    }
    
    /* Dropdown arrow with blue color */
    .stSelectbox [data-baseweb="select"] svg {
        fill: #3b82f6 !important;
        transition: transform 0.2s ease !important;
    }
    
    .stSelectbox [data-baseweb="select"]:hover svg {
        transform: rotate(180deg) !important;
    }
    
    /* Selectbox wrapper */
    .stSelectbox > div > div > div {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        color: #1e40af !important;
    }
    
    /* Selectbox input field when expanded */
    .stSelectbox [role="textbox"] {
        background-color: transparent !important;
        color: #1e40af !important;
        border: none !important;
        font-weight: 600 !important;
    }
    
    /* Plotly chart container styling */
    .js-plotly-plot {
        background-color: white !important;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        padding: 10px;
    }
    
    /* Plotly modebar (toolbar) styling */
    .modebar {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 4px;
        border: 1px solid #e5e7eb;
    }
    
    .modebar-btn {
        color: #374151 !important;
    }
    
    .modebar-btn:hover {
        background-color: #f3f4f6 !important;
        color: #1e40af !important;
    }
    
    /* Enhanced dataframe styling with vibrant theme */
    [data-testid="stDataFrame"] {
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%) !important;
        border: 2px solid #93c5fd !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.15) !important;
    }
    
    [data-testid="stDataFrame"] table {
        background-color: transparent !important;
        color: #1e40af !important;
    }
    
    [data-testid="stDataFrame"] th {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        color: #1e40af !important;
        font-weight: 800 !important;
        border-bottom: 3px solid #3b82f6 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    [data-testid="stDataFrame"] td {
        color: #1e40af !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-bottom: 1px solid #e0e7ff !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stDataFrame"] tr:hover td {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%) !important;
        color: #1d4ed8 !important;
        font-weight: 600 !important;
    }
    
    /* Input number specific styling with vibrant colors */
    input[type="number"] {
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%) !important;
        color: #1e40af !important;
        border: 2px solid #93c5fd !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    input[type="number"]:focus {
        background: linear-gradient(135deg, #f0f9ff 0%, #dbeafe 100%) !important;
        color: #1d4ed8 !important;
        border-color: #3b82f6 !important;
        outline: none !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Selectbox dropdown list container */
    [role="listbox"] {
        background-color: white !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Force override any black dropdown backgrounds */
    .stSelectbox div[data-baseweb="select"] div[role="listbox"],
    .stSelectbox [data-baseweb="popover"] div,
    .stSelectbox [data-baseweb="menu"] div,
    div[data-baseweb="select"] ul,
    div[data-baseweb="select"] [role="listbox"],
    .stSelectbox div[data-testid="stSelectbox"] div[role="listbox"] {
        background-color: white !important;
        background: white !important;
    }
    
    /* Force white background on all dropdown options */
    .stSelectbox [role="option"],
    .stSelectbox li,
    div[data-baseweb="select"] li,
    div[data-baseweb="menu"] li {
        background-color: white !important;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        color: #1e40af !important;
    }
    
    /* Hover state for dropdown options */
    .stSelectbox [role="option"]:hover,
    .stSelectbox li:hover,
    div[data-baseweb="select"] li:hover {
        background-color: #dbeafe !important;
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        color: #1d4ed8 !important;
    }
</style>
""", unsafe_allow_html=True)

class FinanceAppGUI:
    def __init__(self):
        self.data_file = "finance_data.json"
        self.account: Optional[Account] = None
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'account_loaded' not in st.session_state:
            st.session_state.account_loaded = False
        if 'show_success_message' not in st.session_state:
            st.session_state.show_success_message = False
        if 'success_message' not in st.session_state:
            st.session_state.success_message = ""
    
    def load_data_from_json(self) -> bool:
        """Load account data from JSON file"""
        try:
            if not os.path.exists(self.data_file):
                return False
            
            with open(self.data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if "account" not in data:
                return False
            
            account_data = data["account"]
            
            # Create account
            self.account = Account(account_data["owner_name"], 0)
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
                
                if transaction.transaction_type == "income":
                    balance += transaction.amount
                else:
                    balance -= transaction.amount
            
            self.account.balance = balance
            st.session_state.account_loaded = True
            return True
            
        except Exception as e:
            st.error(f"❌ Error loading data: {e}")
            return False
    
    def save_data_to_json(self) -> bool:
        """Save account data to JSON file"""
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
            st.error(f"❌ Error saving data: {e}")
            return False
    
    def setup_account_page(self):
        """Setup or login account page"""
        st.markdown('<div class="main-header"><h1>🏦 Setup Akun Keuangan</h1></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if os.path.exists(self.data_file):
                st.info("📁 Data tersimpan ditemukan!")
                
                if st.button("🔄 Load Data yang Sudah Ada", key="load_existing"):
                    if self.load_data_from_json():
                        st.success(f"✅ Data berhasil dimuat untuk {self.account.owner_name}")
                        st.success(f"💳 Saldo: Rp {self.account.get_balance():,.0f}")
                        st.success(f"📝 Transaksi: {len(self.account.transactions)}")
                        st.rerun()
                    else:
                        st.error("❌ Gagal memuat data")
                
                st.markdown("---")
                st.subheader("🆕 Atau Buat Akun Baru")
            
            with st.form("setup_account_form"):
                st.subheader("👤 Informasi Akun")
                name = st.text_input("Nama Pemilik Akun", placeholder="Masukkan nama Anda")
                initial_balance = st.number_input("Saldo Awal (Rp)", min_value=0.0, value=0.0, step=1000.0)
                
                if st.form_submit_button("✅ Buat Akun"):
                    if not name.strip():
                        st.error("❌ Nama tidak boleh kosong!")
                    else:
                        self.account = Account(name.strip(), initial_balance)
                        if self.save_data_to_json():
                            st.success(f"✅ Akun berhasil dibuat untuk {name}")
                            st.success("💾 Data akun tersimpan otomatis")
                            st.session_state.account_loaded = True
                            st.rerun()
                        else:
                            st.error("⚠️ Akun dibuat tetapi gagal menyimpan data")
    
    def main_dashboard(self):
        """Main dashboard page"""
        # Header
        st.markdown('<div class="main-header"><h1>💰 Personal Finance Manager</h1></div>', unsafe_allow_html=True)
        
        # Success message
        if st.session_state.show_success_message:
            st.success(st.session_state.success_message)
            st.session_state.show_success_message = False
        
        # Account info
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <h3 style="color: #1e40af; margin: 0; font-weight: 600; font-size: 16px;">👤 Pemilik</h3>
                <h2 style="color: #1e40af; margin: 0.5rem 0 0 0; font-weight: 700; font-size: 24px;">{self.account.owner_name}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            balance_color = "#059669" if self.account.balance >= 0 else "#dc2626"
            st.markdown(f'''
            <div class="metric-card">
                <h3 style="color: #1e40af; margin: 0; font-weight: 600; font-size: 16px;">💳 Saldo</h3>
                <h2 style="color: {balance_color}; margin: 0.5rem 0 0 0; font-weight: 700; font-size: 24px;">Rp {self.account.balance:,.0f}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <h3 style="color: #1e40af; margin: 0; font-weight: 600; font-size: 16px;">📝 Transaksi</h3>
                <h2 style="color: #1e40af; margin: 0.5rem 0 0 0; font-weight: 700; font-size: 24px;">{len(self.account.transactions)}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <h3 style="color: #1e40af; margin: 0; font-weight: 600; font-size: 16px;">📅 Dibuat</h3>
                <h2 style="color: #1e40af; margin: 0.5rem 0 0 0; font-weight: 700; font-size: 24px;">{self.account.created_date.strftime('%d/%m/%Y')}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        # Main tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["💵 Pemasukan", "💸 Pengeluaran", "📊 Riwayat", "📈 Laporan", "⚙️ Pengaturan"])
        
        with tab1:
            self.add_income_tab()
        
        with tab2:
            self.add_expense_tab()
        
        with tab3:
            self.transaction_history_tab()
        
        with tab4:
            self.financial_reports_tab()
        
        with tab5:
            self.settings_tab()
    
    def add_income_tab(self):
        """Add income tab"""
        st.markdown("### 💵 Tambah Pemasukan")
        st.markdown("---")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("#### 📝 Form Pemasukan")
            with st.form("add_income_form", clear_on_submit=True):
                st.markdown("**💰 Masukkan Detail Pemasukan:**")
                amount = st.number_input(
                    "Jumlah (Rp)", 
                    min_value=0.01, 
                    step=1000.0, 
                    key="income_amount",
                    help="Masukkan jumlah pemasukan dalam Rupiah"
                )
                
                category = st.selectbox(
                    "🏷️ Pilih Kategori",
                    ["Gaji", "Bonus", "Freelance", "Investasi", "Hadiah", "Penjualan", "Lainnya"],
                    key="income_category",
                    help="Pilih kategori yang sesuai dengan jenis pemasukan"
                )
                
                if category == "Lainnya":
                    custom_category = st.text_input(
                        "Kategori Khusus",
                        placeholder="Masukkan kategori pemasukan lainnya",
                        key="income_custom_category"
                    )
                    if custom_category:
                        category = custom_category
                
                st.markdown("---")
                col_btn1, col_btn2 = st.columns([2, 1])
                with col_btn1:
                    submitted = st.form_submit_button("✅ Tambah Pemasukan", type="primary")
                with col_btn2:
                    if amount > 0:
                        st.markdown(f"**Total:** Rp {amount:,.0f}")
                
                if submitted:
                    description = f"Pemasukan - {category}"
                    if self.account.add_income(amount, description, category):
                        if self.save_data_to_json():
                            st.session_state.success_message = f"✅ Pemasukan Rp {amount:,.0f} dari {category} berhasil ditambahkan!"
                            st.session_state.show_success_message = True
                            st.rerun()
        
        with col2:
            st.markdown("#### 💡 Panduan & Tips")
            
            # Current balance info
            st.info(f"""
            **💳 Saldo Saat Ini:**
            
            Rp {self.account.balance:,.0f}
            """)
            
            # Category suggestions
            st.success("""
            **🏷️ Kategori Pemasukan:**
            
            • 💼 **Gaji** - Pendapatan tetap bulanan
            • 🎁 **Bonus** - Bonus kerja/achievement
            • 💻 **Freelance** - Pekerjaan sampingan
            • 📈 **Investasi** - Return investasi
            • 🎊 **Hadiah** - Uang hadiah/THR
            • 🛒 **Penjualan** - Hasil jual barang
            """)
            
            # Recent income
            recent_income = [t for t in self.account.transactions[-5:] if t.transaction_type == "income"]
            if recent_income:
                st.markdown("#### 📋 Pemasukan Terakhir")
                for trans in reversed(recent_income):
                    st.markdown(f"• **{trans.category}**: Rp {trans.amount:,.0f}")
            
            # Monthly summary
            from datetime import datetime
            current_month = datetime.now().month
            current_year = datetime.now().year
            monthly_summary = self.account.get_monthly_summary(current_month, current_year)
            
            if monthly_summary['total_income'] > 0:
                st.warning(f"""
                **📊 Bulan Ini:**
                
                Total Pemasukan: Rp {monthly_summary['total_income']:,.0f}
                """)
    
    def add_expense_tab(self):
        """Add expense tab"""
        st.markdown("### 💸 Tambah Pengeluaran")
        st.markdown("---")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("#### 📝 Form Pengeluaran")
            
            # Balance warning
            if self.account.balance < 100000:
                st.warning("⚠️ **Peringatan**: Saldo Anda kurang dari Rp 100,000")
            
            with st.form("add_expense_form", clear_on_submit=True):
                st.markdown("**💰 Masukkan Detail Pengeluaran:**")
                amount = st.number_input(
                    "Jumlah (Rp)", 
                    min_value=0.01, 
                    step=1000.0, 
                    key="expense_amount",
                    help="Masukkan jumlah pengeluaran dalam Rupiah"
                )
                
                # Check if amount exceeds balance
                if amount > self.account.balance:
                    st.error(f"❌ Jumlah melebihi saldo! Saldo tersedia: Rp {self.account.balance:,.0f}")
                
                category = st.selectbox(
                    "🏷️ Pilih Kategori", 
                    ["Makanan", "Transportasi", "Belanja", "Hiburan", "Tagihan", "Kesehatan", "Pendidikan", "Lainnya"],
                    key="expense_category",
                    help="Pilih kategori yang sesuai dengan jenis pengeluaran"
                )
                
                if category == "Lainnya":
                    custom_category = st.text_input(
                        "Kategori Khusus",
                        placeholder="Masukkan kategori pengeluaran lainnya",
                        key="expense_custom_category"
                    )
                    if custom_category:
                        category = custom_category
                
                # Show remaining balance
                remaining_balance = self.account.balance - amount
                if amount > 0:
                    if remaining_balance >= 0:
                        st.success(f"💳 Sisa saldo setelah transaksi: Rp {remaining_balance:,.0f}")
                    else:
                        st.error(f"❌ Saldo tidak mencukupi! Kurang: Rp {abs(remaining_balance):,.0f}")
                
                st.markdown("---")
                col_btn1, col_btn2 = st.columns([2, 1])
                with col_btn1:
                    submitted = st.form_submit_button(
                        "✅ Tambah Pengeluaran", 
                        type="primary",
                        disabled=(amount > self.account.balance)
                    )
                with col_btn2:
                    if amount > 0:
                        st.markdown(f"**Total:** Rp {amount:,.0f}")
                
                if submitted:
                    if amount > self.account.balance:
                        st.error(f"❌ Saldo tidak mencukupi. Saldo saat ini: Rp {self.account.balance:,.0f}")
                    else:
                        description = f"Pengeluaran - {category}"
                        if self.account.add_expense(amount, description, category):
                            if self.save_data_to_json():
                                st.session_state.success_message = f"✅ Pengeluaran Rp {amount:,.0f} untuk {category} berhasil dicatat!"
                                st.session_state.show_success_message = True
                                st.rerun()
        
        with col2:
            st.markdown("#### 💡 Panduan & Tips")
            
            # Current balance with color coding
            balance_color = "success" if self.account.balance >= 100000 else "warning" if self.account.balance >= 50000 else "error"
            if balance_color == "success":
                st.success(f"""
                **💳 Saldo Saat Ini:**
                
                Rp {self.account.balance:,.0f}
                
                ✅ Saldo aman untuk transaksi
                """)
            elif balance_color == "warning":
                st.warning(f"""
                **� Saldo Saat Ini:**
                
                Rp {self.account.balance:,.0f}
                
                ⚠️ Saldo mulai menipis
                """)
            else:
                st.error(f"""
                **💳 Saldo Saat Ini:**
                
                Rp {self.account.balance:,.0f}
                
                🚨 Saldo sangat rendah!
                """)
            
            # Category guide
            st.info("""
            **🏷️ Kategori Pengeluaran:**
            
            • 🍽️ **Makanan** - Makan, minum, groceries
            • 🚗 **Transportasi** - Bensin, parkir, ojol
            • 🛍️ **Belanja** - Pakaian, elektronik
            • 🎬 **Hiburan** - Film, game, rekreasi
            • 💡 **Tagihan** - Listrik, air, internet
            • 🏥 **Kesehatan** - Obat, dokter, asuransi
            • 📚 **Pendidikan** - Kursus, buku, training
            """)
            
            # Recent expenses
            recent_expenses = [t for t in self.account.transactions[-5:] if t.transaction_type == "expense"]
            if recent_expenses:
                st.markdown("#### 📋 Pengeluaran Terakhir")
                for trans in reversed(recent_expenses):
                    st.markdown(f"• **{trans.category}**: Rp {trans.amount:,.0f}")
            
            # Monthly spending summary
            from datetime import datetime
            current_month = datetime.now().month
            current_year = datetime.now().year
            monthly_summary = self.account.get_monthly_summary(current_month, current_year)
            
            if monthly_summary['total_expense'] > 0:
                st.warning(f"""
                **📊 Pengeluaran Bulan Ini:**
                
                Total: Rp {monthly_summary['total_expense']:,.0f}
                Net Income: Rp {monthly_summary['net_income']:,.0f}
                """)
    
    def transaction_history_tab(self):
        """Transaction history tab"""
        st.subheader("📊 Riwayat Transaksi")
        
        transactions = self.account.get_transaction_history()
        
        if not transactions:
            st.info("📝 Belum ada transaksi yang tercatat")
            return
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_type = st.selectbox("Filter Jenis", ["Semua", "Pemasukan", "Pengeluaran"])
        
        with col2:
            categories = list(set([t.category for t in transactions]))
            filter_category = st.selectbox("Filter Kategori", ["Semua"] + categories)
        
        with col3:
            limit = st.selectbox("Tampilkan", [10, 25, 50, "Semua"])
        
        # Filter transactions
        filtered_transactions = transactions
        
        if filter_type != "Semua":
            type_filter = "income" if filter_type == "Pemasukan" else "expense"
            filtered_transactions = [t for t in filtered_transactions if t.transaction_type == type_filter]
        
        if filter_category != "Semua":
            filtered_transactions = [t for t in filtered_transactions if t.category == filter_category]
        
        if limit != "Semua":
            filtered_transactions = filtered_transactions[-limit:]
        
        # Display transactions
        if filtered_transactions:
            # Create DataFrame for better display
            df_data = []
            running_balance = 0
            
            # Calculate running balance from the beginning if showing all
            if limit == "Semua":
                running_balance = 0
                for transaction in self.account.transactions:
                    if transaction in filtered_transactions:
                        if transaction.transaction_type == "income":
                            running_balance += transaction.amount
                        else:
                            running_balance -= transaction.amount
            
            for transaction in reversed(filtered_transactions):
                icon = "💵" if transaction.transaction_type == "income" else "💸"
                amount_display = f"+ {transaction.amount:,.0f}" if transaction.transaction_type == "income" else f"- {transaction.amount:,.0f}"
                
                df_data.append({
                    "Tanggal": transaction.date.strftime('%d/%m/%Y %H:%M'),
                    "": icon,
                    "Kategori": transaction.category,
                    "Deskripsi": transaction.description,
                    "Jumlah": amount_display
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, width='stretch', hide_index=True)
        
        else:
            st.info("Tidak ada transaksi sesuai filter yang dipilih")
    
    def financial_reports_tab(self):
        """Financial reports tab"""
        st.subheader("📈 Laporan Keuangan")
        
        transactions = self.account.transactions
        
        if not transactions:
            st.info("📊 Belum ada data untuk laporan")
            return
        
        # Monthly Summary
        current_date = datetime.now()
        monthly_summary = self.account.get_monthly_summary(current_date.month, current_date.year)
        
        st.markdown("### 📅 Ringkasan Bulan Ini")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💵 Total Pemasukan", f"Rp {monthly_summary['total_income']:,.0f}")
        
        with col2:
            st.metric("💸 Total Pengeluaran", f"Rp {monthly_summary['total_expense']:,.0f}")
        
        with col3:
            net_income = monthly_summary['net_income']
            net_color = "normal" if net_income >= 0 else "inverse"
            st.metric("📊 Net Income", f"Rp {net_income:,.0f}")
        
        with col4:
            st.metric("🔢 Transaksi", monthly_summary['transaction_count'])
        
        # Category Analysis
        category_summary = self.account.get_category_summary()
        
        if category_summary:
            st.markdown("### 🏷️ Analisis per Kategori")
            
            # Prepare data for charts
            categories = []
            income_amounts = []
            expense_amounts = []
            
            for category, data in category_summary.items():
                categories.append(category)
                income_amounts.append(data["income"])
                expense_amounts.append(data["expense"])
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Income by category pie chart
                if any(income_amounts):
                    # Custom color palette for better contrast
                    income_colors = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4', '#84cc16', '#f97316']
                    
                    fig_income = px.pie(
                        values=[amount for amount in income_amounts if amount > 0],
                        names=[cat for i, cat in enumerate(categories) if income_amounts[i] > 0],
                        title="Pemasukan per Kategori",
                        color_discrete_sequence=income_colors
                    )
                    fig_income.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='white',
                        font=dict(color='#0f172a', size=12, family="Arial, sans-serif"),
                        title=dict(
                            font=dict(color='#1e40af', size=16, family="Arial, sans-serif"),
                            x=0.5
                        ),
                        showlegend=True,
                        legend=dict(
                            font=dict(color='#374151', size=11),
                            bgcolor='rgba(255,255,255,0.8)',
                            bordercolor='#e5e7eb',
                            borderwidth=1
                        )
                    )
                    
                    # Update text styling for better readability
                    fig_income.update_traces(
                        textposition='auto',
                        textinfo='percent+label',
                        textfont=dict(size=11, color='white', family="Arial, sans-serif"),
                        marker=dict(line=dict(color='#ffffff', width=2)),
                        hovertemplate='<b>%{label}</b><br>Jumlah: Rp %{value:,.0f}<br>Persentase: %{percent}<extra></extra>'
                    )
                    
                    st.plotly_chart(fig_income, width='stretch')
            
            with col2:
                # Expense by category pie chart
                if any(expense_amounts):
                    # Custom color palette for expenses with better contrast
                    expense_colors = ['#dc2626', '#f59e0b', '#7c3aed', '#ec4899', '#06b6d4', '#84cc16', '#f97316', '#6366f1']
                    
                    fig_expense = px.pie(
                        values=[amount for amount in expense_amounts if amount > 0],
                        names=[cat for i, cat in enumerate(categories) if expense_amounts[i] > 0],
                        title="Pengeluaran per Kategori",
                        color_discrete_sequence=expense_colors
                    )
                    fig_expense.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='white',
                        font=dict(color='#0f172a', size=12, family="Arial, sans-serif"),
                        title=dict(
                            font=dict(color='#dc2626', size=16, family="Arial, sans-serif"),
                            x=0.5
                        ),
                        showlegend=True,
                        legend=dict(
                            font=dict(color='#374151', size=11),
                            bgcolor='rgba(255,255,255,0.8)',
                            bordercolor='#e5e7eb',
                            borderwidth=1
                        )
                    )
                    
                    # Update text styling for better readability
                    fig_expense.update_traces(
                        textposition='auto',
                        textinfo='percent+label',
                        textfont=dict(size=11, color='white', family="Arial, sans-serif"),
                        marker=dict(line=dict(color='#ffffff', width=2)),
                        hovertemplate='<b>%{label}</b><br>Jumlah: Rp %{value:,.0f}<br>Persentase: %{percent}<extra></extra>'
                    )
                    
                    st.plotly_chart(fig_expense, width='stretch')
        
        # Daily Balance Trend (last 30 days)
        if len(transactions) > 1:
            st.markdown("### 📈 Tren Saldo Harian (30 Hari Terakhir)")
            
            # Calculate daily balance
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            daily_balances = {}
            balance = 0
            
            # Get initial balance (transactions before start_date)
            for transaction in transactions:
                if transaction.date < start_date:
                    if transaction.transaction_type == "income":
                        balance += transaction.amount
                    else:
                        balance -= transaction.amount
            
            # Calculate daily balances for the last 30 days
            current_date = start_date
            while current_date <= end_date:
                daily_balances[current_date.strftime('%Y-%m-%d')] = balance
                
                # Add transactions for this day
                day_transactions = [t for t in transactions if t.date.date() == current_date.date()]
                for transaction in day_transactions:
                    if transaction.transaction_type == "income":
                        balance += transaction.amount
                    else:
                        balance -= transaction.amount
                
                current_date += timedelta(days=1)
            
            # Create line chart
            dates = list(daily_balances.keys())
            balances = list(daily_balances.values())
            
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=dates,
                y=balances,
                mode='lines+markers',
                name='Saldo',
                line=dict(color='#3b82f6', width=3),
                marker=dict(color='#1e40af', size=6)
            ))
            
            fig_trend.update_layout(
                title=dict(
                    text="Tren Saldo Harian",
                    font=dict(color='#1e40af', size=16, family="Arial, sans-serif"),
                    x=0.5
                ),
                xaxis_title=dict(
                    text="Tanggal",
                    font=dict(color='#374151', size=12)
                ),
                yaxis_title=dict(
                    text="Saldo (Rp)",
                    font=dict(color='#374151', size=12)
                ),
                xaxis=dict(
                    tickfont=dict(color='#1f2937', size=10),
                    gridcolor='#f3f4f6',
                    linecolor='#d1d5db'
                ),
                yaxis=dict(
                    tickfont=dict(color='#1f2937', size=10),
                    gridcolor='#f3f4f6',
                    linecolor='#d1d5db'
                ),
                plot_bgcolor='rgba(248,250,252,0.5)',
                paper_bgcolor='white',
                font=dict(color='#0f172a', family="Arial, sans-serif"),
                showlegend=False,
                margin=dict(l=60, r=20, t=60, b=40)
            )
            
            st.plotly_chart(fig_trend, width='stretch')
    
    def settings_tab(self):
        """Settings tab"""
        st.subheader("⚙️ Pengaturan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👤 Informasi Akun")
            
            with st.form("change_name_form"):
                new_name = st.text_input("Nama Baru", value=self.account.owner_name)
                
                if st.form_submit_button("💾 Simpan Perubahan"):
                    if new_name.strip() and new_name != self.account.owner_name:
                        old_name = self.account.owner_name
                        self.account.owner_name = new_name.strip()
                        
                        if self.save_data_to_json():
                            st.success(f"✅ Nama berhasil diubah dari '{old_name}' ke '{new_name}'")
                        else:
                            st.error("❌ Gagal menyimpan perubahan")
                    else:
                        st.info("ℹ️ Tidak ada perubahan yang disimpan")
        
        with col2:
            st.markdown("#### 📊 Informasi Data")
            st.info(f"""
            📁 **File Data:** {self.data_file}
            
            📄 **Status:** {'✅ Ada' if os.path.exists(self.data_file) else '❌ Tidak ada'}
            
            📏 **Ukuran File:** {os.path.getsize(self.data_file) if os.path.exists(self.data_file) else 0} bytes
            
            ⏰ **Terakhir Diubah:** {datetime.fromtimestamp(os.path.getmtime(self.data_file)).strftime('%d/%m/%Y %H:%M:%S') if os.path.exists(self.data_file) else 'N/A'}
            """)
        
        st.markdown("---")
        
        # Export and backup options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📁 Simpan Data Manual"):
                if self.save_data_to_json():
                    st.success("✅ Data berhasil disimpan")
                else:
                    st.error("❌ Gagal menyimpan data")
        
        with col2:
            if st.button("🔄 Reload Data"):
                if self.load_data_from_json():
                    st.success("✅ Data berhasil dimuat ulang")
                    st.rerun()
                else:
                    st.error("❌ Gagal memuat data")
        
        with col3:
            if st.button("💾 Export ke CSV"):
                self.export_to_csv()
        
        # Reset account option (with confirmation)
        st.markdown("---")
        st.markdown("#### ⚠️ Zona Berbahaya")
        
        if st.checkbox("Saya ingin reset akun (hapus semua data)"):
            if st.button("🗑️ Reset Akun", type="secondary"):
                if os.path.exists(self.data_file):
                    os.remove(self.data_file)
                st.session_state.account_loaded = False
                st.success("✅ Akun berhasil direset. Silakan refresh halaman.")
                st.rerun()
    
    def export_to_csv(self):
        """Export transactions to CSV"""
        if not self.account or not self.account.transactions:
            st.error("❌ Tidak ada data untuk di-export!")
            return
        
        try:
            # Prepare data for CSV
            csv_data = []
            running_balance = 0
            
            for transaction in self.account.transactions:
                if transaction.transaction_type == "income":
                    running_balance += transaction.amount
                    amount_display = f"+{transaction.amount:,.0f}"
                else:
                    running_balance -= transaction.amount
                    amount_display = f"-{transaction.amount:,.0f}"
                
                csv_data.append({
                    'Tanggal': transaction.date.strftime('%d/%m/%Y %H:%M'),
                    'Jenis': transaction.transaction_type.capitalize(),
                    'Kategori': transaction.category,
                    'Deskripsi': transaction.description,
                    'Jumlah': amount_display,
                    'Saldo': f"{running_balance:,.0f}"
                })
            
            df = pd.DataFrame(csv_data)
            csv = df.to_csv(index=False)
            
            # Create download button
            filename = f"finance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            st.download_button(
                label="📥 Download File CSV",
                data=csv,
                file_name=filename,
                mime="text/csv"
            )
            
            st.success(f"✅ File CSV siap didownload: {filename}")
            
        except Exception as e:
            st.error(f"❌ Error exporting to CSV: {e}")
    
    def run(self):
        """Run the Streamlit application"""
        # Load existing data if available
        if not st.session_state.account_loaded and os.path.exists(self.data_file):
            self.load_data_from_json()
        
        # Main application logic
        if not st.session_state.account_loaded or self.account is None:
            self.setup_account_page()
        else:
            self.main_dashboard()

# Run the application
if __name__ == "__main__":
    app = FinanceAppGUI()
    app.run()