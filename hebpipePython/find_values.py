

def get_values_from_dict_inMongo(collection, word):
    """
    Retrieve values for a given word from MongoDB collection.

    Args:
        collection: MongoDB collection object
        word: The word to look up (Hebrew string)

    Returns:
        list: List of values associated with the word
    """
    try:
        # Get the main document
        doc = collection.find_one()
        if not doc:
            print("No document found in collection")
            return []

        # Check if lemma_dict exists
        lemma_dict = doc.get('lemma_dict', {})

        # Look up the word directly
        found_values = lemma_dict.get(word, [])

        # Debug prints
      #  print(f"Looking up word: {word}")
      #  print(f"Found values: {found_values}")

        return found_values

    except Exception as e:
        print(f"Error retrieving from MongoDB: {str(e)}")
        return []