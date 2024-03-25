#!/usr/bin/env python3
"""
Insert a document in Python
"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document into the given collection based on kwargs
    """
    inserted_document = mongo_collection.insert_one(kwargs)
    return inserted_document.inserted_id
