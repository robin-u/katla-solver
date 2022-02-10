import re
import sqlite3
import string

def start():
    # Make a connection + cursor to db
    conn = sqlite3.connect('limaHuruf-v2.db')
    cur = conn.cursor()

    # Asking input from user
    while True:
        print("Please input unknown character(s) as '*', '.', or any special characters as a replacement")
        hint = input("Enter the known positioned character(s): ").lower()
        if len(hint) != 5 or hint == 'quit':
            if hint == 'quit':
                exit()
            print("\nYou can only input 5 characters or input 'quit' to stop the script")
            continue
        break

    incl = input("Known character(s) but is currently misplaced: ").lower()
    incl = [incl[x] for x in range(len(incl))] # Convert the misplaced chars to a list for filtering later
    excl = input("Enter the character(s) to exclude: ").lower()
    excl = [excl[x] for x in range(len(excl))] # Convert the unused chars to a list for filtering later
    
    # Create an array to store potential words & a regex pattern
    potential = list()
    pattern = ''.join([hint[x] if hint[x].isalpha() else '.' for x in range(len(hint))])
    
    # Search for words that suit the pattern
    for row in cur.execute(''' SELECT * FROM kata'''):
        if re.search(pattern, row[0]) is not None:
            potential.append(row[0])

    # Filtering words with excluded character(s)
    filtered = list()
    for i in range(len(potential)):
        count = 0
        for j in range(len((excl))):
            if excl[j] in potential[i]:
                count += 1
        if count == 0:
            filtered.append(potential[i])
        
    # Filtered with included character(s)
    final_result = list()
    for i in range(len(filtered)):
        count = 0
        for j in range(len(incl)):
            if incl[j] in filtered[i]:
                count += 1
        if count == len(incl):
            final_result.append(filtered[i])
    
    # Non-repeating-character-based recommendation | to add more excluded words in 2nd search
    lowercase = string.ascii_lowercase
    active_lowercase = [x for x in lowercase if x not in excl and x not in hint and x not in incl]
    narrowed_recommendation = list()
    for i in range(len(final_result)):
        count = 0
        duplicate_check = set()
        for j in range(len(active_lowercase)):
            if active_lowercase[j] in final_result[i]:
                count += 1
        if count > 1:
            for k in range(len(final_result[i])):
                duplicate_check.add(final_result[i][k])
            if len(duplicate_check) == 5:
                narrowed_recommendation.append(final_result[i])

    # Print narrowed and potential words
    print('----------------------')
    if len(final_result) > 0:
        print("Total narrowed-recommended words based on non-repeating characters:", len(narrowed_recommendation))
        print(narrowed_recommendation)
        print('----------------------')
        print("Total potential words:", len(final_result))
        print(final_result)
    else:
        print("There is no matching word. Please re-check the known characters.")   
    cur.close()

if __name__ == '__main__':
    start()