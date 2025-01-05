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
        # Skip empty or invalid lemmas
        if not lemma or not isinstance(lemma, str) or lemma.isspace():
            print(f"Skipping invalid lemma: {lemma}")
            continue

        # Clean and validate words list
        valid_words = [word for word in words if word and isinstance(word, str) and not word.isspace()]
        if valid_words:
            cleaned_dict[lemma] = valid_words

    # Process the cleaned dictionary
    try:
        for lemma, words in cleaned_dict.items():
            update_query = {
                "$addToSet": {
                    f"lemma_dict.{lemma}": {
                        "$each": words
                    }
                }
            }

            collection.update_one(
                {"_id": main_doc["_id"]},
                update_query,
                upsert=True
            )
        print(f"Successfully merged {len(cleaned_dict)} lemmas")
    except Exception as e:
        print("")
        #print(f"Error during MongoDB update: {str(e)}")

