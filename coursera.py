#!/usr/bin/env python3

import json
import locale
import sys
import os
import glob
import requests
from datetime import datetime

from PIL import Image
from reportlab.platypus import Image
from reportlab.platypus import Paragraph, Spacer, Table
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet

def load_data(filename):
    """Loads the contents of filename as a JSON file."""
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def format_car(car):
    """Given a car dictionary, returns a nicely formatted name."""
    return "{} {} ({})".format(
        car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
    """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
    locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
    max_revenue = {"revenue": 0}
    max_sales = {"total_sales": 0}
    max_car_year = {"max_sales": 0, "car_year": 2002}
    sum_sales = {2002: 0}
    for item in data:
        # Calculate the revenue generated by this model (price * total_sales)
        # We need to convert the price from "$1234.56" to 1234.56
        item_price = locale.atof(item["price"].strip("$"))
        item_revenue = item["total_sales"] * item_price
        if item_revenue > max_revenue["revenue"]:
            item["revenue"] = item_revenue
            max_revenue = item
        # TODO: also handle max sales
        if item["total_sales"] > max_sales["total_sales"]:
            max_sales = item
        # TODO: also handle most popular car_year
        car_year = item["car"]["car_year"]
        sum_sales[car_year] = sum_sales.get(car_year, 0) + item["total_sales"]
        if sum_sales[car_year] > max_car_year["max_sales"]:
            max_car_year["max_sales"] = sum_sales[car_year]
            max_car_year["car_year"] = car_year

    summary = [
        "The {} generated the most revenue: ${}".format(
            format_car(max_revenue["car"]), max_revenue["revenue"]),
        "{} had the most sales: {}".format(format_car(max_sales["car"]), max_sales["total_sales"]),
        "{} is most popular car_year, total sales: {}".format(max_car_year["car_year"], max_car_year["max_sales"])
    ]

    return summary


def cars_dict_to_table(car_data):
    """Turns the data in car_data into a list of lists."""
    table_data = [["ID", "Car", "Price", "Total Sales"]]
    for item in car_data:
        table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
    return table_data


def main(argv):
    for tifFile in glob.glob("supplier-data/images/*.tiff"):
        outFile = tifFile.replace(".tiff", ".jpeg")
        image = Image.open(tifFile)
        out = image.resize((600, 400)).convert("RGB")
        out.save(outFile)


def upload():
    url = "http://localhost/upload/"
    for file in glob.glob("supplier-data/images/*.jpeg"):
        with open(file, 'rb') as opened:
            r = requests.post(url, files={'file': opened})


def add_description():
    url = "http://localhost/fruits/"
    for file in glob.glob("supplier-data/descriptions/*.txt"):
        description = {}
        with open(file, 'r') as f:
            lines = f.readlines()
        description["name"] = lines[0].strip()
        description["weight"] = int(lines[1].split(' ')[0])
        description["description"] = lines[2].strip()
        description["image_name"] = file.replace("supplier-data/descriptions/", "").replace("txt", "jpeg")
        r = requests.post(url, data=description)


def generate_report(attachment, title, paragraph):
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
    report = SimpleDocTemplate("processed.pdf")
    styles = getSampleStyleSheet()
    report_title = Paragraph("Processed Update on {}".format(datetime.date(datetime.now())), styles["h1"])
    report_table = Table(data=all_items)
    report.build([report_title, report_table])


if __name__ == "__main__":
    main(sys.argv)
