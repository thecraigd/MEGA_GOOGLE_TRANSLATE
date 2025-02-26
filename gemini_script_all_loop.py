import os
import google.generativeai as genai
from pathlib import Path
import time

# Configuration
BASE_DIR = "/Users/craigdickson/Documents/Code/Websites/craigdoesdata"
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
EXCLUDED_FILES = [
    "resource_template.html"
]

# Language configuration
LANGUAGES = {
    "es": "Spanish",
    "de": "German",
    "fr": "French",
    "pt": "Portuguese",
    "it": "Italian"
}

# Set your API key here
API_KEY = ""  # Replace with your API key - Should replace this with loading from dotenv but I was in a rush

def create_language_folders():
    """Create language-specific folders if they don't exist."""
    for lang_code in LANGUAGES.keys():
        lang_dir = os.path.join(RESOURCES_DIR, f"resources_{lang_code}")
        os.makedirs(lang_dir, exist_ok=True)
        print(f"Created directory: {lang_dir}")

def get_html_files():
    """Get all HTML files from the resources directory, excluding specified files and subfolders."""
    html_files = []
    for file in os.listdir(RESOURCES_DIR):
        file_path = os.path.join(RESOURCES_DIR, file)
        if (
            file.endswith(".html") 
            and file not in EXCLUDED_FILES 
            and os.path.isfile(file_path)
        ):
            html_files.append(file)
    return html_files

def translate_html(html_content, target_language):
    """Translate HTML content using Google Gemini API."""
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21")
    
    prompt = f"""Translate the following HTML document into {target_language}.
    
    Important guidelines:
    1. Preserve all HTML tags and attributes exactly as they are.
    2. Only translate the text content between the tags.
    3. Maintain any special formatting, links, or code snippets unchanged.
    4. Keep the overall document structure intact.
    5. Ensure that all opening and closing tags remain paired.
    6. Do not translate variable names, function names, or other code elements.
    7. Maintain any custom data attributes or IDs exactly as in the original.
    8. Translate meta tags content and title tags as appropriate.
    
    Here is the HTML document to translate:
    
    {html_content}
    """
    
    try:
        print(f"    Sending translation request to {target_language}...")
        response = model.generate_content(prompt)
        print(f"    {target_language} translation completed!")
        return response.text
    except Exception as e:
        print(f"    Translation error: {e}")
        return None

def process_files():
    """Process all HTML files and translate them to target languages."""
    # Create language folders
    create_language_folders()
    
    # Get HTML files
    html_files = get_html_files()
    total_files = len(html_files)
    
    print(f"Found {total_files} HTML files to translate")
    
    # Process each file
    for index, file in enumerate(html_files, 1):
        file_path = os.path.join(RESOURCES_DIR, file)
        
        print(f"[{index}/{total_files}] Processing: {file}")
        
        # Read HTML content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            print(f"  File size: {len(html_content)} characters")
        except Exception as e:
            print(f"Error reading file {file}: {e}")
            continue
        
        # Translate to each language
        for lang_code, lang_name in LANGUAGES.items():
            output_dir = os.path.join(RESOURCES_DIR, f"resources_{lang_code}")
            output_path = os.path.join(output_dir, file)
            
            # Skip if translation already exists
            if os.path.exists(output_path):
                print(f"  - {lang_name} translation already exists, skipping")
                continue
            
            print(f"  - Starting translation to {lang_name}...")
            start_time = time.time()
            translated_content = translate_html(html_content, lang_name)
            end_time = time.time()
            
            if translated_content:
                # Save translated content
                try:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(translated_content)
                    print(f"    Saved to {output_path}")
                    print(f"    Translation took {end_time - start_time:.2f} seconds")
                except Exception as e:
                    print(f"    Error saving {lang_name} translation: {e}")
            else:
                print(f"    Failed to translate to {lang_name}")
            
            # Add a delay to avoid rate limiting
            time.sleep(3)  # Increased delay between API calls

if __name__ == "__main__":
    if not API_KEY:
        print("Please set your API key in the script")
    else:
        process_files()
        print("Translation process completed!")