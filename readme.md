[![CraigDoesData][logo]][link]

[logo]: https://github.com/thecraigd/Python_SQL/raw/master/img/logo.png
[link]: https://www.craigdoesdata.com/


# MEGA GOOGLE TRANSLATE

**Translate your HTML files to multiple languages with the power of Google Gemini!**

Welcome to **MEGA GOOGLE TRANSLATE**, a repository containing Python scripts designed to automate the translation of HTML files using the cutting-edge Google Gemini API, specifically leveraging the `gemini-2.0-flash-thinking-exp-01-21` model (experimental and fast! I tried the OpenAI and Anthropic APIs, but neither of them would accept HTML files of the size I needed to translate. Gemini did it for free!).  This project is perfect for anyone looking to quickly internationalize their web content or documents programmatically.

This repository contains two main scripts:

*   `gemini_script.py`:  For translating a **single** HTML file – ideal for testing and focused translations.
*   `gemini_script_all_loop.py`:  For batch translating **multiple** HTML files into **several** target languages in a loop, streamlining the process for larger projects.

Let's dive into how these scripts work!

## 🛠️ Packages Used

Before you get started, make sure you have the following Python packages installed. You can easily install them using pip:

```bash
pip install google-generativeai
```

*   **`google-generativeai`**: This is the official Python library for interacting with Google's Generative AI models, including Gemini. We'll be using this to send our translation requests to the Gemini API.
*   **`os`**:  A built-in Python module for interacting with the operating system. We use it for file path manipulation and directory operations.
*   **`pathlib`**:  Another built-in module that offers a more object-oriented way to handle file paths and directories.
*   **`time`**:  Built-in module for time-related functions, used here to introduce delays between API calls and measure translation times.

## 🚀 High-Level Overview

Both scripts share the core functionality: they read HTML content from a file, send it to the Google Gemini API for translation, and then save the translated content to a new file.  The magic lies in Gemini's powerful language understanding and translation capabilities, combined with a prompt carefully crafted to ensure HTML structure and formatting are preserved during translation.

**Key Features:**

*   **HTML Tag Preservation:**  Scripts are designed to *only* translate the text content within HTML tags, leaving all tags, attributes, and code snippets untouched. This ensures your translated files remain valid HTML documents with the same structure as the originals.
*   **Multiple Language Support (in `gemini_script_all_loop.py`):**  Easily translate your HTML files into multiple languages (currently configured for Spanish, German, French, Portuguese, and Italian, but easily customizable).
*   **Batch Processing (in `gemini_script_all_loop.py`):**  Process multiple HTML files in one go, saving you time and effort.
*   **Rate Limiting Awareness:**  Includes a delay between API calls to help avoid hitting rate limits and ensure smooth operation.
*   **Error Handling:** Basic error handling to catch potential issues during file reading, API calls, and file saving.

## ⚙️ Detailed Script Breakdown

Let's break down each script to understand how they achieve this translation magic.

### `gemini_script.py` - Single File Translation

This script focuses on translating a single HTML file into German (by default, but easily adjustable). It's perfect for testing the translation process or when you only need to translate one file.

**Key Steps:**

1.  **Configuration:**
    *   Sets up `BASE_DIR`, `RESOURCES_DIR`, and `OUTPUT_DIR` variables to manage file paths. You'll need to adjust `BASE_DIR` to your local project directory.
    *   Creates the `OUTPUT_DIR` (specifically `resources_de` for German) if it doesn't already exist.
    *   **Crucially, you need to set your `API_KEY` variable!**  This is your Google Gemini API key. **Remember to keep your API key secure and do not commit it directly to your repository!**  Consider using environment variables for better security in a production setting.

2.  **`translate_html(html_content, target_language="German")` Function:**
    *   This is the heart of the translation process.
    *   It configures the `genai` library with your `API_KEY`.
    *   It instantiates the `gemini-2.0-flash-thinking-exp-01-21` model.
    *   **Prompt Engineering:**  A detailed prompt is constructed and sent to the Gemini API. This prompt is carefully designed to instruct Gemini to:
        *   Translate to the specified `target_language`.
        *   **Preserve HTML structure and tags.**  The prompt explicitly lists guidelines to ensure Gemini understands to only translate text content and leave HTML markup untouched. This is critical for maintaining valid HTML.
    *   Sends the translation request using `model.generate_content(prompt)`.
    *   Returns the translated text from the API response.
    *   Includes basic error handling to catch exceptions during the API call and return `None` in case of failure.

3.  **`translate_single_file(filename)` Function:**
    *   Takes the `filename` of the HTML file as input.
    *   Constructs the full file paths for the input and output files.
    *   Reads the HTML content from the input file, handling potential file reading errors.
    *   Calls the `translate_html()` function to perform the translation.
    *   If translation is successful:
        *   Saves the `translated_content` to the output file in the `OUTPUT_DIR`.
        *   Prints success messages and the translation time.
    *   If translation fails, prints an error message.

4.  **Main Execution (`if __name__ == "__main__":`)**
    *   Checks if the `API_KEY` is set. If not, it prompts the user to set it.
    *   Provides options for selecting an HTML file to translate:
        *   **User Input:**  Allows the user to type in the filename.
        *   **Automatic Selection:** If the user presses Enter without typing a filename, it finds the first `.html` file in the `RESOURCES_DIR` (excluding specified excluded files) and uses that.
    *   Calls `translate_single_file()` to perform the translation on the selected file.

