from file_handler import save_file, extract_text, list_files


USER_ID = "ishtiaq"

# এখানে তোমার test file-এর path দাও
FILE_PATH = "test.txt"


# 1. Save file
saved_path = save_file(
    FILE_PATH,
    USER_ID
)

print("\nFile saved:")
print(saved_path)


# 2. Extract text
text = extract_text(
    saved_path
)

print("\nExtracted text:")
print(text)


# 3. List saved files
print("\nSaved files:")

for file in list_files(USER_ID):
    print("-", file)
