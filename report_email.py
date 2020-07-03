#!/usr/bin/env python3
import glob
import reports
from datetime import datetime

if __name__ == "__main__":
    file = "/tmp/processed.pdf"
    my_title = "Processed Update on {}".format(datetime.date(datetime.now()))
    all_items = []
    for file in glob.glob("supplier-data/descriptions/*.txt"):
        description = {}
        with open(file, 'r') as f:
            lines = f.readlines()
        description["name:"] = lines[0].strip()
        description["weight:"] = lines[1].strip()
        all_items.append(description)
        all_items.append(" ")
    print(all_items)
    reports.generate_report(file, my_title, all_items)
