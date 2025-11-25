# import re


# test_regex= r"^.*(\d{4}-\d{1,2}-\d{1,2}_to_\d{4}-\d{1,2}-\d{1,2}.*)$"

# test_file_path = "email-auto/testvg/processed/test/spatial_Monthly_Sales_Extract_All_Locations_2000-02-15_to_2000-02-19yy.csv"

# regex = re.compile(test_regex)
# print(regex)

# matches = re.match(regex, test_file_path)
# print(matches)

# if matches:
#     print(f"✅ MATCH!")
#     print(f"  Group 0 (full match): '{matches.group(0)}'")
#     print(f"  Group 1 (capture): '{matches.group(1)}'")
# else:
#     print("❌ NO MATCH")


# # python test
# paragraph = "Bob hit a ball, the hit BALL flew far after it was hit."
# a = "!?',;."
# pargragh = paragraph.replace(",", "").replace(".", "").lower()
# print(pargragh)
# banned = ["hit"]
# word_count = {}
# para = pargragh.split(" ")
# print(para)
# for i in para:
#     if i in banned:
#         word_count[i] = 0
#     else:
#         word_count[i] = word_count.get(i, 0) + 1
# print(word_count)
# sort_asc = sorted(word_count.items(), key=lambda item: item[1], reverse=True)
# sort_asc_dict = dict(sort_asc)
# print(sort_asc_dict)

# # Method 1: Get first key using next() and iter()
# first_key = next(iter(sort_asc_dict))
# print(f"First key: {first_key}")

# test pathlib module
from pathlib import Path
# current working dir
print(Path.cwd())
# check folders
for p in Path().iterdir():
    print(p)