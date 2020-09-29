from pathlib import Path
import os

def error():
	'''Prints ERROR when called'''
	print('ERROR')

r_files = [] # initializes list that will store files from subdirectories
def compile_files(letter: str, p: Path, files: [Path]) -> Path:
    '''Compile files into a list according to first input from user. 
    If R, files from subdirectories will be contained in a different list.
    Returns tuple of two lists containing files.'''
    directories = []
    for file in p.iterdir():
        if file.is_dir():
            if letter == 'R':
                directories.append(file)
        else:
            files.append(file)
    if letter == 'R':
        for file in directories:
            #r_files will contain files from subdirectories
            compile_files(letter, file, r_files)
    return files, r_files


def print_files(files: [Path], r_files: [Path]):
    '''Sorts each list of files, adds them together, and prints each file from compiled list.'''
    files.sort()
    r_files.sort()

    sorted_files = []
    sorted_files = files + r_files

    for x in sorted_files:
        print(str(x))

def narrow_search(search_letter: str, name: str, files: [Path]) -> Path:
    '''Takes certain files from the list printed previously that fit specific characteristics
    and stores them in a new list, called interesting_files'''
    interesting_files = []
    if search_letter == 'A': #all files considered interesting
        interesting_files = files
    elif search_letter == 'N': #file name matches user input
        for file in files:
            if file.name == name:
                interesting_files.append(file)
    elif search_letter == 'E': #file extension matches user input
        if '.' in name:
            name = name [1:]
        for file in files:
            if file.suffix.split('.')[-1] == name:
                interesting_files.append(file)
    elif search_letter == 'T': #text in file contains user input
        for file in files:
            try:
                line = file.read_text()
                if name in line:
                    interesting_files.append(str(file))
                    continue
            except ValueError: #error appears when trying to read a text file on a file that isn't
                continue
    elif search_letter == '<': #size of file is less than or equal to user input
        byte_size = int(name)
        for file in files:
            if file.stat().st_size <= byte_size:
                interesting_files.append(file)
    elif search_letter == '>': #size of file is greater than or equal to user input
        byte_size = int(name)
        for file in files:
            if file.stat().st_size >= byte_size:
                interesting_files.append(str(file))

    return interesting_files

def taking_action(action_letter: str, interesting_files: [Path]):
    '''Performs actions on files from interesting_files list'''
    if action_letter == 'F': #reads first line of text file; if not a text file, prints NOT TEXT
        for file in interesting_files:
            try:
                with Path(file).open() as r:
                    x = r.readline()
                    print(x, end = '')
            except:
                print('NOT TEXT')
    elif action_letter == 'D': #duplicates file
        for file in interesting_files:
            duplicate_file = file.parent / Path(file.name + '.dup')
            if file.suffix.split('.')[-1] == 'txt':
                duplicate_file.write_text(Path(file).read_text()) #text files
            else:
                duplicate_file.write_bytes(Path(file).read_bytes()) #non text files
    elif action_letter == 'T': #changes timestamp of file to current time and date
        for file in interesting_files:
            stamped_file = Path(file).open('w')
            stamped_file.write('')
            stamped_file.close()

def execute_program():
    '''Consists of three sets of user input that dictate how and which files are 
    printed, stored, and taken action on'''
    #PART 1: Take D or R and the path of a directory, then print out files depending on letter
    while True: #continue to take user input until no errors
        user_input_one = input()
        letter = user_input_one[0:1]
        p = Path(user_input_one[2:])
        if user_input_one[1] != ' ':
        	error()
        	continue
        elif letter != 'D' and letter != 'R' or p.is_dir() == False:
            error()
            continue
        break
    files = []
    f = compile_files(letter, p, files)
    files = f[0] #first list in returned tuple
    r_files = f[1] #second list in returned tuple
    print_files(files, r_files)

    #PART 2: Take a letter that determines the characteristics of files to be stored
    while True: 
        user_input_two = input()
        search_letter = user_input_two[0:1]
        name = user_input_two[2:]
        if search_letter == 'A':
            if len(name) != 0:
                error()
                continue
        elif search_letter == 'N' or search_letter == 'E' or search_letter == 'T':
            if len(name) == 0:
                error()
                continue
            elif user_input_two[1] != ' ':
            	error()
            	continue
        elif search_letter == '>' or search_letter == '<':
            if not name.isdigit():
                error()
                continue
            elif user_input_two[1] != ' ':
            	error()
            	continue
        else:
            error()
            continue
        break
    interesting_files = narrow_search(search_letter, name, files)
    #perform same function on files from subdirectories
    interesting_r_files = narrow_search(search_letter, name, r_files)
    if (len(interesting_files) == 0) and (len(interesting_r_files) == 0):
        quit()
    print_files(interesting_files, interesting_r_files)

    #PART 3: Take a letter that determines the action to be taken on the file
    while True:
        user_input_three = input()
        action_letter = user_input_three.strip()
        if len(user_input_three) != 1 or action_letter != 'F' and action_letter != 'D' and action_letter != 'T':
            error()
            continue
        break
    taking_action(action_letter, interesting_files)
    #perform same function on files from subdirectories
    taking_action(action_letter, interesting_r_files)

    #End program
    quit()


    
if __name__ == '__main__':
    execute_program()
