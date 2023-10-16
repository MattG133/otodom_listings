import pandas as pd
import re
from datetime import datetime, timedelta

"""
Data Cleaning Script
This script reads data from CSV files, performs various data cleaning operations, and saves the cleaned data to a new CSV file.

Functions:
- join_el(link): Concatenates a URL prefix with a provided relative path.
- extract_if(string): Returns 'empty' for strings with a length of 4, or the first character otherwise.
- insert_to_list(ad_list): Inserts 'no info' elements at the beginning of a list if the length is less than 5.
- convert_to_integer(s): Attempts to convert a value to an integer after removing non-numeric characters.

Actions:
1. Read data from CSV files into DataFrames.
2. Modify the 'link1' column to match the 'link2' column for merging.
3. Merge two DataFrames based on matching columns.
4. Remove fully null columns.
5. Fill remaining null values with 'no data'.
6. Split and align the 'address' column.
7. Convert 'price' and 'rooms_No' columns to integers.
8. Clean the 'floor' column, converting it into 'floor' and 'building_floors' columns.
9. Delete unnecessary columns.
10. Save the cleaned data to a new CSV file.

Note: Make sure to specify the paths for 'LISTINGS_PATH' and 'ITEM_PATH' to your data files.
"""

LISTINGS_PATH = '/Users/Maciek/Desktop/Mieszkania/scrape_listings/otodom_listings/scrape_listings/data/raw/listings_page.csv'
ITEM_PATH = '/Users/Maciek/Desktop/Mieszkania/scrape_listings/otodom_listings/scrape_listings/data/raw/listings_item.csv'

####
#FUNCTIONS

def join_el(link):
    """
    Concatenates the input 'link' with a fixed URL prefix.
    
    Parameters:
        link (str): The relative path or a part of the URL to join with the prefix.
        
    Returns:
        str: The complete URL formed by joining 'link' and the prefix.
    """
    return ''.join(['https://www.otodom.pl', link])

def extract_if(string):
    """
    Checks the length of the input 'string' and returns 'empty' if it has a length of 4;
    otherwise, it returns the first character of the string.
    
    Parameters:
        string (str): The string to process.
        
    Returns:
        str: 'empty' if the length of the input string is 4; otherwise, the first character of the string.
    """
    if len(string) == 4:
        return 'empty'
    else:
        return string[0]
    
def insert_to_list(ad_list):
    """
    Inserts 'no info' elements at the beginning of a list if the list's length is less than 5.
    The number of 'no info' elements inserted is calculated based on the modulo operation (5 % len(ad_list)).
    
    Parameters:
        ad_list (list): The list to which 'no info' elements may be added at the beginning.
        
    Returns:
        list: A new list with 'no info' elements inserted at the beginning, or the original list
        if its length is 5 or greater.
    """
    if len(ad_list) < 5:
        i = 5%len(ad_list)
        return i * ['no info'] + ad_list
    else:
        return ad_list
    

def convert_to_integer(s):
    """
    Attempts to convert the input 's' to an integer. If 's' is a string, it removes non-numeric
    characters and returns the integer value. If 's' is not a string, it returns the value as-is
    (or handles it differently depending on the type).
    
    Parameters:
        s (str or any): The value to convert to an integer or handle differently.
        
    Returns:
        int or any: An integer if 's' can be converted to one after removing non-numeric characters.
        If not, it returns the original value (or handles it differently).
    """
    if isinstance(s, str):
        # Remove non-numeric characters
        numeric_str = ''.join(filter(str.isdigit, s))
        # Check for empty strings
        if numeric_str:
            return int(numeric_str)
        else:
            return 'N/A'
    # If the value is not a string, return it as is (or handle it differently)
    return s

def convert_to_float(s):
    '''
    Converts object to float. The function removes non-numeric charaters by using this regex: r'\b\d+(?:\.\d+)?\b'
    '''
    s = s.replace(',', '.').replace(' ', '')
    numeric_str = ''.join(re.findall(r'\b\d+(?:\.\d+)?\b', s))
    if numeric_str:
        return float(numeric_str)
    else:
        return 'N/A'

####
#ACTIONS

# read data
df_page = pd.read_csv(LISTINGS_PATH)
df_item = pd.read_csv(ITEM_PATH)

# change link1 column so it matches link2
df_page['link1'] = df_page['link1'].apply(join_el)

# merge two dfs together
df_full = df_page.merge(df_item, left_on='link1', right_on='link2', how='left')

# check for fully null columns
null_cols = df_full.columns[df_full.isnull().all()]
# delete the fully null columns
df_full = df_full.drop(null_cols, axis=1)

# fill remaining nulls with string 'no data'
df_full = df_full.fillna('no data')

# convert address col to list and align the objects in columns
df_full['address'] = df_full['address'].str.split(",")
df_full['address'] = df_full['address'].apply(insert_to_list)

# split address col to separate col for each object
address = pd.DataFrame(df_full['address'].to_list(), columns=['street', 'nbrhood', 'district', 'city', 'vvdship'] + (df_full['address'].apply(len).max()-5)*['i'])
df_full = df_full.merge(address[['street', 'nbrhood', 'district', 'city', 'vvdship']], left_index=True, right_index=True)

# convert 'price', 'area' column to integer
df_full['price'] = df_full['price'].apply(convert_to_float)

# convert rooms_No column to integer
df_full['rooms_No'] = df_full['rooms_No'].apply(convert_to_integer)
df_full['district'] = df_full['district'].str.strip()
df_full['nbrhood'] = df_full['nbrhood'].str.strip()

# clean floor column
df_full['floor'] = (df_full['floor']
                     .str.replace('parter', '0')
                     .str.replace('suterena', '-1')
                     .str.split('/')
)
floors = pd.DataFrame(df_full['floor'].to_list(), columns=['floor', 'building_floors']+(df_full['floor'].apply(len).max() - 2)*['i'])[['floor', 'building_floors']]
df_full.merge(floors, left_index=True, right_index=True)

# convert area column to float
df_full['area'] = df_full['area'].str.replace(',', '.').apply(convert_to_float)

# add timestamp of scraping
df_full['timestamp'] = datetime.now()

# delete unnecessary columns
df_full = df_full.drop(['address', 'floor'], axis=1)

# save clean file to new dir
df_full.to_csv('../scrape_listings/data/clean/listings_clean_{}.csv'.format(df_full['timestamp'].dt.strftime('%Y-%m-%d')[0]), index=False)





