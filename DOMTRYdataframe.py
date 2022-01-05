# IMPORT modules
import sys
import os
import pandas as pd
from uszipcode import SearchEngine
search = SearchEngine(simple_zipcode=True)                 # set simple_zipcode=False to use rich info database
def main():
    NewWD = ('C:\OPTMODELS\ZIPGEO\data')   # Setting the directory we need to use
    InputFileName = ('AnyData.csv')                    # Default the name of the input file
    OutputFileName = ('DOM_AnyData.csv')                       # Default the name of the output file
    
    try:     # Changing the working directory, then checking the exception codes
        os.chdir(NewWD)        
    except: 
        print('exception on os. chdir command.')
        print(f'unknown error: {sys.exc_info()[1]}')
    else: 
        print('directory was changed to ', NewWD)
        inputfile_obj = open(InputFileName, 'rt')       # opening input file in the cwd; r = read mode, t = text data
        anydata = pd.read_csv(InputFileName)            # Loading the input file to dataframe
        anydata['newzip'] = anydata['zip'].str[:5]      # add field newzip in the dataframe, value is left 5 characters of the zip
                                                        # field...
        anydata['newzip'] = anydata['newzip'].str.pad(width=4, side='right', fillchar='0')    # pad '0' on end if needed
        anydata['newzip'] = anydata['newzip'].str.pad(width=5, side='right', fillchar='1')    # pad '1' on end if needed
        anydata.assign(ADLat = "", ADLong = "", ADNewCity = "", ADStat = "") # Add empty columns to anydata dataframe
        print("Length of anydata is:",len(anydata))
        ZCount = len(anydata)           # Set ZCount to the number of rows in the anydata dataframe
        for row in range(0, ZCount):    # controlling number of iterations of logic based on rows in anydata dataframe
            result = search.by_zipcode(anydata['newzip'].iloc[row]) 
            if result:                                              # Found match on 5 digit Zipcode
                anydata.loc[row, 'ADLong'] = result.lng        
                anydata.loc[row, 'ADLat'] = result.lat        
                anydata.loc[row, 'ADNewCity'] = result.city
                anydata.loc[row, 'ADStat'] = "FROM_ZIP5_VIA_PY_uszipcode"
            else:                                                   # no match on 5 digit Zipcode
                anydata.loc[row, 'ADLong'] = "Not Found"      
                anydata.loc[row, 'ADLat'] = "Not Found"       
                anydata.loc[row, 'ADNewCity'] = "Not Found"
                anydata.loc[row, 'ADStat'] = "Not Found"

        NewWD = ('C:\OPTMODELS\ZIPGEO\output')  # Setting the directory we need to use
        os.chdir(NewWD)
        anydata.to_csv(OutputFileName)      # Writing the dataframe to the output file
        print("All Done...Check files") 
        
if __name__ == '__main__': main()
