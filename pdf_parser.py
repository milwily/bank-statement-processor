import PyPDF2
from datetime import datetime
from dateutil import parser as date_parser
import re

class BankStatementParser:
    """
    Parses bank statement PDFs and extracts transaction data.
    Supports multiple date formats and transaction patterns.
    """
    
    def __init__(self, pdf_path):
        """Initialize parser with PDF file path."""
        self.pdf_path = pdf_path
        self.text = None
        self.transactions = []
        
    def extract_text(self):
        """Extract all text from PDF file."""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                self.text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    self.text += page.extract_text()
            return self.text
        except FileNotFoundError:
            raise Exception(f"PDF file not found: {self.pdf_path}")
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def parse_dates(self, text):
        """Extract dates from text in multiple formats."""
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',      # MM/DD/YYYY or DD/MM/YYYY
            r'\d{4}-\d{1,2}-\d{1,2}',      # YYYY-MM-DD
            r'\d{1,2}-\d{1,2}-\d{4}',      # DD-MM-YYYY
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4}',  # Jan 01, 2024
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                try:
                    date_obj = date_parser.parse(match)
                    dates.append(date_obj)
                except:
                    pass
        
        return dates
    
    def parse_amounts(self, text):
        """Extract monetary amounts from text."""
        amount_pattern = r'\$?\d+(?:,\d{3})*\.?\d{0,2}'
        amounts = re.findall(amount_pattern, text)
        return amounts
    
    def parse_transactions(self):
        """Parse complete transactions with date, description, and amount."""
        if not self.text:
            self.extract_text()
        
        # Split text into lines
        lines = self.text.split('\n')
        
        transactions = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Try to extract transaction pattern: Date | Description | Amount
            parts = re.split(r'\s{2,}', line)  # Split by multiple spaces
            
            if len(parts) >= 2:
                # Check if first part is a date
                first_part = parts[0]
                try:
                    trans_date = date_parser.parse(first_part)
                    
                    # Extract amount (look for currency patterns)
                    amount_match = re.search(r'-?\$?[\d,]+\.?\d{0,2}', line)
                    amount = amount_match.group() if amount_match else None
                    
                    # Description is everything between date and amount
                    description = ' '.join(parts[1:-1]) if len(parts) > 2 else parts[1]
                    
                    transaction = {
                        'date': trans_date,
                        'description': description[:100],  # Limit description length
                        'amount': amount,
                        'raw_line': line
                    }
                    
                    transactions.append(transaction)
                except:
                    pass
        
        self.transactions = transactions
        return transactions
    
    def get_summary(self):
        """Generate summary statistics of transactions."""
        if not self.transactions:
            self.parse_transactions()
        
        total_transactions = len(self.transactions)
        
        amounts = []
        for trans in self.transactions:
            if trans['amount']:
                try:
                    amount = float(trans['amount'].replace('$', '').replace(',', ''))
                    amounts.append(amount)
                except:
                    pass
        
        summary = {
            'total_transactions': total_transactions,
            'total_amount': sum(amounts) if amounts else 0,
            'average_amount': sum(amounts) / len(amounts) if amounts else 0,
            'max_amount': max(amounts) if amounts else 0,
            'min_amount': min(amounts) if amounts else 0,
        }
        
        return summary
