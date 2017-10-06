/*

*/
SELECT image_event_id, COUNT(image_event_id)
FROM images
GROUP BY image_event_id

# Number of records
SELECT COUNT(*)
FROM images

# Number of image events
SELECT COUNT(*) AS image_event_count FROM (
SELECT image_event_id, COUNT(image_event_id)
FROM images
GROUP BY image_event_id
)

# folder set count
SELECT COUNT(*) AS image_event_id FROM (
SELECT image_event_id, COUNT(image_event_id)
FROM images
WHERE image_classifications LIKE "%folder%"
GROUP BY image_event_id
)

# CR2 records
SELECT *
FROM images
WHERE file_extension LIKE "%CR2"

/* records with otherCatalogNumbers */
SELECT *
FROM specimens
WHERE (otherCatalogNumbers IS NOT NULL AND otherCatalogNumbers !='')

/* records with no BRIT catalogNumber but with otherCatalogNumbers */
SELECT *
FROM specimens
WHERE (otherCatalogNumbers IS NOT NULL AND otherCatalogNumbers !='') AND (catalogNumber IS NULL OR catalogNumber = '')


/* testing JOIN */
SELECT
catalogNumber,
otherCatalogNumbers,
images.image_path
FROM specimens s
INNER JOIN images ON s.image_event_id = images.image_event_id
WHERE 
(otherCatalogNumbers IS NOT NULL AND otherCatalogNumbers !='')
AND
(images.file_extension LIKE "%CR2")
AND
(catalogNumber IS NULL OR catalogNumber = '')


/* Drop specimen table */
DROP TABLE IF EXISTS specimens;
/* Create specimen table */
CREATE TABLE specimens 
(id INTEGER PRIMARY KEY, image_event_id text, catalogNumber text, otherCatalogNumbers text, barcodes text, original_file_name text, new_file_name text);
