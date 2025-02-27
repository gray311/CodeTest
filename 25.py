import pickle

def deserialize_data(pickled_data: str):
    """
    Deserializes data from a pickled string using pickle.loads.

    Parameters:
    pickled_data (str): A string containing pickled data.

    Returns:
    The deserialized object.
    """
    return pickle.loads(pickled_data)