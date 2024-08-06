import copy
import datetime
import os
from io import BytesIO

from docxtpl import DocxTemplate
from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def generate_plan(
        stages,
        data,
        output_path = os.getcwd() + "/templates/file/output.docx",
        template_path = os.getcwd() + "/templates/file/plan_word.docx",
        add_template_path = os.getcwd()  + "/templates/file/add_plan_word.docx",
):
    def set_cell_border(cell, **kwargs):
        """
        Set cell`s border
        Usage:
            set_cell_border(
                cell,
                top={"sz": 12, "color": "#FF0000", "val": "single"},
                bottom={"sz": 12, "color": "#00FF00", "val": "single"},
                start={"sz": 24, "color": "#0000FF", "val": "dashed"},
                end={"sz": 24, "color": "#FF00FF", "val": "dashed"},
            )
        """
        tc = cell._element
        tcPr = tc.get_or_add_tcPr()

        for edge in ('top', 'bottom', 'start', 'end'):
            edge_data = kwargs.get(edge)
            if edge_data:
                tag = f'w:{edge}'
                element = tcPr.find(qn(tag))
                if element is None:
                    element = OxmlElement(tag)
                    tcPr.append(element)

                for key in ["sz", "val", "color", "space"]:
                    if key in edge_data:
                        element.set(qn(f'w:{key}'), str(edge_data[key]))

    # Функция для создания таблицы
    def create_table(doc, items):
        table = doc.add_table(rows=1, cols=5)
        hdr_cells = table.rows[0].cells
        headers = ['№', 'Услуга', 'Цена за ед.', 'Кол-во', 'Всего']

        # Устанавливаем стили для заголовков таблицы
        for i, header in enumerate(headers):
            cell = hdr_cells[i]
            run = cell.paragraphs[0].add_run(header)
            run.bold = True
            run.font.size = Pt(14)  # Размер шрифта 15 пунктов

            # Добавляем границы
            set_cell_border(cell, top={"sz": 12, "val": "single", "color": "000000"},
                            bottom={"sz": 12, "val": "single", "color": "000000"},
                            start={"sz": 12, "val": "single", "color": "000000"},
                            end={"sz": 12, "val": "single", "color": "000000"})

        for item in items:
            row_cells = table.add_row().cells
            row_cells[0].text = str(item['no'])
            row_cells[1].text = item['service']
            row_cells[2].text = item['price_per_unit']
            row_cells[3].text = str(item['quantity'])
            row_cells[4].text = item['total']
            for cell in row_cells:
                # Установка размера шрифта для текста в ячейке
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(14)  # Размер шрифта 15 пунктов

                # Добавляем границы
                set_cell_border(cell, top={"sz": 12, "val": "single", "color": "000000"},
                                bottom={"sz": 12, "val": "single", "color": "000000"},
                                start={"sz": 12, "val": "single", "color": "000000"},
                                end={"sz": 12, "val": "single", "color": "000000"})

    doc = DocxTemplate(template_path)
    doc.render(data)
    doc.save(output_path)
    document = Document(output_path)

    for stage in stages:
        title = document.add_paragraph()
        ts = title.add_run(f"Этап №{stage['number']} – {stage['stage']}")
        ts.font.size = Pt(14)
        create_table(document, stage['items'])
        document.add_paragraph()  # Добавляем пустую строку между этапами
    doc_end = Document(add_template_path)

    # Сохраняем результирующий документ
    document.save(output_path)
    # Создаем буфер для записи нового документа
    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)

    # Считываем новый документ и заполненный шаблон
    new_doc_from_buffer = Document(buffer)

    # Переносим содержимое заполненного шаблона в новый документ с сохранением стилей
    for element in doc_end.element.body:
        new_doc_from_buffer.element.body.append(element)

    # Сохраняем результирующий документ
    new_doc_from_buffer.save(output_path)

stages = [
    {
        "number": 1,
        "stage": "Подготовка",
        "items": [
            {"no": 1, "service": "Услуга 1", "price_per_unit": "100", "quantity": 2, "total": "200"},
            {"no": 2, "service": "Услуга 2", "price_per_unit": "150", "quantity": 1, "total": "150"},
        ]
    },
    {
        "number": 2,
        "stage": "Реализация",
        "items": [
            {"no": 1, "service": "Услуга 3", "price_per_unit": "200", "quantity": 3, "total": "600"},
            {"no": 2, "service": "Услуга 4", "price_per_unit": "250", "quantity": 2, "total": "500"},
        ]
    }
]

# Открываем шаблон
data = {
        "fio": 1,
        "birthday": "Подготовка",
        "data_day": datetime.datetime.now().strftime("%d.%m.%Y")
    }

generate_plan(stages,data)