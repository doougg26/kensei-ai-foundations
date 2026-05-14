from pathlib import Path
from PyPDF2 import PdfReader
import sys
path = Path('Kensei_AI_Foundations_Aula_Inaugural.pptx.pdf')
reader = PdfReader(path)
for i, page in enumerate(reader.pages, 1):
    text = page.extract_text() or ''
    print(f'--- PAGE {i} ---')
    print(text)
