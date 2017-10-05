import sqlite3
import re
import ast

BRIT_BARCODE_PATTERN = re.compile('^(BRIT)\d+$') 
BKL_BARCODE_PATTERN = re.compile('^(BKL)\d+$') #Brooklyn Botanic Garden
NUMBERS_PATTERN = re.compile('^\d+$') # Numbers only
# set up database
database_file = 'workflow_test.db'
conn = sqlite3.connect(database_file)

specimens = []
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
                    catalogNumber = barcode_value
                else:
                    # no BRIT barcode foud for primary catalog number
                    if bkl_match:
                        otherCatalogNumbersList.append(barcode_value)
                        #print('BKL:', barcode_value, row['file_name'])
                    elif number_match:
                        otherCatalogNumbersList.append(barcode_value)
                        #print('number:', barcode_value, row['file_name'])
                    else:
                        #print('Not BRIT:', barcode_value, row['file_name'])
                        #TODO flag record as bad number
                        pass
                    """
                    number_match = NUMBERS_PATTERN.match(barcode_value)
                    if number_match:
                        print(barcode_value, row['file_name'])
                    """
                    #print(otherCatalogNumbersList, row['file_name'])
            #print(catalogNumber, otherCatalogNumbersList)
        else:
            # No barcodes_string
            #print('Alert: No barcode')
            pass
        # Create otherCatalogNumbers string
        sep = '|'
        otherCatalogNumbers = sep.join(otherCatalogNumbersList)
        #Add specimen metadata
        specimen_record={}
        specimen_record['catalogNumber'] = catalogNumber
        specimen_record['otherCatalogNumbers'] = otherCatalogNumbers
        specimen_record['barcodes'] = barcodes_string
        specimen_record['image_event_id'] = row['image_event_id']
        specimen_record['original_file_name'] = row['file_name']
        specimen_record['new_file_name'] = None #TODO change to catalogNumber
        specimens.append(specimen_record)

"""
for specimen in specimens:
    print (specimen['image_event_id'], specimen['catalogNumber'], specimen['otherCatalogNumbers'], specimen['barcodes'], specimen['original_file_name'], specimen['new_file_name'])
"""
with conn:
    cur = conn.cursor()
    #cur.execute("SELECT * FROM images")
    for specimen in specimens:
        cur.execute(\
            "INSERT INTO specimens (image_event_id, catalogNumber, otherCatalogNumbers, barcodes, original_file_name, new_file_name)\
            VALUES (?, ?, ?, ?, ?, ?)", \
            (specimen['image_event_id'], specimen['catalogNumber'], specimen['otherCatalogNumbers'],\
                specimen['barcodes'], specimen['original_file_name'], specimen['new_file_name'])\
            )
        conn.commit()


"""
cur.execute(\
    "INSERT INTO images (batch_id, batch_path, batch_flags, image_event_id, datetime_analyzed, barcodes, image_classifications, closest_model, \
        image_path, basename, file_name, file_extension, file_creation_time, file_hash, file_uuid, derived_from_file)\
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?)", \
    (batch_id, batch_path, batch_flags, image_event_id, datetime_analyzed, barcodes, image_classifications, closest_model, \
        image_path, basename, file_name, file_extension, file_creation_time, file_hash, file_uuid, derived_from_file))
conn.commit()
"""

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