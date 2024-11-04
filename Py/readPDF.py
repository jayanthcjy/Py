import PyPDF2

with open(r'C:\Users\Jayanth C\Downloads\sample-1.pdf', 'rb') as pdf_file:
    reader = PyPDF2.PdfFileReader(pdf_file)
    text_data = ''
    for page_num in range(reader.numPages):
        page = reader.getPage(page_num)
        text_data += page.extract_text()
    print(text_data)
