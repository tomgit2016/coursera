#!/usr/bin/env python3
import glob
from reportlab.platypus import Paragraph, Spacer, Table
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


def generate_report(attachment, title, paragraph):
    report = SimpleDocTemplate(attachment)
    styles = getSampleStyleSheet()
    report_title = Paragraph(title, styles["h1"])
    report_table = Table(data=paragraph)
    report.build([report_title, report_table])


if __name__ == "__main__":
    file = "processed.pdf"
    my_title = "Processed Update on {}".format(datetime.date(datetime.now()))
    all_items = []
    for file in glob.glob("supplier-data/descriptions/*.txt"):
        all_items.append(" ")
        description = {}
        with open(file, 'r') as f:
            lines = f.readlines()
        description["name:"] = lines[0].strip()
        description["weight:"] = lines[1].strip()
        all_items.append(description)
    print(all_items)
    generate_report(file, my_title, all_items)
