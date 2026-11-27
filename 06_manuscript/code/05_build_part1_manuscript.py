"""Assemble Part 1 with the repository Methods, Results and Figure 1."""
import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

HERE = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
CITATIONS = re.compile(r"(\[\d+(?:,\d+)*\])")


def add_body(document, text):
    for group in text.strip().split("\n\n"):
        group = group.strip()
        if not group:
            continue
        if group.startswith("## "):
            document.add_heading(group.removeprefix("## "), 2)
        else:
            paragraph = document.add_paragraph()
            for part in CITATIONS.split(LINK.sub(r"\1", group)):
                run = paragraph.add_run(part.strip("[]") if CITATIONS.fullmatch(part) else part)
                if CITATIONS.fullmatch(part):
                    run.font.superscript = True


def main():
    source = (HERE / "04_part1_manuscript_sections.md").read_text(encoding="utf-8-sig")
    title = source.splitlines()[0].removeprefix("# ")
    sections = dict(re.findall(r"^## ([^\n]+)\n(.*?)(?=^## |\Z)", source, flags=re.M | re.S))
    document = Document()
    for name, size in (("Normal", 11), ("Title", 18), ("Heading 1", 14), ("Heading 2", 11)):
        style = document.styles[name]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor(0, 0, 0)
    normal = document.styles["Normal"]
    normal.paragraph_format.line_spacing = 1.13
    normal.paragraph_format.space_after = Pt(7)
    document.add_paragraph(title, style="Title")
    for name in ("Abstract", "Introduction", "Results", "Discussion", "Methods",
                 "Data availability", "Code availability", "References"):
        document.add_heading(name, 1)
        if name in sections:
            add_body(document, sections[name])
        else:
            path = HERE / ("01_methods_working.md" if name == "Methods" else "result/02_results_working.md")
            text = path.read_text(encoding="utf-8-sig").partition("\n")[2]
            add_body(document, text)
    document.add_page_break()
    for part in ("figure1_A.flow_chart", "figure1_B.evidence_screening_and_ranking",
                 "figure1_C.pathway_framework"):
        picture = document.add_paragraph()
        picture.alignment = WD_ALIGN_PARAGRAPH.CENTER
        picture.add_run().add_picture(str(HERE / f"result/figure/{part}.png"), width=Inches(6.5))
        document.add_page_break()
    add_body(document, sections["Figure legends"])
    document.core_properties.title = title
    document.core_properties.author = ""
    document.core_properties.subject = "Part 1 of the food-derived antioxidant study"
    document.save(HERE / "result/Manuscript_Part1_Nature_Communications.docx")


if __name__ == "__main__":
    main()
