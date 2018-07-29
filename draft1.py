# *********Import the file, read, split by lines
# *********Split the lines into columns, exactly one of these lists will have all of that companies corresponding answers
# ********* Do the weighting/calculations to produce the score, using indices from the list
# *********Close the evaluation csv file
# *********Open an existing csv file with company data/results, in append mode (or I guess can create a new .txt or .csv file to export to), write the company name and results to the file, close the file
# Using the new data, update variables including:
# Export all of this information to a csv file, expect just overwrite the previous file to update the results


import os


def option1():
    #Identify the desired file
    filename = input("Type the name of the file containing information on the desired vendor: ")
    while not os.path.exists(filename):
        filename = input("Wrong file name. Type the name of the file containing information on the desired vendor: ")


    # Getting the weighting values
    weighting_numbers = []
    weight_file = input("Type in the name of the file containing the weighting values: ")
    while not os.path.exists(weight_file):
        weight_file = input("Wrong file name. Type in the name of the file containing the weighting values: ")
    with open(weight_file, 'r') as infile:
        contents = infile.read().strip().split("\n")
        for line in contents:
            columns = line.split(",")
            weighting_numbers.append(columns[1])

    # Isolating the questionnaire results
    answers = []
    with open(filename, 'r') as infile:
        contents = infile.read().strip().split("\n")
        for line in contents:
            columns = line.split(",")
            answers.append(columns[1])
    del answers[0]

    # translating to numbers
    values = []
    for response in answers:
        if response == "a" or response == "A":
            values.append(1)
        if response == "b" or response == "B":
            values.append(2)
        if response == "c" or response == "C":
            values.append(3)
        if response == "d" or response == "D":
            values.append(4)

    # calculating total score
    total = 0
    if len(weighting_numbers) != len(values):
        print(
            "There is an error. Please update your file with the weighting values, so it is equal to the number of questions in your questionnairre.")
    else:
        for i in range(0, len(values)):
            total += values[i] * float(weighting_numbers[i])

        # calculating the weighted average
        nums = 0
        for j in range(0, len(weighting_numbers)):
            nums += float(weighting_numbers[j])
        weighted_average = total / nums

        with open(filename, 'r') as infile:
            header = infile.readline().strip().split(",")
            vendor = header[1]
    print("Vendor: "+ vendor)
    print("Total: " +str(total) )
    print("Weighted Average: "+ str(weighted_average))


def option2():
    #Identify the folder that you want
    filename = input("Type the name of one of the files in your desired folder: ")
    while not os.path.exists(filename):
        filename = input("Wrong file name. Type the name of one of the files in your desired folder: ")
    file_path = os.path.abspath(filename)
    folder_path = file_path.strip(filename)

    #Find all of the files in the desired folder
    dirs = os.listdir(folder_path)

    #Identify only the csv files that will be run through the program
    csv_files = []
    for obj in dirs:
        if ".csv" in obj:
            csv_files.append(obj)

    #Getting the weighting values
    weighting_numbers = []
    weight_file = input("Type in the name of the file containing the weighting values: ")
    while not os.path.exists(weight_file):
        weight_file = input("Wrong file name. Type in the name of the file containing the weighting values: ")
    with open(weight_file, 'r') as infile:
        contents = infile.read().strip().split("\n")
        for line in contents:
            if "," in line:
                columns = line.split(",")
                weighting_numbers.append(columns[1])
    if weight_file in csv_files:
        csv_files.remove(weight_file)
    set = "["
    for t in range(0, len(weighting_numbers)):
        set += "'" + str(weighting_numbers[t]) + "', "
    set = set.strip(", ")
    set += "]"

    results_file = input("Type the file name to which you want results published: ")
    while not os.path.exists(results_file):
        print("This file does not exist. What would you like to do? (Type a or b)")
        print("     a. Create a file with this name")
        print("     b. Re-type the file name")
        hmmmm = input("Answer: ")
        if hmmmm == "a":
            with open(results_file, 'w') as results:
                print("Weighting Values used for calculations:", weighting_numbers, file=results)
                print("Vendor" + "," + "total score" + "," + "weighted average", file=results)
        if hmmmm == "b":
            results_file = input("Wrong file name. Type in the name of the file to which you want results published: ")
    if results_file in csv_files:
        csv_files.remove(results_file)

    #See if weighting values have changed
    with open(results_file, 'r') as results:
        line1 = results.readline().strip()
        line_1 = line1.strip("Weighting Values used for calculations: ")
    if line_1 != set:
        print("Your weighting values have changed. All results being re-calculated.")
        with open(results_file, 'w') as results:
            print("Weighting Values used for calculations:", weighting_numbers, file=results)
            print("Vendor" + "," + "total score" + "," + "weighted average", file=results)
    #Isolating the questionnaire results
    for file in csv_files:
        answers = []
        with open (file, 'r') as infile:
            contents = infile.read().strip().split("\n")
            for line in contents:
                if "," in line:
                    columns = line.split(",")
                    answers.append(columns[1])
        del answers[0]

        #translating to numbers
        values = []
        for response in answers:
            if response == "a" or response == "A":
                values.append(1)
            if response == "b" or response == "B":
                values.append(2)
            if response == "c" or response == "C":
                values.append(3)
            if response == "d" or response == "D":
                values.append(4)

        #calculating total score
        total = 0
        if len(weighting_numbers) != len(answers):
            print("There is an error. Please update your file with the weighting values, so it is equal to the number of questions in your questionnairre.")
        else:
            for i in range(0, len(values)):
                total += values[i] * float(weighting_numbers[i])

            #calculating the weighted average
            nums = 0
            for j in range(0, len(weighting_numbers)):
                nums += float(weighting_numbers[j])
            weighted_average = total / nums

            #add this information to an existing file

            if os.path.exists(results_file):
                with open(file, 'r') as infile:
                    header = infile.readline().strip().split(",")
                    vendor = header[1]
                with open(results_file, 'r') as original_file:
                    text = original_file.read().strip()
                if vendor not in text:
                    with open(results_file, 'w') as new_file:
                        print(text, file=new_file)
                        print(vendor+","+str(total)+","+str(weighted_average), file=new_file)


print("Which would you like to do? (Type 1 or 2)")
print("     1. Access data for one vendor")
print("     2. Run program to update results for all related vendors")
choice = input("Answer: ")
if choice == "1":
    option1()
if choice == "2":
    option2()