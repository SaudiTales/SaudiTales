import sys
import csv
import os
import django

# Prepared Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import Landmark

csv_path = os.path.join(os.path.dirname(__file__), "dataset", "Landmarks_table.csv")

# This is to upload the data without handling updates (this may cause duplicates if run multiple times):
with open(csv_path, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        Landmark.objects.create(
            Destination=row["Destination"],
            Landmark_Name=row["Landmark_Name"],
            Description=row["Description"],
            Image_Url=row["Image_Url"]
        )

print("Landmarks uploaded successfully!")
