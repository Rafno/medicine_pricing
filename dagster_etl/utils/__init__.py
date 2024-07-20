from datetime import datetime
import re

# Helper function to convert Icelandic month names to English month names
def icelandic_month_to_english(month_name):
    months = {
        "januar": "January",
        "februar": "February",
        "mars": "March",
        "april": "April",
        "mai": "May",
        "juni": "June",
        "juli": "July",
        "agust": "August",
        "september": "September",
        "oktober": "October",
        "november": "November",
        "desember": "December"
    }
    return months.get(month_name.lower(), month_name)

def extract_date_from_filename(filename):
    '''
    The files come in any variety of formatting. 
    These helper functions extract the date so we can actually filter based on when the report was updated.
    '''
    # Define regex patterns for different date formats
    patterns = [
        r'(\d{8})',  # YYYYMMDD
        r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
        r'(\d{2}-\d{2}-\d{4})',  # DD-MM-YYYY
        r'(\d{4}-\d{2})',  # YYYY-MM
        r'(\d{2}-\d{4})',  # MM-YYYY
        r'(\d{1,2}[^\d]+\w+[^\d]+\d{4})',  # D-month-YYYY
        r'(\d{2}-\d{2})',  # MM-YY or DD-MM
        r'(\d{2}-\d{4})',  # MM-YYYY
        r'(\d{7})',  # DMMYYYY
        r'lyfjaverdskra-(\d{2})-(\d{4})\.xls',  # MM-YYYY specific format
        r'lyfjaverdskra-(\d{2})(\d{4})\.xls'  # MMYYYY specific format
    ]
    
        # Handle specific cases for when the file did not give enough information
    if filename == 'lyfjaverdskra-132022.xls':
        return datetime.strptime('2022-04-13', '%Y-%m-%d').date()

    elif filename == 'lyfjaverdskra-142022.xls':
        return datetime.strptime('2022-04-14', '%Y-%m-%d').date()

    elif filename == 'lyfjaverdskra-15-februar.xls':
        return datetime.strptime('2022-02-15', '%Y-%m-%d').date()

    elif filename == 'lyfjaverdskra-15-januar.xls':
        return datetime.strptime('2022-01-15', '%Y-%m-%d').date()

    elif filename == 'lyfjaverdskra-202402001-2.xls':
        return datetime.strptime('2024-02-01', '%Y-%m-%d').date() # Big sigh for spelling mistakes.

    elif filename == 'lyfjaverdskra-2022915.xls':
        return datetime.strptime('2022-09-15', '%Y-%m-%d').date()

    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            date_str = match.group(0)
            try:
                if pattern == r'(\d{2}-\d{2}-\d{4})':
                    # Handle DD-MM-YYYY format
                    return datetime.strptime(date_str, '%d-%m-%Y').date()
                elif pattern == r'lyfjaverdskra-(\d{2})-(\d{4})\.xls':
                    # Handle specific MM-YYYY format
                    month = match.group(1)
                    year = match.group(2)
                    date_str = f"{year}-{month}-01"
                    return datetime.strptime(date_str, '%Y-%m-%d').date()
                elif pattern == r'lyfjaverdskra-(\d{2})(\d{4})\.xls':
                    # Handle specific MMYYYY format
                    month = match.group(1)
                    year = match.group(2)
                    date_str = f"{year}-{month}-01"
                    return datetime.strptime(date_str, '%Y%m%d').date()
                elif pattern == r'(\d{1,2}[\s\-]?[a-zA-Z]+[\s\-]?\d{4})' or pattern == r'(\d{1,2}[^\d]+\w+[^\d]+\d{4})':
                    # Handle D-month-YYYY format with Icelandic month names
                    parts = re.split(r'[\s\-]', date_str)
                    if len(parts) == 3:
                        day = parts[0]
                        month = icelandic_month_to_english(parts[1])
                        year = parts[2]
                        date_str = f"{day} {month} {year}"
                    return datetime.strptime(date_str, '%d %B %Y').date()
                elif len(date_str) == 8 and date_str.isdigit():
                    return datetime.strptime(date_str, '%Y%m%d').date()
                elif len(date_str) == 10:
                    if '-' in date_str:
                        return datetime.strptime(date_str, '%Y-%m-%d').date()
                    else:
                        return datetime.strptime(date_str, '%d-%m-%Y').date()
                elif len(date_str) == 7 and '-' in date_str:
                    return datetime.strptime(date_str, '%Y-%m').date()
                elif len(date_str) == 5 and '-' in date_str:
                    return datetime.strptime(date_str, '%m-%Y').date()
                elif len(date_str) == 7 and date_str.isdigit():
                    return datetime.strptime(date_str, '%d%m%Y').date()
            except ValueError:
                continue

        
    return None

def add_date_column(df, filename):
    extracted_date = extract_date_from_filename(filename=filename)
    df = df.assign(extracted_date=extracted_date)
    return df