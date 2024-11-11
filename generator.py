import argparse
import os
import shutil
import random


arg = argparse.ArgumentParser()
arg.add_argument("-t", "--type", required=False,
                 help="Specify the type of file to add (csv, txt, json)")
arg.add_argument("-n", "--number", required=False,
                help="Specify the number of file to add")              
args = vars(arg.parse_args())
file_type = args.get("type")
number_files = int(args.get("number")) if args.get("number") else 1

directories = {
    "txt": "data/txt",
    "csv": "data/csv",
    "json": "data/json",
    "test": "data/testing"
}

try:
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
    len_files = len(new_files)
    print(f"Number of insert new file times: {len_files}")

    if len_files <= 0:
        print(f"Out of testing data! Please chose another datatype to test or delete data from S3 bucket and {file_type} folder")
    elif number_files > len_files:
        print(f"Not enough files")
    else:
        selected_files = random.sample(new_files, int(number_files))
        for random_file in selected_files:
            source_path = os.path.join(directories['test'], random_file)
            destination_path = os.path.join(directories[file_type], random_file)

            shutil.copy(source_path, destination_path)
            print(f"Copied {random_file} to {directories[file_type]}")
        print(f"Copied {number_files} files to {directories[file_type]}")
except Exception as e:
    print(f"Error generating file: {e}")
finally:
    print("Existing...")
    exit(0)