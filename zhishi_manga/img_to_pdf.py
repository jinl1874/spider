from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfgen import canvas
import os


def convert_images_to_pdf(img_path, pdf_path):
    pages = 0
    (w, h) = portrait(A4)
    c = canvas.Canvas(pdf_path, pagesize=portrait(A4))
    l = os.listdir(img_path)
    l.sort(key=lambda x: int(x[:-4]))
    for i in l:
        f = img_path + os.sep + str(i)
        c.drawImage(f, 0, 0, w, h)
        c.showPage()
        pages = pages + 1
    c.save()


path = r"D://web//script//pxtt-118"
pdf_path = r"D://web//script//pdf//pxtt-118.pdf"

convert_images_to_pdf(path, pdf_path)
