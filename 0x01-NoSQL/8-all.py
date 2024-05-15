#!/usr/bin/env python3

def list_all(mongo_collection):
    """
    Retrieve all documents from a MongoDB collection.

    Args:
        mongo_collection: pymongo collection object to retrieve documents from.

    Returns:
        A cursor object containing all documents from the collection if documents are found,
        otherwise an empty list.
    """
    action = mongo_collection.find({})
    if action.count() == 0:
        return []
    return action
