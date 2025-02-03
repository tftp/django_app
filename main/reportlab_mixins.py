import io

from django.db.models import Prefetch
from django.http import FileResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.utils import dateformat
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

from main.models import Customer, Product, Record


class PDFCreator():
    PAGE_HEIGHT = A4[0]
    PAGE_WIDTH = A4[1]
    styles = getSampleStyleSheet()
    styles['Normal'].fontName = 'FreeSans'
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf', 'UTF-8'))
    pdfmetrics.registerFont(TTFont('FreeSansBold', 'FreeSansBold.ttf', 'UTF-8'))

    def create_for_customer(self, request: HttpRequest, pk: int) -> FileResponse:
        self.user = request.user

        self.customer = get_object_or_404(Customer, pk=pk)
        records = self.customer.record_set.all()

        filename = f"Карточка учета МЦ {self.customer.fio()}.pdf"
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=(self.PAGE_WIDTH, self.PAGE_HEIGHT), title=filename)

        Story = [Spacer(mm, mm*70)]
        style = self.styles["Normal"]
        style.fontSize = 6

        data = []
        head = [
            Paragraph("Наименование выданных материальных ценностей", style),
            Paragraph("Вид материальных ценностей", style),
            Paragraph("Единица измерения", style),
            Paragraph("Количество", style),
            Paragraph("Инвентарный номер", style),
            Paragraph("Дата выдачи", style),
            Paragraph("Подпись пользователя", style),
            Paragraph("Дата возврата", style),
            Paragraph("Подпись МОЛ", style),
        ]
        data.append(head)

        style.fontSize = 8
        for record in records:
            row = []
            row.append(Paragraph(record.product.name, style))
            row.append('')
            row.append('')
            row.append('')
            row.append(Paragraph(record.product.identity_number, style))
            row.append(Paragraph(dateformat.format(record.set_date, 'd.m.Y'), style))
            row.append('')
            if record.unset_date:
                row.append(Paragraph(dateformat.format(record.unset_date, 'd.m.Y'), style))
            else:
                row.append('')
            row.append('')
            data.append(row)

        t = Table(data, colWidths=[mm*85,mm*23,mm*20,mm*20,mm*25,mm*20,mm*20,mm*20,mm*20])
        t.setStyle(TableStyle([
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ]))
        Story.append(t)

        doc.build(Story, onFirstPage=self.myHeader)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=filename)

    def create_for_vedomost(self, request: HttpRequest, type: str) -> FileResponse:
        records = Product.objects.filter(producttype__name__icontains=type, archived__exact=0).prefetch_related(
            Prefetch('record_set', queryset=Record.objects.filter(unset_date=None).select_related("customer")),
        )

        filename = f"Ведомость.pdf"
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=(self.PAGE_HEIGHT, self.PAGE_WIDTH), title=filename)

        Story = [Spacer(mm, mm)]
        style = self.styles["Normal"]
        style.fontSize = 6

        data = []
        head = [
            Paragraph("Материальные ценности", style),
            Paragraph("Инвентарный номер", style),
            Paragraph("Текущий пользователь", style),
            Paragraph("Тип", style),
            Paragraph("Примечание", style),
        ]
        data.append(head)

        style.fontSize = 8
        for record in records:
            row = []
            row.append(Paragraph(record.name, style))
            row.append(Paragraph(record.identity_number, style))
            if record.record_set.first():
                row.append(Paragraph(record.record_set.first().customer.fio(), style))
                print(record.record_set.first().description)
            else:
                row.append('')
            row.append(Paragraph(record.producttype.name, style))
            if record.record_set.first() and record.record_set.first().description:
                row.append(Paragraph(str(record.record_set.first().description), style))
            else:
                row.append(Paragraph(str(record.description), style))
            data.append(row)

        t = Table(data, colWidths=[mm*55,mm*20,mm*25,mm*25,mm*55])
        t.setStyle(TableStyle([
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ]))
        Story.append(t)

        doc.build(Story, onFirstPage=self.vedomostHeader)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=filename)

    def myHeader(self, canvas: canvas.Canvas, doc):
        canvas.saveState()
        canvas.setFont("FreeSans", 6)
        canvas.drawRightString(770, self.PAGE_HEIGHT - 50, "Приложение №5")
        canvas.drawRightString(770, self.PAGE_HEIGHT - 60, "Для внутреннего пользования в подразделении")
        canvas.drawRightString(770, self.PAGE_HEIGHT - 70, "Хранится у материально-ответственного лица подразделения")

        canvas.setFont("FreeSansBold", 8)
        canvas.drawString(50, self.PAGE_HEIGHT - 80, settings.ORGANIZATION)

        canvas.setFont("FreeSans", 8)
        canvas.drawString(50, self.PAGE_HEIGHT - 95, 'Структурное подразделение:')
        canvas.drawString(200, self.PAGE_HEIGHT - 95, 'НТЦ-4')
        canvas.line(185, self.PAGE_HEIGHT - 98, 770, self.PAGE_HEIGHT - 98)

        canvas.drawString(50, self.PAGE_HEIGHT - 110, 'Материально-ответственное лицо:')
        canvas.drawString(200, self.PAGE_HEIGHT - 110, f'{self.user.last_name} {self.user.first_name}')
        canvas.line(185, self.PAGE_HEIGHT - 113, 770, self.PAGE_HEIGHT - 113)

        canvas.setFont("FreeSans", 10)
        canvas.drawCentredString(400, self.PAGE_HEIGHT - 140, "ЛИЧНАЯ КАРТОЧКА")
        canvas.drawCentredString(400, self.PAGE_HEIGHT - 155, "УЧЕТА МАТЕРИАЛЬНЫХ ЦЕННОСТЕЙ, ВЫДАННЫХ ПОЛЬЗОВАТЕЛЮ")

        canvas.setFont("FreeSans", 8)
        canvas.drawString(50, self.PAGE_HEIGHT - 180, 'Фамилия, имя, отчество')
        canvas.drawString(200, self.PAGE_HEIGHT - 180, f"{self.customer.fio()} (тел. {self.customer.telephone})")
        canvas.line(185, self.PAGE_HEIGHT - 183, 770, self.PAGE_HEIGHT - 183)

        canvas.drawString(50, self.PAGE_HEIGHT - 195, 'Должность')
        canvas.drawString(200, self.PAGE_HEIGHT - 195, self.customer.position)
        canvas.line(185, self.PAGE_HEIGHT - 198, 770, self.PAGE_HEIGHT - 198)

        canvas.drawString(50, self.PAGE_HEIGHT - 210, 'Дата поступления на работу')
        canvas.line(185, self.PAGE_HEIGHT - 213, 770, self.PAGE_HEIGHT - 213)

        canvas.drawString(50, self.PAGE_HEIGHT - 225, 'Место расположения')
        canvas.drawString(200, self.PAGE_HEIGHT - 225, self.customer.house_auditory())
        canvas.line(185, self.PAGE_HEIGHT - 228, 770, self.PAGE_HEIGHT - 228)

        canvas.restoreState()

    def vedomostHeader(self, canvas: canvas.Canvas, doc):
        canvas.saveState()
        canvas.setFont("FreeSans", 10)
        canvas.drawCentredString(300, self.PAGE_WIDTH - 50, "ВЕДОМОСТЬ МАТЕРИАЛЬНЫХ ЦЕННОСТЕЙ")
        canvas.restoreState()

