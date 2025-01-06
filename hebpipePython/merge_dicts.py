def merge_dict_to_mongodb(collection, new_dict):
    """
    Merge a new dictionary into MongoDB collection with validation.

    Args:
        collection: MongoDB collection object
        new_dict: Dictionary containing new lemmas and their words
    """
    # Create initial document if it doesn't exist
    if collection.count_documents({}) == 0:
        collection.insert_one({"lemma_dict": {}})

    # Get or create the main document
    main_doc = collection.find_one()
    if not main_doc:
        main_doc = collection.insert_one({"lemma_dict": {}})
        main_doc = collection.find_one()

    # Clean and validate the dictionary before merging
    cleaned_dict = {}
    for lemma, words in new_dict.items():
        # Replace dots in lemma with 'DOT'
        updated_lemma = lemma.replace('.', 'DOT')

        # Skip empty or invalid lemmas
        if not updated_lemma or not isinstance(updated_lemma, str) or updated_lemma.isspace():
            print(f"Skipping invalid lemma: '{updated_lemma}'")
            continue

        # Clean and validate words list
        valid_words = [word for word in words if word and isinstance(word, str) and not word.isspace()]
        if valid_words:
            print(f"Valid words for lemma '{updated_lemma}': {valid_words}")
            cleaned_dict[updated_lemma] = valid_words
        else:
            print(f"No valid words for lemma '{updated_lemma}'")

    # Debugging: Print the cleaned dictionary
    print("Cleaned dictionary to merge:", cleaned_dict)

    # Process the cleaned dictionary
    try:
        for lemma, words in cleaned_dict.items():
            if not lemma:
                print(f"Skipping update for empty lemma key.")
                continue

            update_query = {
                "$addToSet": {
                    f"lemma_dict.{lemma}": {
                        "$each": words
                    }
                }
            }

            result = collection.update_one(
                {"_id": main_doc["_id"]},
                update_query,
                upsert=True
            )
            print(f"Update result for lemma '{lemma}': {result.modified_count} document(s) modified.")
    except Exception as e:
        print(f"Error during MongoDB update: {str(e)}")