### `gemini_script_all_loop.py` - Batch Translation for Multiple Languages

This script expands on the single-file translation to handle multiple HTML files and translate them into several languages in a loop. This is ideal for preparing your website or documentation for a multilingual audience.

**Key Enhancements and Differences from `gemini_script.py`:**

1.  **Language Configuration (`LANGUAGES` dictionary):**
    *   Introduces a `LANGUAGES` dictionary to define the target languages and their language codes (e.g., `"es": "Spanish"`).  This makes it easy to add or modify target languages.

2.  **`create_language_folders()` Function:**
    *   Before processing files, this function creates language-specific output directories within the `RESOURCES_DIR` (e.g., `resources_es`, `resources_de`, etc.) based on the `LANGUAGES` dictionary.  It uses `os.makedirs(exist_ok=True)` to ensure directories are created only if they don't exist and avoids errors if they do.

3.  **`get_html_files()` Function:**
    *   Dynamically retrieves a list of all `.html` files from the `RESOURCES_DIR`, excluding files listed in `EXCLUDED_FILES` and ensuring it only includes files, not subdirectories.

4.  **`process_files()` Function (Core Batch Processing Logic):**
    *   Calls `create_language_folders()` to set up the output directory structure.
    *   Calls `get_html_files()` to get the list of HTML files to translate.
    *   **Loops through each HTML file:**
        *   Reads the HTML content.
        *   **Nested Loop for Languages:**  For each HTML file, it then loops through each language defined in the `LANGUAGES` dictionary.
            *   Constructs the output file path in the language-specific directory.
            *   **Checks for Existing Translations:**  It efficiently checks if a translated file already exists for the current language. If it does, it skips the translation for that language, avoiding redundant API calls and saving time.
            *   Calls `translate_html()` to translate the HTML content to the current language.
            *   If translation is successful, saves the translated content to the language-specific output file.
            *   **Introduces a `time.sleep(3)` delay:**  This is important to prevent overwhelming the Gemini API with requests and potentially hitting rate limits. You might need to adjust this delay depending on the number of files and languages you are processing and your API usage limits.
            *   Prints informative messages at each step, including file processing progress, language translation status, and translation times.

5.  **Main Execution (`if __name__ == "__main__":`)**
    *   Same API key check as `gemini_script.py`.
    *   Calls `process_files()` to initiate the batch translation process.
    *   Prints a "Translation process completed!" message at the end.

## 🚀 Get Started!

1.  **Clone this repository:**
    ```bash
    git clone [repository-url]
    cd MEGA-GOOGLE-TRANSLATE
    ```
2.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt  # (Optional: Create a requirements.txt with `google-generativeai`)
    ```
    or
    ```bash
    pip install google-generativeai
    ```
3.  **Set your Google Gemini API Key:**
    *   **Edit either `gemini_script.py` or `gemini_script_all_loop.py` and replace `API_KEY = ""` with your actual API key.**  **Remember to keep this key secure!**

4.  **Configure Directories (if needed):**
    *   Adjust the `BASE_DIR` and `RESOURCES_DIR` variables in both scripts to point to your project's resources directory.  Make sure your HTML files are located in the `RESOURCES_DIR`.

5.  **Run the scripts:**
    *   **For single file translation (German):**
        ```bash
        python gemini_script.py
        ```
        Follow the prompts to select a file or let it choose the first available one.
    *   **For batch translation (multiple languages):**
        ```bash
        python gemini_script_all_loop.py
        ```
        This will process all `.html` files in your `RESOURCES_DIR` and create translated versions in language-specific subdirectories.

## ⚠️ Important Notes and Considerations

*   **API Key Security:**  **Never commit your API key directly to your repository.**  Consider using environment variables or a more secure configuration method, especially if you plan to share your code or use it in a production environment.
*   **Google Gemini API Costs:**  Be aware of the usage costs associated with the Google Gemini API.  Check Google Cloud documentation for pricing details.  The `gemini-2.0-flash-thinking-exp-01-21` model might have different pricing than other Gemini models. (In practice, in Feb 2025 I was able to translate ~30 long documents into 5 separate languages for free).
*   **Rate Limiting:**  The scripts include a delay to help avoid rate limiting. However, if you are processing a large number of files, you might still encounter rate limits. Monitor your API usage and adjust the `time.sleep()` delay in `gemini_script_all_loop.py` if needed.
*   **HTML Complexity:**  While the scripts are designed to handle standard HTML, very complex or malformed HTML might lead to unexpected translation results.  Always review the translated files to ensure accuracy and proper formatting.
*   **Experimental Model:** The script uses `gemini-2.0-flash-thinking-exp-01-21`, which is described as an experimental model.  The behavior and availability of experimental models can change.  You might want to consider using a more stable Gemini model for production use cases in the future.

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements, bug fixes, or new features, feel free to submit a pull request.

## 📧 Contact

If you have any questions or need assistance, feel free to [get in touch](www.craigdoesdata.com/contact.html)

## 📜 License

MIT License

---

**Happy Translating!** ✨
```
# MEGA_GOOGLE_TRANSLATE
