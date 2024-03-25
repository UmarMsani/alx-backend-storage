#!/usr/bin/env python3
"""
Provide statistics about Nginx logs stored in MongoDB
"""

from pymongo import MongoClient


def nginx_logs_stats(mongo_collection):
    """
    Display statistics about Nginx logs stored in MongoDB
    """
    # Number of documents in the collection
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")

    # Methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Number of documents with method=GET and path=/status
    count_status = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{count_status} status check")


if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_db = client.logs
    nginx_collection = logs_db.nginx

    # Display statistics
    nginx_logs_stats(nginx_collection)
