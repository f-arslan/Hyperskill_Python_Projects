import pandas as pd
import csv
import sqlite3
import json
from collections import defaultdict
from lxml import etree
import math
from xml.etree import ElementTree


class FileOperations(object):
    def __init__(self):
        self.file_name = None
        self.excel_df_shape = None
        self.data = []
        self.header = []
        self.db_rows = []
        self.json_values = 0
        self.json_dict = defaultdict()
        self.xml_dict = defaultdict()
        self.recover = 0
        self.check = 0
        self.xml_values = 0

    def insert_record_db(self):
        self.file_name = self.file_name.replace("[CHECKED].csv", ".s3db")
        conn = sqlite3.connect(f"{self.file_name}")
        cur_conn = conn.cursor()
        cur_conn.execute(
            f"""
        CREATE TABLE IF NOT EXISTS convoy (
            {self.header[0]} INT PRIMARY KEY,
            {self.header[1]} INT NOT NULL,
            {self.header[2]} INT NOT NULL,
            {self.header[3]} INT NOT NULL);
            """
        )
        conn.commit()
        for i in self.data:
            cur_conn.execute(
                f"""INSERT INTO convoy (
                {self.header[0]}, {self.header[1]}, {self.header[2]}, {self.header[3]}) 
                VALUES ({i[0]}, {i[1]}, {i[2]}, {i[3]});
                """
            )
            conn.commit()
        result = cur_conn.execute("select * from convoy")
        self.db_rows = result.fetchall()

    def excel_csv(self):
        my_df = pd.read_excel(fr"{self.file_name}", sheet_name="Vehicles", dtype=str)
        self.file_name = self.file_name.replace(".xlsx", ".csv")
        my_df.to_csv(fr"{self.file_name}")
        self.excel_df_shape = my_df.shape[0]

    def write_to_checked_csv(self):
        with open(self.file_name, "w", encoding="utf-8") as w_file:
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\n")
            file_writer.writerow(self.header)
            for line in self.data:
                file_writer.writerow(line)

    def menu(self):
        self.file_name = input("Input file name\n")

        if self.file_name.endswith(".xlsx"):
            FileOperations.excel_csv(self)
            FileOperations.print_excel_message(self)
        # Clean and get header and data from csv and also clean [CHECKED] clause
        if self.file_name.endswith(".csv"):
            FileOperations.read_csv_file_clean(self)

        if not self.file_name.endswith("[CHECKED].csv") and not self.file_name.endswith(
            ".s3db"
        ):
            self.file_name = self.file_name.replace(".csv", "[CHECKED].csv")
            FileOperations.write_to_checked_csv(self)
            FileOperations.print_recovery(self)

        if self.file_name.endswith("[CHECKED].csv"):
            FileOperations.insert_record_db(self)
            FileOperations.print_db_results(self)
            self.check = 1

        if self.file_name.endswith(".s3db"):
            if self.check == 1:
                FileOperations.get_value_from_s3db(self)
            FileOperations.read_s3db_file_to_dict(self)
            FileOperations.write_to_json(self)
            FileOperations.print_json_results(self)
            FileOperations.write_to_xml(self)
            FileOperations.print_xml_results(self)

    def get_value_from_s3db(self):
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()
        all_rows = cur.execute("Select * from convoy").fetchall()
        cur.execute("ALTER TABLE convoy ADD score INT NOT NULL DEFAULT (0)")
        conn.commit()
        for item in all_rows:
            score = 0
            eng_cap, fuel_cons, max_load = item[1], item[2], item[3]
            total_liter = fuel_cons / 100 * 450
            score = 2 if total_liter < 230 else 1
            pit_stops = math.floor(total_liter / eng_cap)
            if pit_stops >= 2:
                score += 0
            else:
                score += 2 if pit_stops == 0 else 1
            score += 2 if max_load >= 20 else 0
            cur.execute(
                f"UPDATE convoy set score = {score} where vehicle_id = {item[0]};"
            )
            conn.commit()

    def write_to_xml(self):
        self.file_name = self.file_name.replace(".json", ".xml")
        if len(self.xml_dict) == 0:
            xml_string = "<convoy></convoy>"
            doc = etree.fromstring(xml_string)
            doc.getroottree().write_c14n(self.file_name)
            return

        xml_string = "<convoy>"
        r = 0
        for item in self.xml_dict.values():
            for k in item:
                xml_string += "<vehicle>"
                for i in k:
                    xml_string += f"<{i}>" + f"{k[i]}" + f"</{i}>"
                r += 1
                xml_string += "</vehicle>"
        xml_string += "</convoy>"
        self.xml_values = r
        root = etree.fromstring(xml_string)
        tree = etree.ElementTree(root)
        tree.write(self.file_name)

    def write_to_json(self):
        self.file_name = self.file_name.replace(".s3db", ".json")
        with open(self.file_name, "w") as json_file:
            json.dump(self.json_dict, json_file)

        values = len([i for _, v in self.json_dict.items() for i in v])
        self.json_values = values

    def read_s3db_file_to_dict(self):
        conn = sqlite3.connect(f"{self.file_name}")
        cur_conn = conn.cursor()
        query = cur_conn.execute(f"PRAGMA table_info(convoy);")
        conn.commit()
        header = [x[1] for x in query.fetchall()]
        rows = cur_conn.execute(f"SELECT * from convoy where score > 3").fetchall()
        conn.commit()
        json_dict = defaultdict(list)
        for item in rows:
            row_dict = {}
            for i in range(len(item) - 1):
                row_dict[header[i]] = item[i]
            json_dict["convoy"].append(row_dict)

        self.json_dict = json_dict

        rows = cur_conn.execute(f"SELECT * FROM convoy where score <= 3").fetchall()
        conn.commit()
        xml_dict = defaultdict(list)
        for item in rows:
            row_dict = {}
            for i in range(len(item) - 1):
                row_dict[header[i]] = item[i]
            xml_dict["convoy"].append(row_dict)

        self.xml_dict = xml_dict

    def read_csv_file_clean(self):
        if self.file_name.endswith("[CHECKED].csv"):
            with open(fr"{self.file_name}", newline="") as csv_chc_file:
                file_reader = csv.reader(csv_chc_file, delimiter=",")
                i = 0
                big_data = []
                for line in file_reader:
                    if i == 0:
                        self.header = line
                    else:
                        row = []
                        for item in line:
                            row.append(item)
                        big_data.append(row)
                    i += 1
                self.data = big_data

        else:
            with open(fr"{self.file_name}", newline="") as csv_file:
                file_reader = csv.reader(csv_file, delimiter=",")
                i = 0
                big_data = []
                check_no_digit = 0
                total_recover = 0
                for line in file_reader:
                    if len(line) == 5:
                        line = line[1:]
                    if i == 0:
                        self.header = line
                    else:
                        row = []
                        for item in line:
                            cell = ""
                            for n in item:
                                if n.isdigit():
                                    cell += n
                                else:
                                    check_no_digit = 1
                            if check_no_digit == 1:
                                total_recover += 1
                                check_no_digit = 0
                            cell = int(cell)
                            row.append(cell)
                        big_data.append(row)
                    i += 1

                self.data = big_data
                self.recover = total_recover

    def print_recovery(self):
        if self.recover == 1:
            print(f"{self.recover} cell was corrected in {self.file_name}")
        if self.recover > 1:
            print(f"{self.recover} cells were corrected in {self.file_name}")

    def print_excel_message(self):
        if self.excel_df_shape == 1:
            print(f"{self.excel_df_shape} line was imported to {self.file_name}")
        if self.excel_df_shape > 1:
            print(f"{self.excel_df_shape} lines were imported to {self.file_name}")

    def print_db_results(self):
        if len(self.db_rows) == 1:
            print(f"{len(self.db_rows)} record was inserted into {self.file_name}")
        else:
            print(f"{len(self.db_rows)} records were inserted into {self.file_name}")

    def print_json_results(self):
        if self.json_values == 1:
            print(f"{self.json_values} vehicle was saved into {self.file_name}")
        else:
            print(f"{self.json_values} vehicles were saved into {self.file_name}")

    def print_xml_results(self):
        if self.xml_values == 1:
            print(f"{self.xml_values} vehicle was saved into {self.file_name}")
        else:
            print(f"{self.xml_values} vehicles were saved into {self.file_name}")


def main():
    files = FileOperations()
    files.menu()


if __name__ == "__main__":
    main()
