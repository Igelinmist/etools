import io
import xlsxwriter
from datetime import date


def WriterToExcel(context):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("Отчет")
    worksheet_s.set_column('A:A', 23)
    worksheet_s.set_column('B:Z', 14)

    # excel styles
    title = workbook.add_format({
        'bold': True,
        'font_size': 16,
        'align': 'center',
        'valign': 'vcenter'
    })
    rtitle = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'left',
        'valign': 'vcenter'
    })
    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'text_wrap': True,
        'valign': 'top',
        'border': 1
    })
    cell = workbook.add_format({
        'align': 'left',
        'valign': 'top',
        'text_wrap': True,
        'border': 1
    })
    cell_center = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'border': 1
    })

    row_pointer = 2
    date_from = context['date_from'] if context['date_from'] else None
    date_to = context['date'] if context['date'] else date.today().strftime("%d.%m.%Y")
    if date_from:
        title_text = "Отчет по наработке оборудования с {} до {}".format(
            date_from, date_to)
    else:
        title_text = "Отчет по наработке оборудования на {}".format(date_to)
    worksheet_s.merge_range('A{0}:G{0}'.format(row_pointer), title_text, title)
    row_pointer += 2

    for report, rtable in context['rdata']:
        worksheet_s.merge_range('A{0}:G{0}'.format(row_pointer), report.title, rtitle)
        row_pointer += 1
        for c_idx, h_text in enumerate(rtable[0]):
            worksheet_s.write_string(row_pointer, c_idx, h_text, header)
        row_pointer += 1

        for r_idx, row in enumerate(rtable[1:]):
            worksheet_s.write_string(row_pointer, 0, row[0], cell)
            for c_idx, r_text in enumerate(row[1:]):
                worksheet_s.write_string(row_pointer, c_idx + 1, r_text, cell_center)
            row_pointer += 1
        row_pointer += 2
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data
