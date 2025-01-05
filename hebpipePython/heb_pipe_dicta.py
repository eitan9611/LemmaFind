from transformers import AutoModel, AutoTokenizer


def process_roots_memory(input_file):
    # Initialize the DICTA model
    tokenizer = AutoTokenizer.from_pretrained('dicta-il/dictabert-joint')
    model = AutoModel.from_pretrained('dicta-il/dictabert-joint', trust_remote_code=True)
    model.eval()

    # Initialize an empty dictionary
    root_to_words_dict = {}

    # Process the input text file
    with open(input_file, "r", encoding="utf-8") as infile:
        for line in infile:
            try:
                # Process the line using DICTA
                analysis = model.predict([line.strip()], tokenizer, output_style='json')

                # Extract tokens and their lemmas from the analysis
                for token_info in analysis[0]['tokens']:
                    word_text = token_info['token']  # The original word
                    lemma = token_info['lex']  # The root/lemma of the word

                    # Skip empty or None lemmas
                    if not lemma:
                        continue

                    # Ensure the lemma exists in the dictionary
                    if lemma not in root_to_words_dict:
                        root_to_words_dict[lemma] = set()

                    # Add the word to the set (avoids duplication automatically)
                    root_to_words_dict[lemma].add(word_text)

            except Exception as e:
                print(f"Error processing line: {line.strip()}\n{e}")

    # Merge duplicate lemmas and remove redundant ones
    merged_dict = {}
    redundant_lemmas = set()

    # Iterate over the dictionary to merge duplicates and clean redundant lemmas
    for lemma, words in root_to_words_dict.items():
        if lemma not in merged_dict:
            merged_dict[lemma] = set()

        # Add all words to the current lemma's set
        merged_dict[lemma].update(words)

        # If any word itself exists as a lemma, merge its words and mark for deletion
        for word in words:
            if word in root_to_words_dict and word != lemma:
                merged_dict[lemma].update(root_to_words_dict[word])
                redundant_lemmas.add(word)

    # Remove redundant lemmas from the merged dictionary
    for redundant_lemma in redundant_lemmas:
        if redundant_lemma in merged_dict:
            del merged_dict[redundant_lemma]

    # Convert sets to lists in the final dictionary
    final_dict = {lemma: list(words) for lemma, words in merged_dict.items()}

    return final_dict

