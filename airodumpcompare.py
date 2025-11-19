#!/usr/bin/python
import sys, os, csv

def delete_first_rows(input_path, output_path):
    if not os.path.isfile(input_file):
        print(f'Error: File {file_path} does not exist.')
        return

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = f.read()

        parts = data.split('\n\n', 1)

        trimmed = parts[1] if len(parts) > 1 else data

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(trimmed)
        else:
            print(trimmed)

    except Exception as e:
        print(f'An error occurred: {e}')

def remove_empty(input_file):
    with open(input_file, 'r', encoding='utf-8') as r:
        lines = r.readlines()

    full_lines = [line for line in lines if line.strip() != '']

    with open(input_file, 'w', encoding='utf-8') as w:
        w.writelines(full_lines)

    print(f'Empty lines removed from {input_file}')

def compare(file1, file2, unk):
    company_dict = {}

    with open(file2, mode='r', encoding='utf-8') as f2:
        reader2 = csv.reader(f2)
        next(reader2, None)
        for row in reader2:
            mac_prefix = row[0][:8].upper()
            company_name = row[1]
            company_dict[mac_prefix] = company_name
    
    with open(file1, mode='r', encoding='utf-8') as f1:
        reader1 = csv.reader(f1)
        next(reader1, None)
        for row in reader1:
            mac_address = row[0].upper()
            mac_prefix = mac_address[:8]
            
            try:
                company = company_dict[mac_prefix]
                print(f'{mac_address} {company}')
            except:
                if unk == True:
                    company = "UNKOWN"
                    print(f'{mac_address} {company}')
                elif unk == False:
                    pass

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
           print("-----------------------------------------")
           print("airodumpcompare.py - airodump csv mac address processor")
           print("Author - Cpl Connor Knight")
           print("-----------------------------------------")
           print("Example:")
           print("compareMAC.py <inputfile> <options>")
           print("-----------------------------------------")
           print("<inputfile>       filepath for airodump-ng csv file")
           print("-h OR --help      this menu")
           print("-u                show UNKNOWN mac addresses")
           print("-----------------------------------------")
           sys.exit(1)

    input_file = sys.argv[1]
    args = sys.argv[1:]
    for arg in args:
        if arg == "-u":
            unk = True
        else:
            unk = False

    delete_first_rows(input_file, "TEMP.csv")
    remove_empty("TEMP.csv")
    compare("TEMP.csv", "mac-vendors-export.csv", unk)
    os.remove("TEMP.csv")
