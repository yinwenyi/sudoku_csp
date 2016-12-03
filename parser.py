import itertools
import glob, os
import pickle

directory = 'C:/Users/wenyi/Dropbox/Year 4/CSC384/CSC384Project/'

# The examples are in a text file with 81 characters per line
# blank spaces are represented by periods

def parse_example_file(file):
    '''
    A function for parsing one example file. Returns a list of lists in the following format:
    [[],[],[],[],...]
    where there are 9 nested lists inside the main list, each representing a row
    and each entry in the row list corresponding to a column.
    Blanks are represented by zeros.
    This function writes to a pickle file named <example>_parsed
    :param file: name of file, a string
    :return: None

    '''
    example_dict = {}
    key = 0

    with open(file) as f:
        lines = f.readlines()
    for line in lines:
        # invalid line, skip over this one
        if len(line) < 3:
            continue
        # grab string 9 chars at a time
        index = 1
        array_list = []
        while index < 10:
            num_list = []
            slice = line[(index-1)*9:index*9]  # second index is non-inclusive
            for character in slice:
                if character != ".":
                    num = int(character)
                else:
                    num = 0      # blanks are represented by zeros
                num_list.append(num)
            array_list.append(num_list)
            index = index + 1
        # add this example to the dict
        example_dict[key] = array_list
        key = key + 1

    outname = directory + file.split('.txt')[0] + "_parsed.pkl"
    os.remove(outname)
    output = open(outname, 'wb')
    # write the dict to pickle file
    pickle.dump(example_dict, output)
    output.close()


def parse_example_files(dir):
    '''
    The main function for parsing all text files.
    :param dir: a string with the absolute path of the directory containing examples
    :return: None
    '''
    # get all example files, stored in .txt format
    file_list = []
    os.chdir(dir)
    for file in glob.glob("*.txt"):
        file_list.append(file)

    for file in file_list:
        parse_example_file(file)

    return

if __name__ == "__main__":
    parse_example_files(directory)