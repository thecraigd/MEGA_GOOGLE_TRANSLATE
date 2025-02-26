import os
import google.generativeai as genai
import time

# Configuration
BASE_DIR = "/Users/craigdickson/Documents/Code/Websites/craigdoesdata"
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
OUTPUT_DIR = os.path.join(RESOURCES_DIR, "resources_de")  # German output directory

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set your API key here
API_KEY = ""  # Replace with your API key - Should replace this with loading from dotenv but I was in a rush

def translate_html(html_content, target_language="German"):
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
        # Send request to the Gemini API
        print("Sending translation request to Gemini API...")
        response = model.generate_content(prompt)  # Remove timeout parameter
        print("Translation completed!")
        return response.text
    except Exception as e:
        print(f"Translation error: {e}")
        return None

def translate_single_file(filename):
    """Translate a single file to German for testing."""
    file_path = os.path.join(RESOURCES_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    print(f"Reading file: {file_path}")
    
    # Read HTML content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            print(f"File size: {len(html_content)} characters")
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return False
    
    # Translate to German
    print("Starting translation to German...")
    start_time = time.time()
    translated_content = translate_html(html_content)
    end_time = time.time()
    
    if translated_content:
        # Save translated content
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            print(f"Translation successful!")
            print(f"Saved to: {output_path}")
            print(f"Translation took {end_time - start_time:.2f} seconds")
            return True
        except Exception as e:
            print(f"Error saving German translation: {e}")
            return False
    else:
        print("Translation failed")
        return False

if __name__ == "__main__":
    if not API_KEY:
        print("Please set your API key in the script")
    else:
        # Get first HTML file that's not in the excluded list
        excluded_files = [
            "de_churn_prediction.html",
            "de_improved_1140_data-visualization-best-practices-for-presenting-product-insights.html",
            "de_improved_data-visualization-best-practices-for-presenting-product-insights.html",
            "resource_template.html"
        ]
        
        # Option 1: Let the user specify the filename
        test_file = input("Enter the name of an HTML file to translate (or press Enter to choose the first available file): ")
        
        if not test_file:
            # Option 2: Choose the first available file
            for file in os.listdir(RESOURCES_DIR):
                if file.endswith(".html") and file not in excluded_files and os.path.isfile(os.path.join(RESOURCES_DIR, file)):
                    test_file = file
                    break
        
        if test_file:
            print(f"Selected test file: {test_file}")
            translate_single_file(test_file)
        else:
            print("No suitable HTML files found")