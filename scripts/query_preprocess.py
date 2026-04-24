import re


def preprocess_query(query: str):

    # lowercase
    query = query.lower()

    # remove extra spaces
    query = query.strip()

    # remove multiple spaces
    query = re.sub(r"\s+", " ", query)

    return query