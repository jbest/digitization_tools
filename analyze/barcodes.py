import sqlite3
import re
import ast

BRIT_BARCODE_PATTERN = re.compile('^(BRIT)\d+$') 
BKL_BARCODE_PATTERN = re.compile('^(BKL)\d+$') #Brooklyn Botanic Garden
NUMBERS_PATTERN = re.compile('^\d+$') # Numbers only
# set up database
conn = sqlite3.connect('workflow_full_test.db')

with conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    #cur.execute("SELECT * FROM images")
    cur.execute("SELECT * FROM images WHERE file_extension LIKE '%CR2%'")
    rows = cur.fetchall()
 
    for row in rows:
        #print(row['barcodes'])
        catalogNumber = None
        otherCatalogNumbersList = []
        barcodes_string = row['barcodes']
        if barcodes_string:
            barcodes = ast.literal_eval(barcodes_string)
            for barcode in barcodes:
                barcode_value = barcode['data']
                brit_match = BRIT_BARCODE_PATTERN.match(barcode_value)
                bkl_match = BKL_BARCODE_PATTERN.match(barcode_value)
                number_match = NUMBERS_PATTERN.match(barcode_value)
                if brit_match:
                    # make this value the primary catalog number
                    pass
                    #TODO add other barcodes to DwC otherCatalogNumbers
                else:
                    # no BRIT barcode foud for primary catalog number
                    if bkl_match:
                        pass
                        #print('BKL:', barcode_value, row['file_name'])
                    elif number_match:
                        print('number:', barcode_value, row['file_name'])
                    else:
                        print('Not BRIT:', barcode_value, row['file_name'])
                    """
                    number_match = NUMBERS_PATTERN.match(barcode_value)
                    if number_match:
                        print(barcode_value, row['file_name'])
                    """
        else:
            # No barcodes_string
            #print('Alert: No barcode')
            pass
        #print(row)



"""
cur = conn.cursor()
try:
    cur.execute('''CREATE TABLE images (id INTEGER PRIMARY KEY, \
        batch_id text, batch_path text, batch_flags text, image_event_id text, datetime_analyzed text, \
        barcodes text, image_classifications text, closest_model text, \
        image_path text, basename text, file_name text, file_extension text, \
        file_creation_time text, file_hash text, file_uuid text, derived_from_file text)''')
except lite.Error as e:
    print(e)

"""