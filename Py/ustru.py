import re

text = "John Doe was admitted on 12/25/2020. Contact: john.doe@example.com, SSN: 123-45-6789"
text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN REDACTED]', text)  # SSN Removal
text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL REDACTED]', text)  # Email Removal
print(text)
