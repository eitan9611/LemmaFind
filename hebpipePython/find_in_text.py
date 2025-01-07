import pypdfium2 as pdfium
import re
import json

def get_file_letter(page_number):
    if page_number <= 207:
        return "א"
    elif page_number <= 289:
        return "ב"
    elif page_number <= 379:
        return "ג"
    elif page_number <= 419:
        return "ד"
    elif page_number <= 526:
        return "ה"
    elif page_number <= 602:
        return "ו"
    elif page_number <= 691:
        return "ז"
    else:
        return "ח"

def is_valid_paragraph_marker(text):
    # Single letter case - any Hebrew letter is valid
    if len(text) == 1:
        return '\u0590' <= text <= '\u05FF'
    
    # Two letter case - must start with י כ ל מ נ ס ע פ צ
    elif len(text) == 2:
        valid_starts_2 = 'יכלמנסעפצ'
        return any(text.startswith(letter) for letter in valid_starts_2)
    
    # Three or four letter case - must start with ק ר ש ת
    elif len(text) in [3, 4]:
        valid_starts_34 = 'קרשת'
        return any(text.startswith(letter) for letter in valid_starts_34)
    
    # No valid markers with 5 or more letters
    else:
        return False

def find_paragraph_marker(line):
    # Strip whitespace from the beginning
    line = line.lstrip()
    
    # Line should be long enough
    if len(line) < 2:
        return None
    
    # every paragraph letter starts always with "letter dot space".
    match = re.match(r'^([\u0590-\u05FF]{1,4})\.\s+(.+)', line)
    if not match:
        return None
        
    potential_marker = match.group(1)
    following_text = match.group(2)
    
    # Validate according to Hebrew numbering rules
    if not is_valid_paragraph_marker(potential_marker):
        return None
        
    # Check that following text is substantial
    if len(following_text.strip()) < 5:
        return None
        
    return potential_marker

def find_sentences_with_values(pdf_path, search_words):
    results = []
    pdf = pdfium.PdfDocument(pdf_path)

    try:
        total_pages = len(pdf)
        current_paragraph = None
        
        for page_num in range(total_pages):
            page = pdf[page_num]
            width = int(page.get_width())
            height = int(page.get_height())
            
            text_page = page.get_textpage()
            text = text_page.get_text_bounded(left=0, top=0, right=width, bottom=height)
            
            if not text:
                continue
            
            lines = text.split('\n')
            
            for line in lines:
                marker = find_paragraph_marker(line)
                if marker:
                    current_paragraph = marker
                    # Remove the paragraph marker from the line
                    marker_length = len(marker) + 2  # +2 for dot and space
                    line = line[marker_length:].strip()
                
                if not line:
                    continue
                
                sentences = re.split(r'(?<=[.!?])\s+', line)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    
                    for word in search_words:
                        if re.search(r'\b' + re.escape(word) + r'\b', sentence):
                            file_letter = get_file_letter(page_num + 1)
                            
                            result = {
                                "file_letter": file_letter,
                                "paragraph_marker": current_paragraph,
                                "sentence": sentence,
                                "word": word,
                                "page": page_num + 1
                            }
                            
                            results.append(result)
                            break
    
    finally:
        pdf.close()
    
    if not results:
        return json.dumps([], ensure_ascii=False)
    
    return json.dumps(results, ensure_ascii=False, indent=4)