# IMPORT modules
import csv
import sys
import os
from uszipcode import SearchEngine
search = SearchEngine(simple_zipcode=True)                 # set simple_zipcode=False to use rich info database

def main():
    NewWD = ('C:\OPTMODELS\ZIPGEO\data')   # Setting the directory we need to use
    InputFileName = ('AnyData.csv')                    # Default the name of the input file
    OutputFileName = ('C:\OPTMODELS\ZIPGEO\output\DOM_AnyData_byLIST.csv')                       # Default the name of the output file
    try:     # Changing the working directory, then checking the exception codes
        os.chdir(NewWD)        
    except: 
        print('exception on os. chdir command.')
        print(f'unknown error: {sys.exc_info()[1]}')
    else: 
        print('directory was changed to ', NewWD)
        cwd = os.getcwd()  # Getting the updated current working directory in field to print confirmation that it changed ****(necessary? logging?)******
        print("Current working directory is:", cwd)
        inputfile_obj = open(InputFileName, 'rt')       # opening input file in the cwd; r = read mode, t = text data 
        outputfile_obj = open(OutputFileName, 'w+', newline ='')

        InputList = []              # Storage of the input data
        ListofFields = []           # Storage of the data derived by the program
        ListLineCount = 0
        with open(InputFileName, 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                InputList.append(line)                     # Append line to the list holding the data
                NewZipValue = InputList[ListLineCount][4]  # store the zip (5th element) in single temp field/variable
                NewZipValue = NewZipValue.ljust(4, '0')  # Left justify, pad to 4 digits with 0 if needed
                NewZipValue = NewZipValue.ljust(5, '1')  # Left justify, pad to 5 digits with 1 if needed
                result = search.by_zipcode(NewZipValue)
                if result:                      # Found match on 5 digit Zipcode, 
                    longitude = result.lng         
                    latitude =  result.lat         
                    city = result.city
                    status = "FROM_ZIP5_VIA_PY_uszipcode"
                else:
                    if ListLineCount == 0:      # First row of List: Write headings of new fields (could be improved)
                        NewZipValue = "GeoZip"
                        longitude = "Longitude"
                        latitude = "Latitude"
                        city = "City"
                        status = "Status"
                    else:
                        longitude = "Not Found"
                        latitude = "Not Found"
                        city = "Not Found"
                        status = "Not Found"

#  Append the additional fields to a single list (ListofFields), then combine (extend) the InputList    
#  before writing to the output time  [Extend only allows one arguement, hence intermediate list]
                ListofFields.append([NewZipValue, latitude, longitude, city, status])   # NOTE the arrangement of ([ ]) - this made it work
                InputList[ListLineCount].extend(ListofFields[ListLineCount])  # Extend the 2nd level nested list at record counter
                ListLineCount = ListLineCount + 1
        with outputfile_obj:
            write = csv.writer(outputfile_obj)
            write.writerows(InputList)
        print("All Done...Check files")         
        
if __name__ == '__main__': main()
