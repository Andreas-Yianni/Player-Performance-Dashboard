from pathlib import Path
from pypdf import PdfReader

root = Path('..') / 'thesis' / 'references'
for path in sorted(root.glob('*.pdf')):
    print(f'===== {path.name} =====')
    try:
        reader = PdfReader(str(path))
        text = '\n'.join(page.extract_text() or '' for page in reader.pages[:3])
        print(text[:4000])
    except Exception as exc:
        print(f'ERROR: {exc}')
    print('\n')
