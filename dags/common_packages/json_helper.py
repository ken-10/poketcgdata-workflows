import csv
import json
from pathlib import Path


def json_to_csv(output_path: Path, json_list: list, header: list = None) -> Path:
    csv_contents = []
    for json_obj in json_list:
        json_str = json.dumps(json_obj)
        csv_contents.append([json_str])
    with open(output_path, mode='w', newline='') as csv_f:
        writer = csv.writer(csv_f)
        if header is not None and len(header) > 0:
            writer.writerow(header)
        writer.writerows(csv_contents)
    return output_path
