#!/usr/bin/env python3
import os
import requests
import glob

for file in glob.glob("/data/feedback/*.txt"):
    with open(file, 'r') as f:
        content = f.readlines()
    keys = ["tile", "name", "date", "feedback"]
    body = {}
    for x in range(4):
        body[keys[x]] = content[x].strip()
    response = requests.post("http://35.223.82.144/feedback/", json=body)
    if response.status_code != 201:
        print(f"status code is {response.status_code}")
