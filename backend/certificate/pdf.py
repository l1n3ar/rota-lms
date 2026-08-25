"""PDF rendering for issued certificates."""
import io
import logging

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

logger = logging.getLogger(__name__)

NAVY = colors.HexColor("#1F3A5F")
GOLD = colors.HexColor("#C9A227")
GREY = colors.HexColor("#555555")


def _display_name(user):
    name = f"{user.first_name} {user.last_name}".strip()
    return name or user.email


def generate_certificate_pdf(issued_certificate) -> io.BytesIO:
    """Render an IssuedCertificate as a landscape A4 PDF and return the buffer."""
    certificate = issued_certificate.certificate
    page_w, page_h = landscape(A4)

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(page_w, page_h))

    # Optional background template image, stretched to fill the page
    if certificate.picture and certificate.picture.name:
        try:
            with certificate.picture.open("rb") as template_file:
                pdf.drawImage(ImageReader(template_file), 0, 0, width=page_w, height=page_h)
        except OSError as exc:
            logger.warning(
                "Could not load certificate template image %s: %s",
                certificate.picture.name, exc,
            )

    # Decorative double border
    margin = 18 * mm
    pdf.setLineWidth(2.5)
    pdf.setStrokeColor(NAVY)
    pdf.rect(margin, margin, page_w - 2 * margin, page_h - 2 * margin)

    pdf.setLineWidth(0.8)
    pdf.setStrokeColor(GOLD)
    pdf.rect(
        margin + 4 * mm, margin + 4 * mm,
        page_w - 2 * (margin + 4 * mm), page_h - 2 * (margin + 4 * mm),
    )

    center = page_w / 2

    # Header
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(center, page_h - 45 * mm, "ROTA LMS")

    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 34)
    pdf.drawCentredString(center, page_h - 62 * mm, "Certificate of Completion")

    pdf.setFillColor(GREY)
    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(center, page_h - 70 * mm, "This certificate is proudly presented to")

    # Recipient
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(center, page_h - 86 * mm, _display_name(issued_certificate.user))

    # Course
    pdf.setFillColor(GREY)
    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(center, page_h - 98 * mm, "for successfully completing")

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(center, page_h - 108 * mm, certificate.title)

    if issued_certificate.score is not None:
        pdf.setFillColor(GREY)
        pdf.setFont("Helvetica", 12)
        pdf.drawCentredString(center, page_h - 118 * mm, f"Score: {issued_certificate.score}%")

    # Footer: issue date, verification code, signature
    pdf.setFillColor(GREY)
    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(center, 40 * mm, f"Issued on {issued_certificate.issued_at:%B %d, %Y}")

    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(center, 34 * mm, f"Verification code: {issued_certificate.verification_code}")

    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(0.6)
    pdf.line(page_w - 75 * mm, 52 * mm, page_w - 30 * mm, 52 * mm)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(page_w - 52.5 * mm, 48 * mm, "Authorized Signature")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer
