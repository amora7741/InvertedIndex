#-------------------------------------------------------------------------
# AUTHOR: your name
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #1
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
import psycopg2
from psycopg2.extras import RealDictCursor

def connectDataBase():
    DB_NAME = "corpus"
    DB_USER = "postgres"
    DB_PASS = "123"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    try:
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
            cursor_factory=RealDictCursor
        )

        return conn
    
    except:
        print("Database not connected successfully!")


def createCategory(cur, catId, catName):
    # Insert a category in the database
    try:
        query = "INSERT INTO Categories (category_id, name) VALUES (%s, %s)"
        recset = [catId, catName]
        cur.execute(query, recset)
    except Exception as e:
        print(f"Error creating category: {e}")

def createDocument(cur, docId, docText, docTitle, docDate, docCat):
    # 1 Get the category id based on the informed category name
    query = "SELECT category_id FROM Categories WHERE name = %s"
    recset = [docCat]
    cur.execute(query, recset)
    cat_id = cur.fetchone()['category_id']
    
    # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
    numChars = len(''.join(filter(str.isalnum, docText)))
    query = "INSERT INTO Documents (doc_number, text, title, date, num_chars, category_id) VALUES (%s, %s, %s, %s, %s, %s)"
    recset = [docId, docText, docTitle, docDate, numChars, cat_id]
    cur.execute(query, recset)

    # 3 Update the potential new terms.

    # 3.1 Find all terms that belong to the document. Use space " " as the
    # delimiter character for terms and Remember to lowercase terms and remove
    # punctuation marks.
    filteredChars = filter(lambda x: x.isalnum() or x.isspace(), docText)
    cleanedString = ''.join(filteredChars)
    lowercaseString = cleanedString.lower()
    terms = lowercaseString.split()

    for term in set(terms):
        # 3.2 Check if the term already exists in the database
        query = "SELECT term FROM Terms WHERE term = %s"
        recset = [term]
        cur.execute(query, recset)
        if cur.fetchone() is None:
            # 3.3 In case the term does not exist, insert it into the database
            query = "INSERT INTO Terms (term, num_chars) VALUES (%s, %s)"
            recset = [term, len(term)]
            cur.execute(query, recset)

    # 4 Update the index
    termCount = {}
    for term in terms:
        termCount[term] = termCount.get(term, 0) + 1

    for term, count in termCount.items():
        query = "SELECT count FROM Index WHERE doc_number = %s AND term = %s"
        recset = [docId, term]
        cur.execute(query, recset)
        result = cur.fetchone()

        if result:
            newCount = result['count'] + count
            query = "UPDATE Index SET count = %s WHERE doc_number = %s AND term = %s"
            recset = [newCount, docId, term]
            cur.execute(query, recset)
        else:
            query = "INSERT INTO Index (doc_number, term, count) VALUES (%s, %s, %s)"
            recset = [docId, term, count]
            cur.execute(query, recset)

def createDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Get the category id based on the informed category name
    # --> add your Python code here

    # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
    # --> add your Python code here

    # 3 Update the potential new terms.
    # 3.1 Find all terms that belong to the document. Use space " " as the delimiter character for terms and Remember to lowercase terms and remove punctuation marks.
    # 3.2 For each term identified, check if the term already exists in the database
    # 3.3 In case the term does not exist, insert it into the database
    # --> add your Python code here

    # 4 Update the index
    # 4.1 Find all terms that belong to the document
    # 4.2 Create a data structure the stores how many times (count) each term appears in the document
    # 4.3 Insert the term and its corresponding count into the database
    # --> add your Python code here

def deleteDocument(cur, docId):

    # 1 Query the index based on the document to identify terms
    # 1.1 For each term identified, delete its occurrences in the index for that document
    # 1.2 Check if there are no more occurrences of the term in another document. If this happens, delete the term from the database.
    # --> add your Python code here

    # 2 Delete the document from the database
    # --> add your Python code here

def updateDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Delete the document
    # --> add your Python code here

    # 2 Create the document with the same id
    # --> add your Python code here

def getIndex(cur):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here