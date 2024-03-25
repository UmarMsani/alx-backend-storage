#!/usr/bin/env python3
"""
students
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score
    """
    pipeline = [
        {"$unwind": "$topics"},
        {"$group": {"_id": "$_id", "name": {"$first": "$name"}, "averageScore": {"$avg": "$topics.score"}}},
        {"$project": {"_id": 1, "name": 1, "averageScore": 1}},
        {"$sort": {"averageScore": -1}}
    ]
    top_students = list(mongo_collection.aggregate(pipeline))
    return top_students
