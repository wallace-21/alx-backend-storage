#!/usr/bin/env python3
""" Using pipelines to arrange students by average score """


def top_students(mongo_collection):
    """ returns all students sorted by average score"""
    result = mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {"$avg": "$topics.score"}}},
        {"$sort": {"averageScore": -1}}
    ])
    return result
