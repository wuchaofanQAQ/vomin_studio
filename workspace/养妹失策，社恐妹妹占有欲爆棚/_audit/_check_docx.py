import sys
try:
    import docx
    print("python-docx ok", docx.__version__ if hasattr(docx,'__version__') else "")
except Exception as e:
    print("ERR", e)
