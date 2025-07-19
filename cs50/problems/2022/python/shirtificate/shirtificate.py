from fpdf import FPDF, Align

def main():
    name = input("Name: ")

    pdf = PDF()
    pdf.add_name(name)
    pdf.output("shirtificate.pdf")


class PDF(FPDF):
    def __init__(self):
        super().__init__(orientation="portrait", format="A4")
        self.add_page()
        self.set_margins(left=0, top=0, right=0)
        self.image("shirtificate.png", w=self.w - 20, x=10, y=70, keep_aspect_ratio=False)

    def header(self):
        self.set_font('helvetica', size=44, style="B")
        text = "CS50 Shirtificate"
        self.set_y(28)
        self.cell(w=self.w, text=text, align=Align.C)

    def add_name(self, name):
        self.set_font('helvetica', size=24, style="B")
        self.set_text_color(255, 255, 255)
        shirt_print = f"{name} took CS50"
        self.set_y(130)
        self.set_x(50)
        self.multi_cell(w=self.w - 100, text=shirt_print, align=Align.C)


if __name__ == "__main__":
    main()
