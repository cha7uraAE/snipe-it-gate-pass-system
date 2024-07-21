from fpdf import FPDF
from datetime import datetime


height = 7

def create_empty_table(pdf):
    # Add the table header
    pdf.set_xy(10, 90)
    pdf.cell(10, height, txt = "No", border = 1, align = 'C')
    pdf.cell(120, height, txt = "ITEM", border = 1, align = 'C')
    pdf.cell(60, height, txt = "QUANTITY", border = 1, align = 'C')
    pdf.ln()

    # Add empty rows for the rest of the table
    for i in range(1, 16):
        pdf.cell(10, height, txt = str(i), border = 1, align = 'C')
        pdf.cell(85, height, txt = "", border = 1)
        pdf.cell(95, height, txt = "", border = 1)
        pdf.ln()

def populate_table(pdf, df):
    # Add the table header
    pdf.set_xy(10, 90)
    pdf.cell(10, height, txt = "No", border = 1, align = 'C')
    pdf.cell(120, height, txt = "ITEM", border = 1, align = 'C')
    pdf.cell(60, height, txt = "QUANTITY", border = 1, align = 'C')
    pdf.ln()

    # Populate rows with DataFrame values
    for i, row in df.iterrows():
        pdf.cell(10, height, txt = str(i + 1), border = 1, align = 'C')
        pdf.cell(120, height, txt = f"{row['item']} [Serial: {row['serial']}]", border = 1)
        pdf.cell(60, height, txt = str(row['quantity']), border = 1)
        pdf.ln()

    # Add empty rows for the rest of the table if any
    for i in range(len(df) + 1, 16):
        pdf.cell(10, height, txt = str(i), border = 1, align = 'C')
        pdf.cell(120, height, txt = "", border = 1)
        pdf.cell(60, height, txt = "", border = 1)
        pdf.ln()


def create_gate_pass(input_df):
    # Create instance of FPDF class
    pdf = FPDF()
    company_list = input_df.company.unique().tolist()
    for company in company_list:
        df = input_df[input_df['company'] == company]
        df_len = len(df)


        items_per_page = 15
        page_count = df_len//items_per_page + 1

        for i in range(page_count):
            print(i)
            df_out= df[(i)*items_per_page: (i+1)*items_per_page]
            df_out = df_out.reset_index(drop=True)

            if len(df_out)>0:

                # Add a page
                pdf.add_page()

                # Set the title and fonts
                pdf.set_font("Arial", size = 12)

                pdf.image("data/aet_bw.png", x=10, y=20, w=60)

                # Add the title
                pdf.set_xy(40, 21)
                pdf.set_font("Arial", 'B', size = 32)
                pdf.cell(200, 10, txt = "GATE PASS", ln = True, align = 'C')

                # Add the date and details
                pdf.set_xy(110, 40)
                pdf.set_font("Arial", size = 12)
                pdf.cell(200, 10, txt=f"DATE - {datetime.now().strftime('%d/%m/%Y')}", ln=True)

                # Handed over to
                pdf.set_xy(10, 70)
                if company == 'leave empty':
                    pdf.cell(200, 10, txt = "HANDED OVER TO: ____________________", ln = True)
                else:
                    pdf.cell(200, 10, txt=f"HANDED OVER TO: {company}", ln=True)

                # Populate the table
                pdf.set_font("Arial", size = 10)
                populate_table(pdf, df_out)

                pdf.set_font("Arial", size = 12)
                pdf.set_xy(10, 220)
                pdf.cell(200, 10, txt = "APPROVED BY:  ____________________", ln = True)

                pdf.set_xy(10, 240)
                pdf.cell(200, 10, txt = "TAKEN BY:          ____________________", ln = True)

                pdf.set_xy(10, 260)
                pdf.cell(200, 10, txt = "VERIFIED BY:     ____________________", ln = True)

        # # Save the populated table PDF
    populated_table_path = f'pdf_files/gate_pass_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.pdf'
    pdf.output(populated_table_path)

    return populated_table_path

    # return populated_table_path
    # pdf_buffer = BytesIO()
    # pdf.output(pdf_buffer)
    # pdf_buffer.seek(0)

    # return pdf_buffer.getvalue()