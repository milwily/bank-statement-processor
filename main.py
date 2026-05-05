import sys
import os
from pdf_parser import BankStatementParser
from excel_exporter import ExcelExporter

def main():
    """
    Command-line interface for processing bank statement PDFs.
    Usage: python main.py <input_pdf> [output_excel]
    """
    
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_pdf> [output_excel]")
        print("Example: python main.py bank_statement.pdf output.xlsx")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_excel = sys.argv[2] if len(sys.argv) > 2 else input_pdf.replace('.pdf', '_extracted.xlsx')
    
    # Check if PDF exists
    if not os.path.exists(input_pdf):
        print(f"❌ Error: PDF file '{input_pdf}' not found!")
        sys.exit(1)
    
    try:
        print(f"📄 Processing: {input_pdf}")
        
        # Parse PDF
        parser = BankStatementParser(input_pdf)
        transactions = parser.parse_transactions()
        summary = parser.get_summary()
        
        print(f"✅ Extracted {len(transactions)} transactions")
        print(f"   Total Amount: ${summary['total_amount']:.2f}")
        print(f"   Average Amount: ${summary['average_amount']:.2f}")
        
        # Export to Excel
        exporter = ExcelExporter(output_excel)
        exporter.export_transactions(transactions, summary)
        
        print(f"✅ Success! Excel file saved: {output_excel}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
