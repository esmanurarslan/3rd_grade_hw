import re

class Recording:
    def __init__(self, case_no, plaintiff, defendant):
        self.case_no = case_no
        self.plaintiff = plaintiff
        self.defendant = defendant

    def pack(self):
        return f"{self.case_no}|{self.plaintiff}|{self.defendant}\n"

def main():
    recordings = []

    #read the data from file
    with open("court-cases.txt", "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue 
            
            # Case number
            match = re.search(r"\((\d+)\)$", line)
            if not match:
                print(f"Invalid line format (missing case number): {line}")
                continue
            
            case_no = match.group(1)
            rest = line[:match.start()].strip()
            
            # split via v. or V.
            if " v. " in rest:
                plaintiff, defendant = rest.split(" v. ", 1)
            elif " V. " in rest:
                plaintiff, defendant = rest.split(" V. ", 1)
            else:
                print(f"Invalid line format (missing 'v.' or 'V.'): {line}")
                continue

            recordings.append(Recording(case_no, plaintiff.strip(), defendant.strip()))
            print(f"Matched: case_no={case_no}, plaintiff={plaintiff.strip()}, defendant={defendant.strip()}")

    # write to the file
    with open("record.dat", "w") as file:
        for recording in recordings:
            packed_data = recording.pack()
            file.write(packed_data)
            print(f"Writing to file: {packed_data.strip()}")

if __name__ == "__main__":
    main()
