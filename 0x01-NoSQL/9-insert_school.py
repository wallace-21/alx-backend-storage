#!/usr/bin/env python3

""" Python function that inserts a new document in a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a MongoDB collection based on kwargs.

    Args:
        mongo_collection: pymongo collection object to insert the document into.
        **kwargs: Key-value pairs representing the fields and values of the new document.

    Returns:
        The new _id of the inserted document.
    """
    new = mongo_collection.insert_one(kwargs)
    return new.inserted_id
