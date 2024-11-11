import argparse


arg = argparse.ArgumentParser()
arg.add_argument("-t", "--type", required=False,
                 help="Specify the type of file to add (csv, txt, json)")
args = vars(arg.parse_args())
file_type = args.get("type", 20)

text_dir = "data/text"
csv_dir = "data/csv"
json_dir = "data/json"

if not file_type:
    print("No file type selected!")
    print("Which type of file you want to stream? \n[1] CSV\n[2] JSON\n[3] TXT")
    print("Note: \n- CSV file has 10 records\n- JSON file has 5 records\n- TXT file has 1 record")
    type_dict = {
        1: "csv",
        2: "json",
        3: "txt",
    }
    try:
        choice = int(input("Your choice: "))
        if choice not in type_dict.keys():
            print("Invalid Choice")
            exit(0)
        else:
            file_type = type_dict[choice]
    except Exception as e:
        print(f"Error selecting file type: {e}")
        exit(0)
        

print(f"File type selected: {file_type}")


