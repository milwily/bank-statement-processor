"""
Bank Statement PDF to Excel Converter - Usage Examples
This file demonstrates 5 different ways to use the converter.
"""

from pdf_parser import BankStatementParser
from excel_exporter import ExcelExporter
import pandas as pd

# =============================================================================
# EXAMPLE 1: Basic Usage - Process a single PDF and export to Excel
# =============================================================================
def example_basic_usage():
    """Simple example to process a bank statement PDF."""
    print("📌 Example 1: Basic Usage")
    
    # Parse PDF
    parser = BankStatementParser('bank_statement.pdf')
    transactions = parser.parse_transactions()
    
    # Export to Excel
    exporter = ExcelExporter('output.xlsx')
    exporter.export_transactions(transactions)
    
    print(f"✅ Processed {len(transactions)} transactions\n")


# =============================================================================
# EXAMPLE 2: With Summary Statistics
# =============================================================================
def example_with_summary():
    """Process PDF and include summary statistics in Excel."""
    print("📌 Example 2: With Summary Statistics")
    
    parser = BankStatementParser('bank_statement.pdf')
    transactions = parser.parse_transactions()
    summary = parser.get_summary()
    
    print(f"Summary Statistics:")
    print(f"  Total Transactions: {summary['total_transactions']}")
    print(f"  Total Amount: ${summary['total_amount']:.2f}")
    print(f"  Average Amount: ${summary['average_amount']:.2f}")
    
    exporter = ExcelExporter('output_with_summary.xlsx')
    exporter.export_transactions(transactions, summary)
    
    print(f"✅ Excel file created with summary sheet\n")


# =============================================================================
# EXAMPLE 3: Process Multiple PDFs
# =============================================================================
def example_multiple_pdfs():
    """Process multiple bank statement PDFs."""
    print("📌 Example 3: Process Multiple PDFs")
    
    pdf_files = ['statement_jan.pdf', 'statement_feb.pdf', 'statement_mar.pdf']
    all_transactions = []
    
    for pdf_file in pdf_files:
        try:
            parser = BankStatementParser(pdf_file)
            transactions = parser.parse_transactions()
            all_transactions.extend(transactions)
            print(f"✅ Processed {pdf_file}: {len(transactions)} transactions")
        except Exception as e:
            print(f"⚠️  Error processing {pdf_file}: {str(e)}")
    
    # Export all to single Excel
    exporter = ExcelExporter('combined_statements.xlsx')
    exporter.export_transactions(all_transactions)
    
    print(f"✅ Total transactions from all files: {len(all_transactions)}\n")


# =============================================================================
# EXAMPLE 4: Filter Transactions and Export
# =============================================================================
def example_filter_transactions():
    """Parse transactions and filter before exporting."""
    print("📌 Example 4: Filter Transactions")
    
    parser = BankStatementParser('bank_statement.pdf')
    transactions = parser.parse_transactions()
    
    # Filter transactions with amounts over $1000
    large_transactions = [
        t for t in transactions 
        if t.get('amount') and float(t['amount'].replace('$', '').replace(',', '')) > 1000
    ]
    
    print(f"Found {len(large_transactions)} transactions over $1000")
    
    exporter = ExcelExporter('large_transactions.xlsx')
    exporter.export_transactions(large_transactions)
    
    print(f"✅ Filtered transactions exported\n")


# =============================================================================
# EXAMPLE 5: Work with Pandas DataFrame
# =============================================================================
def example_pandas_workflow():
    """Parse PDF, work with Pandas, and export to Excel."""
    print("📌 Example 5: Pandas DataFrame Workflow")
    
    parser = BankStatementParser('bank_statement.pdf')
    transactions = parser.parse_transactions()
    
    # Convert to Pandas DataFrame
    df = pd.DataFrame(transactions)
    
    # Data analysis
    print(f"DataFrame Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # You can now use Pandas operations
    # Example: Group by description, sum amounts, etc.
    if 'description' in df.columns and 'amount' in df.columns:
        print(f"\nTop 5 Descriptions:")
        print(df['description'].value_counts().head(5))
    
    # Export to Excel using Pandas
    df.to_excel('pandas_export.xlsx', sheet_name='Transactions', index=False)
    
    print(f"✅ Exported {len(df)} transactions to Excel\n")


# =============================================================================
# Run Examples (Uncomment to test)
# =============================================================================
if __name__ == "__main__":
    print("🏦 Bank Statement PDF to Excel Converter - Usage Examples\n")
    print("=" * 60)
    
    # Uncomment examples to run:
    # example_basic_usage()
    # example_with_summary()
    # example_multiple_pdfs()
    # example_filter_transactions()
    # example_pandas_workflow()
    
    print("\n📝 Note: Update file paths before running examples!")
