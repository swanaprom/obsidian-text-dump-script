import os
import argparse

def has_md_files(dir_path):
    """Helper function to check if a directory or any of its subdirectories contain .md files."""
    for root, _, files in os.walk(dir_path):
        if any(f.endswith(".md") for f in files):
            return True
    return False

def process_directory(dir_path, outfile, base_vault_path):
    # Skip this entire directory tree if there are no markdown files inside
    if not has_md_files(dir_path):
        return

    # Safely get the folder name
    folder_name = os.path.basename(os.path.normpath(dir_path))
    if not folder_name:
        folder_name = "ROOT"

    # 1. START the directory
    outfile.write(f"\n\n<dir={folder_name.upper()}>\n")

    try:
        # Sort entries so files and folders process in alphabetical order
        entries = sorted(os.listdir(dir_path))
    except PermissionError:
        return

    # 2. Process all .md files in the CURRENT level first
    for entry in entries:
        full_path = os.path.join(dir_path, entry)
        if os.path.isfile(full_path) and entry.endswith(".md"):
            outfile.write(f"\n<node={entry}>\n")
            with open(full_path, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())
            outfile.write(f"\n</node={entry}>\n")

    # 3. Process all subdirectories (Nested inside the current directory)
    for entry in entries:
        full_path = os.path.join(dir_path, entry)
        if os.path.isdir(full_path):
            # Recursively call this same function for sub-folders
            process_directory(full_path, outfile, base_vault_path)

    # 4. END the directory
    outfile.write(f"\n</dir={folder_name.upper()}>\n")

if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Recursively dump an Obsidian vault into a single nested text file.")
    
    # Add arguments for directory and output name
    parser.add_argument("--dir", required=True, help="The absolute or relative path to the Obsidian vault directory.")
    parser.add_argument("--out", default="obsidian_dump", help="The desired name of the output file (without extension).")
    
    # Parse the arguments from the terminal
    args = parser.parse_args()
    
    # Ensure the output filename ends with .txt
    output_filename = args.out if args.out.endswith(".txt") else f"{args.out}.txt"
    vault_path = args.dir
    
    # Validate that the provided directory actually exists before running
    if not os.path.isdir(vault_path):
        print(f"Error: The directory '{vault_path}' does not exist.")
        exit(1)

    print(f"Starting dump of vault at: {vault_path}")
    print(f"Outputting to: {output_filename}")
    
    # Run the dump
    with open(output_filename, "w", encoding="utf-8") as outfile:
        process_directory(vault_path, outfile, vault_path)

    print("Dump complete!")
