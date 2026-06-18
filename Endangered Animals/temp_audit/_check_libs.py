for mod in ['PyMuPDF', 'fitz', 'pdfplumber', 'pypdf', 'pikepdf', 'reportlab', 'pdfminer']:
    try:
        __import__(mod)
        print(f'{mod}: YES')
    except ImportError:
        print(f'{mod}: no')
