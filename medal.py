"""
MCOMP Computer Science - Level 1
CMP1902M Programming Fundamentals: Assessment 2 (Task 1: Medals)
Author: John Brock
Student ID: 11216709
Email: 11216709@students.lincoln.ac.uk
Date submitted: 03/02/2022
"""

import csv

def radix_sort(input_list, reverse = False):
    """Performs a Radix sort algorithm on the provided list of integers.

    The Radix sorting algorithm performs a counting sort algorithm on each 
    digit of the integers, starting with units, tens, hundreds etc. 
    
    Although the counting sort is an efficient sort for smaller integers, 
    performance and memory can become inefficient when sorting larger integers. 
    Utilising the counting sort as part of a radix sort helps to counter this
    inefficiency.
    
    Args:
        input_list (list): The input list of integers to be sorted.
        reverse (bool): If set to True, the list is returned in descending order 
            (default is False which returns numbers in ascending order).

    Returns:
        A sorted list of integers.
    """

    # Check all items are integers or convertible to whole integers.
    for i, val in enumerate(input_list):
        if not isinstance(val, int):
            try:
                if int(val) == float(val):
                    input_list[i] = int(val)
                else:
                    raise TypeError
            except:
                raise TypeError("Value cannot be converted into a whole integer.")

    max_number = max(input_list)
    number_of_digits = len(str(max_number))
    
    # make all integers the same number of digits by padding with zeros.
    sortable_list = []
    for n in input_list:
        sortable_list.append(str(n).zfill(number_of_digits))
    
    for i in range(1, number_of_digits + 1):
        # Get the list of integers from the units, tens, hundreds etc.
        digits_to_sort = [int(x[-i]) for x in sortable_list]

        # Perform a counting sort on the list of integers and return a list 
        # of starting positions
        digit_places = counting_sort(digits_to_sort, True)

        temp_sortable_list = [0] * len(input_list)

        # Load values into new order based on starting positons above.
        for n in sortable_list:
            digit = int(n[-i])
            temp_sortable_list[digit_places[digit]-1] = n
            digit_places[digit] += 1
  
        sortable_list = temp_sortable_list

    # convert all values back to integers.
    sorted_list = []
    for i in sortable_list:
        sorted_list.append(int(i))

    # Reverse if needed
    # Assignment note: not using list.reverse() in case this is prohibited.
    if reverse:
        reversed_list = [0] * len(sorted_list)
        for i, val in enumerate(sorted_list, 1):
            reversed_list[-i] = val
        sorted_list = reversed_list
    
    return sorted_list

def counting_sort(input_list, return_positions = False):
    """Performs a counting sort algorithm on the provided list of integers and 
    returns these in ascending order.

    Note: The counting sort algorithm works best with small integers, for larger
    integers a different sorting algorithm is recommended.
    
    Args:
        input_list (list): The input list of integers to be sorted.
        return_positions (bool): If set to True, will return a list of the 
            starting positions for each integer instead of a sorted list 
            (default is False).

    Returns:
        A sorted list of the integers, or the starting positions for the
        integers if return_positions is set to True.
    """

    max_number = max(input_list)
    number_counts = [0] * (max_number + 1)

    cumulative_list = []
    cumulative_total = 0

    # Count the number of occurances of each integer and store in number_counts
    # at the relevant index matching the value.
    for i in input_list:
        number_counts[i] += 1

    # Work out the starting positions of each number for the sorted list.
    for count in number_counts:
        cumulative_total += count
        cumulative_list.append(cumulative_total)
    
    # Return the starting positions if return_positions is set to True.
    if return_positions:
        positions = [0] * len(cumulative_list)
        for i in range(len(cumulative_list)):
            if i > 0:
                positions[i] = cumulative_list[i - 1] + 1
            else:
                positions[i] = 1
        return positions

    # Create a list to copy the sorted values into.
    sorted_list = [0] * len(input_list)

    # Loop through the input list, copying the integers into the relevant
    # position based on the starting positions worked out above.
    for i in input_list:
        sorted_list[cumulative_list[i]-1] = i
        cumulative_list[i] -= 1

    return sorted_list

def make_sortable_numbers(input_list):
    """Combines nested lists of integers into one list that can be used to 
    compare and sort against each other, assuming each position takes
    precedence over the following positions. I.e the first positions should be
    sorted, then the second etc.
    
    E.g. if the input is [[1, 3], [1, 13], [1, 2]] then the returned list would 
    be [103, 113, 102] which can be used to sort all columns in ascending order.
    
    Args:
        input_list (list of lists): The input list containing lists of integers. 
            Each list of integers will be combined into a sort-safe integer.

    Returns:
        A single list of combined integers in the same order as passed in.
    """

    sub_list_count = len(input_list[0])

    # Check to ensure all nested lists are the same.
    for l in input_list:
        if len(l) != sub_list_count:
            raise AttributeError('Size of nested lists is not the same for every list')

    column_counts = []
    for i in range(sub_list_count):
        col = [len(str(x[i])) for x in input_list]
        column_counts.append(max(col))

    output_list = []
    for l in input_list:
        row_number = ''
        for i, val in enumerate(l):
            row_number += str(val).zfill(column_counts[i])
        
        output_list.append(row_number)

    return output_list

def rank_team(filename):
    """Ranks the medals table in filename and then writes a new file.

    Args:
        filename (str): Filename of the file to read in and process.
    """

    medals = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file)
        for row in csv_file:
            typed_row = []
            for col in row:
                try:
                    typed_row.append(int(col))
                except:
                    typed_row.append(col)
            medals.append(typed_row)

    csv_headers = medals.pop(0)

    medals_only_list = []
    for l in medals:
        medals_only_list.append(l[1:])

    # Combine medals together into one integer that can be sorted.
    combined_medals = make_sortable_numbers(medals_only_list)

    # Append the combined medals integer to the related lists.
    for i, combined_medal in enumerate(combined_medals):
        medals[i].append(combined_medal)

    # Perform a Radix sort on the combined medal integer. 
    medal_order = radix_sort([x[4] for x in medals], True)

    # Copy the medals rows into the correct sorted positon.
    sorted_medals = [0] * len(medals)
    for medal in medals:
        position = medal_order.index(int(medal[4]))
        medal.pop(4) # Removes combined integer used for sorting.
        sorted_medals[position] = medal

    # Write sorted table back to CSV.
    with open('medal_table.csv', 'w') as file:
        csv_file = csv.writer(file)
        csv_file.writerow(csv_headers)
        csv_file.writerows(sorted_medals)

# Program main --- Do not change the code below but feel free to comment out 
# Calling Task 1 function

rank_team('medal.csv')
