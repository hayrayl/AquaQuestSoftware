from pdf2image import convert_from_path

# Path to the PDF file
pdf_path = 'your_file.pdf'

# Convert PDF to images
images = convert_from_path("FlowChart.pdf")

# Save images
for i, image in enumerate(images):
    image.save(f'page_{i + 1}.jpg', 'JPEG')
