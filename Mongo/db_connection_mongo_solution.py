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
    termsCount = {}
    for term in docText.lower().split(" "):
        cleanedTerm = ''.join(char for char in term if char.isalnum())
        
        if cleanedTerm in termsCount:
            termsCount[cleanedTerm] += 1
        else:
            termsCount[cleanedTerm] = 1

    # create a list of dictionaries to include term objects.
    termsList = [{"term": term, "num_chars": len(term), "count": termsCount[term]} for term in termsCount]

    docDate = datetime.strptime(docDate, '%Y-%m-%d')

    # Producing a final document as a dictionary including all the required document fields
    document = {
        "_id": docId,
        "title": docTitle,
        "text": docText,
        "num_chars": sum(1 for char in docText if char.isalnum()),  # Count only alphanumeric characters
        "date": docDate,
        "category": {"name": docCat},
        "terms": termsList
    }

    # Insert the document
    col.insert_one(document)

def deleteDocument(col, docId):
    # Delete the document from the database
    col.delete_one({"_id": docId})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):
    # Delete the document
    deleteDocument(col, docId)

    # Create the document with the same id
    createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):
    # Query the database to return the documents where each term occurs with their corresponding count.
    output = {}

    documents = col.find({})
    for document in documents:
        for termObj in document["terms"]:
            term = termObj["term"]

            if term in output:
                output[term] += f",{document['title']}:{termObj['count']}"
            else:
                output[term] = f"{document['title']}:{termObj['count']}"

    return output