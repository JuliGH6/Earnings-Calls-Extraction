import os

def remove_files_with_same_prefix(folder_path):
    
    print("\n")
    # Get list of files in the folder
    files = os.listdir(folder_path)
    # Dictionary to store prefixes and corresponding files
    prefix_dict = {}
    # List to store files to be removed
    files_to_remove = []
    
    # Iterate over each file
    for file_name in files:
        # Extract the first 10 characters of the file name
        # Check if prefix already exists in dictionary
        if file_name[:-34] in prefix_dict:
            # If it exists, add the file to the list of files to be removed
            files_to_remove.append(file_name)
        else:
            # If it doesn't exist, add it to the dictionary
            prefix_dict[file_name[:-34]] = file_name
    
    # Remove the files
    for file_name in files_to_remove:
        os.remove(os.path.join(folder_path, file_name))
        print(f"File '{file_name}' deleted")


def add_line_to_files(folder_path, line_to_add):
    # Get list of files in the folder
    files = os.listdir(folder_path)
    
    print("\n")
    # Iterate over each file
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            with open(file_path, 'a') as file:
                # Add the line to the end of the file
                file.write('\n' + line_to_add)
                # print(f"Line '{line_to_add}' added to file '{file_name}'")



def main():
    # Specify the folder path
    folder_path = "./Results"

    # Specify the line to add
    line_to_add = "End of Transcript."
    
    # Call the function to remove files with the same prefix
    remove_files_with_same_prefix(folder_path)
    
    # Call the function to add line to files
    add_line_to_files(folder_path, line_to_add)

if __name__ == "__main__":
    main()