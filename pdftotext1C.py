import pdftotext

# Load your PDF
with open("C:\DATA\RIPTEXT.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)

# Save all text to a txt file.
with open('C:\DATA\ANAPLAN_TEXT.txt', 'w') as f:
    f.write("\n\n".join(pdf))