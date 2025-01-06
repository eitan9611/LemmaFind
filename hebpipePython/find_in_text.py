from transformers import AutoModel, AutoTokenizer
from collections import defaultdict
import pypdfium2 as pdfium

def process_roots_memory(input_file):
    # Initialize the DICTA model
    tokenizer = AutoTokenizer.from_pretrained('dicta-il/dictabert-joint')
    model = AutoModel.from_pretrained('dicta-il/dictabert-joint', trust_remote_code=True)
    model.eval()  # Ensure we only use the model and not updating it

    # Initialize an empty defaultdict with sets
    root_to_words_dict = defaultdict(set)

    if input_file.endswith("txt"):
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
                        if not lemma or lemma == "[BLANK]":
                            continue

                        # Add the word to the set of the corresponding lemma (avoids duplication)
                        root_to_words_dict[lemma].add(word_text)

                except Exception as e:
                    print(f"Error processing line: {line.strip()}\n{e}")
    
    elif input_file.endswith("pdf"):
        try:
            # Load the PDF file
            pdf = pdfium.PdfDocument(input_file)
            
            # Process each page
            for page_number in range(len(pdf)):
                # Get the page
                page = pdf[page_number]
                width = int(page.get_width())
                height = int(page.get_height())
                
                # Extract text from the page with boundaries
                text_page = page.get_textpage()
                text_content = text_page.get_text_bounded(left=0, top=0, right=width, bottom=height)
                
                # Split the text into lines
                lines = text_content.split('\n')
                
                # Process each line
                for line in lines:
                    if line.strip():  # Skip empty lines
                        try:
                            # Process the line using DICTA
                            analysis = model.predict([line.strip()], tokenizer, output_style='json')

                            # Extract tokens and their lemmas from the analysis
                            for token_info in analysis[0]['tokens']:
                                word_text = token_info['token']
                                lemma = token_info['lex']

                                # Skip empty or None lemmas
                                if not lemma or lemma == "[BLANK]":
                                    continue

                                # Add the word to the set of the corresponding lemma
                                root_to_words_dict[lemma].add(word_text)

                        except Exception as e:
                            print(f"Error processing line on page {page_number + 1}: {line.strip()}\n{e}")
                
                # Clean up page resources
                page.close()
            
            # Clean up PDF resources
            pdf.close()
            
        except Exception as e:
            print(f"Error processing PDF file: {input_file}\n{e}")
    
    else:
        raise ValueError("Unsupported file format. Only .txt and .pdf files are supported.")

    # Convert sets to lists in the final dictionary
    final_dict = {lemma: list(words) for lemma, words in root_to_words_dict.items()}

    return final_dict
