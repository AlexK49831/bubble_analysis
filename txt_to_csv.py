## File for converting text circle and radius files into a csv file we can use.
## Goes through each line of the file and extracts each x value, y value, and radius.


### Example usage
### python txt_to_csv.py <your_dir_here>


from config import *
import os
import pandas as pd

base_dir = IMAGE_BASE_DIR # from config

def main():
    ### Varaibles within main before the loop:
    ### df - Pandas dataFrame, this is the end result of the function.
    ###      We will be exporting df back to the directory where the txt file was found
    ### f - the text file to be transposed to csv
    ### index - Keeps track of the index in the csv
    ### skip - We skip the first 7 lines of the file because they aren't useful for us.
    paths = [f for f in os.listdir(os.path.join(base_dir, args.path)) if os.path.isfile(os.path.join(base_dir, args.path, f)) and '.txt' in f]
    for path in paths:
        f = open(os.path.join(base_dir, args.path, path), 'r')
        df = pd.DataFrame(columns={'X', 'Y', 'Radius'})
        index = -1
        skip = 0
        ################## MAIN LOOP ####################
        # Inside the loop, we have variables:           #
        # count - counts the column of the txt file     #
        # tens - keeps track of the digit to transfer   #
        # prev_char - Denotes previous char as 0 (blank)#
        #      or a number (1)                          #
        # val - This is the value that goes into df     #
        # index - Placeholder for index in dataFrame    #
        #################################################
        for line in f:
            if skip < 7:
                skip += 1
                continue
            count = 0
            tens = 0
            prev_char = 0
            val = ""
            index += 1
            for char in line:
                # If we hit white space or a non-number
                if not char.isdigit():
                    tens = 0
                    # If the previous character was a digit
                    if prev_char == 1:
                        prev_char = 0
                        # The first column is the x column
                        if count == 1:
                            df.set_value(index, 'X', int(val))
                            val = ""
                        # When count is 2, that means we're at the y column    
                        elif count == 2:
                            df.set_value(index, 'Y', int(val))
                            val = ""
                        elif count == 3:
                        # When count is 3, we're at the radius column
                            df.set_value(index, 'Radius', int(val))
                            val = ""
                        count += 1
                        if count > 3:
                            # If count is more than 3, keep going through the line
                            continue
                    else:
                        continue
                    continue
                #If we get to here, that means we have found a digit
                prev_char = 1
                # The above line means the previous char was a digit

                # If we are in the index column, we don't need to touch the numbers
                if count == 0:
                    continue
                val += char
                tens += 1
            df.to_csv(os.path.join(base_dir, args.path, path[:-4])+'.csv', index=False)







if __name__ == '__main__':
    import argparse
    #Path -- a path to the directory where you have txt files
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    
    main()
