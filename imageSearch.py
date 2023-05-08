from utilities import *
import psycopg2
from io import BytesIO
from time import perf_counter
numResultsPerPage = 13
def imageSearch(imageString, pageNumber):
    start = perf_counter()
    Hash = getHashInt(BytesIO(imageString), False)
    maxDifference = 3

    conn = psycopg2.connect(database ="postgres", user = "postgres",
                            password = "reverseWikipedia", host = "192.168.204.7", 
                            )
    cursor = conn.cursor()
    print("Connection Successful to PostgreSQL")

    cursor.execute(f"SELECT url FROM hashes WHERE hash <@ ({Hash}, {maxDifference}) limit {numResultsPerPage} offset {(pageNumber - 1) * numResultsPerPage}")
    hashRows = cursor.fetchall()
    urls = [x[0] for x in hashRows]
    count = None
    if (pageNumber == 1):
        cursor.execute(f"SELECT count(*) AS exact_count FROM hashes WHERE hash <@ ({Hash}, {maxDifference})")
        count = cursor.fetchone()[0]
    end = perf_counter()
    return [urls, count, numResultsPerPage, round((end-start), 2)]
