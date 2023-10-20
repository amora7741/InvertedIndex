#-------------------------------------------------------------------------
# AUTHOR: Alejandro Mora-Lopez
# FILENAME: db_connection_mongo_solution
# SPECIFICATION: This program simulates an inverted index in MongoDB.
# FOR: CS 4250- Assignment #2
# TIME SPENT: 5 Hours Total
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
from pymongo import MongoClient
from datetime import datetime

def connectDataBase():

    # Create a database connection object using pymongo
    client = MongoClient('localhost', 27017)
    db = client['corpus']
    return db

def createDocument(col, docId, docText, docTitle, docDate, docCat):
    # create a dictionary to count how many times each term appears in the document.
    terms_count = {}
    for term in docText.lower().split(" "):
        cleaned_term = ''.join(char for char in term if char.isalnum())
        if cleaned_term in terms_count:
            terms_count[cleaned_term] += 1
        else:
            terms_count[cleaned_term] = 1

    # create a list of dictionaries to include term objects.
    terms_list = [{"term": term, "num_chars": len(term), "count": terms_count[term]} for term in terms_count]

    docDate = datetime.strptime(docDate, '%Y-%m-%d')

    # Producing a final document as a dictionary including all the required document fields
    document = {
        "_id": docId,
        "title": docTitle,
        "text": docText,
        "num_chars": sum(1 for char in docText if char.isalnum()),  # Count only alphanumeric characters
        "date": docDate,
        "category": {"name": docCat},
        "terms": terms_list
    }

    # Insert the document
    col.insert_one(document)

def deleteDocument(col, docId):

    # Delete the document from the database
    # --> add your Python code here

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    # --> add your Python code here

    # Create the document with the same id
    # --> add your Python code here

def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here