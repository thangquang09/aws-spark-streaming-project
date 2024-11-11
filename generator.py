import argparse
import os
import shutil
import random


arg = argparse.ArgumentParser()
arg.add_argument("-t", "--type", required=False,
                 help="Specify the type of file to add (csv, txt, json)")
args = vars(arg.parse_args())
file_type = args.get("type", 20)

directories = {
    "txt": "data/text",
    "csv": "data/csv",
    "json": "data/json",
    "test": "data/testing"
}

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

files = [f for f in os.listdir(directories['test']) if f.endswith(file_type)]
existed_files = [f for f in os.listdir(directories[file_type]) if f.endswith(file_type)]

new_files = [f for f in files if f not in existed_files]
print(f"Number of insert new file times: {len(new_files)}")

if len(new_files) <= 0:
    print(f"Out of testing data! Please chose another datatype to test or delete data from S3 bucket and {file_type} folder")
else:
    random_file = random.choice(new_files)
    source_path = os.path.join(directories['test'], random_file)
    destination_path = os.path.join(directories[file_type], random_file)

    shutil.copy(source_path, destination_path)
    print(f"Copied {random_file} to {directories[file_type]}")