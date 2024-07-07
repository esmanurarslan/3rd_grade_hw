import json

def build_index():
    plaintiff_index = {}
    defendant_index = {}
    case_no_index = {}
    with open("record.dat", "rb") as file:
        position = 0
        while True:
            line = file.readline()
            if not line:
                break
            line = line.decode().strip()
            parts = line.split("|")
            case_no, plaintiff, defendant = parts
            #Plaintiff indexes
            if plaintiff not in plaintiff_index:
                plaintiff_index[plaintiff] = []
            plaintiff_index[plaintiff].append(position)
            # Defendant indexes
            if defendant not in defendant_index:
                defendant_index[defendant] = []
            defendant_index[defendant].append(position)
            # Case_no indexes
            case_no_index[case_no] = position
            position = file.tell()
    
    # sort indexes
    plaintiff_index = dict(sorted(plaintiff_index.items()))
    defendant_index = dict(sorted(defendant_index.items()))
    case_no_index = dict(sorted(case_no_index.items()))
    
    return plaintiff_index, defendant_index, case_no_index

def save_index(plaintiff_index, defendant_index, case_no_index):
    with open("plaintiff_index.json", "w") as file:
        json.dump(plaintiff_index, file, indent=4)
    with open("defendant_index.json", "w") as file:
        json.dump(defendant_index, file, indent=4)
    with open("case_no_index.json", "w") as file:
        json.dump(case_no_index, file, indent=4)

def load_index():
    try:
        with open("plaintiff_index.json", "r") as file:
            plaintiff_index = json.load(file)
    except FileNotFoundError:
        plaintiff_index = {}
    try:
        with open("defendant_index.json", "r") as file:
            defendant_index = json.load(file)
    except FileNotFoundError:
        defendant_index = {}
    try:
        with open("case_no_index.json", "r") as file:
            case_no_index = json.load(file)
    except FileNotFoundError:
        case_no_index = {}
    
    return plaintiff_index, defendant_index, case_no_index

def search_record_by_plaintiff(index, plaintiff_name):
    if plaintiff_name in index:
        positions = index[plaintiff_name]
        records = []
        with open("record.dat", "rb") as file:
            for position in positions:
                file.seek(position)
                line = file.readline().decode().strip()
                records.append(line.split("|"))
        return records
    else:
        return None

def search_record_by_defendant(index, defendant_name):
    if defendant_name in index:
        positions = index[defendant_name]
        records = []
        with open("record.dat", "rb") as file:
            for position in positions:
                file.seek(position)
                line = file.readline().decode().strip()
                records.append(line.split("|"))
        return records
    else:
        return None

def search_record_by_case_no(index, case_no):
    if case_no in index:
        position = index[case_no]
        with open("record.dat", "rb") as file:
            file.seek(position)
            line = file.readline().decode().strip()
            return line.split("|")
    else:
        return None

def main():
    plaintiff_index, defendant_index, case_no_index = load_index()
    if not plaintiff_index or not defendant_index or not case_no_index:
        plaintiff_index, defendant_index, case_no_index = build_index()
        save_index(plaintiff_index, defendant_index, case_no_index)

    while True:
        print("Enter in which field you want to search:")
        print("1. Plaintiff")
        print("2. Defendant")
        print("3. Case No")
        print("Type 'exit' to stop the code from running.")
        
        search_type = input("Your choice: ").strip()
        if search_type == "exit":
            break
        
        search_key = input("Value to seek: ").strip()

        if search_type == "1":
            found_records = search_record_by_plaintiff(plaintiff_index, search_key)
        elif search_type == "2":
            found_records = search_record_by_defendant(defendant_index, search_key)
        elif search_type == "3":
            found_record = search_record_by_case_no(case_no_index, search_key)
            if found_record:
                print("Founded records:")
                print(f"caseNo: {found_record[0]}")
                print(f"plaintiff: {found_record[1]}")
                print(f"defendant: {found_record[2]}")
               
            else:
                print("No found any record.")
            continue
        else:
            print("unsuitable research.")
            continue

        if found_records:
            print("Founded records:")
            for record in found_records:
                print(f"caseNo: {record[0]}")
                print(f"plaintiff: {record[1]}")
                print(f"defendant: {record[2]}")
                print(f"-------------------------------")
        else:
            print("No found any record.")

if __name__ == "__main__":
    main()