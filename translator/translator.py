import requests
import argparse
from typing import List
from pathlib import Path
from bs4 import BeautifulSoup


PROJECT_ROOT = Path(__file__).resolve().parent.parent
USER_AGENT = 'Mozilla/5.0'
SUPPORTED_LANGUAGES = ("Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese", "Dutch", "Polish",
                       "Portuguese", "Romanian", "Russian", "Turkish")
SUPPORTED_LANGUAGES_LOWERCASE = ("arabic", "german", "english", "spanish", "french", "hebrew", "japanese", "dutch",
                                 "polish", "portuguese", "romanian", "russian", "turkish")


def find_all_word_translations(soup: BeautifulSoup) -> List[str]:
    """
    :param soup: BeatifulSoup object that has already requested html.parser data from a URL.
    :return: list containing all translation words.
    """
    # Find all translations for the word in the HTML page.
    all_translation_links = soup.find_all("a", {"class": 'translation'})
    all_translations = []
    for link in all_translation_links:
        # Use the <a> HTML object text
        translation_string = link.get_text()

        # Clean the text before appending
        translation_string = translation_string.strip().lower()
        # if translation_string.lower() != "translation":
        all_translations.append(translation_string)

    # Return a str, not a list
    return all_translations


def find_all_translation_sentence_examples(soup: BeautifulSoup) -> List[tuple]:
    """
    :param soup: BeatifulSoup object that has already requested html.parser data from a URL.
    :return: list containing all translation words.
    """
    # Filter for <div> that corresponds to the sentence examples on the HTML page.
    all_translation_div_start = soup.find_all('div', {"class": "src ltr"})
    all_translation_div_end = soup.find_all('div', {"class": ["trg ltr", "trg rtl arabic", "trg rtl"]})

    # Zip all the translated sentence pairs together
    all_translation_sentence_examples = []
    all_translation_zip = zip(all_translation_div_start, all_translation_div_end)
    for sentence_start, sentence_end in all_translation_zip:
        sentence_start, sentence_end = sentence_start.text.strip(), sentence_end.text.strip()
        if len(sentence_start) > 0:
            all_translation_sentence_examples.append((sentence_start, sentence_end))

    # Return a str, not a list
    return all_translation_sentence_examples


def print_results_formatted(word_examples: List[str], sentence_examples: List[tuple],
                            language_end: str, count: int) -> list:
    """
    Formats the results and prints the count number of results
    :param word_examples: list of words that have been translated
    :param sentence_examples: list of sentence pairs containing (sentence_start, sentence_end)
    :param language_end: End/target language for the translation
    :param count: Number of examples to print
    :return: None
    """
    # Only print and save a given count of examples
    word_examples, sentence_examples = word_examples[:count], sentence_examples[:count]

    lines_for_print = []
    lines_for_save = []

    # Word example translations from language_start to language_end
    word_print_string = f"{language_end.title()} Translations:"
    lines_for_print.append("\n" + word_print_string)
    lines_for_save.append(word_print_string + "\n")
    for i, word in enumerate(word_examples):
        lines_for_print.append(word)
        lines_for_save.append(word + "\n")
        if i == len(word_examples) - 1:
            lines_for_save.append("\n")

    # Print up to "count" sentence pairs of original sentence and it's translation
    sentence_print_string = f"{language_end.title()} Examples:"
    lines_for_print.append("\n" + sentence_print_string)
    lines_for_save.append(sentence_print_string + "\n")
    for i, (sentence_start, sentence_end) in enumerate(sentence_examples):
        lines_for_print.append(sentence_start)
        lines_for_save.append(sentence_start + "\n")
        lines_for_print.append(sentence_end)
        lines_for_save.append(sentence_end + "\n")
        if i == len(sentence_examples) - 1:
            lines_for_save.append("\n")

    # Print lines
    for line in lines_for_print:
        print(line)
    return lines_for_save


# def get_user_selection() -> tuple:
#     """
#     :return: tuple of starting language, ending language, and word for translation
#     """
#
#     # Print languages supported for translation.
#     print("Hello, you're welcome to the translator. Translator supports:")
#     i = 1
#     for language in SUPPORTED_LANGUAGES:
#         print(f"{i}. {language}")
#         i += 1
#
#     # Starting language prompt and ending/target language prompt
#     start = int(input("Type the number of your language:\n"))
#     end = int(input("Type the number of a language you want to translate to or '0' to translate to all languages:\n"))
#
#     # Convert the start and end int to a language str
#     start_string = SUPPORTED_LANGUAGES[start - 1].lower()
#     end_string = [SUPPORTED_LANGUAGES[end - 1].lower()] if end != 0 else [l.lower() for l in SUPPORTED_LANGUAGES]
#
#     # Word to translate from start to end languages
#     word = input("Type the word you want to translate:\n")
#
#     return start_string, end_string, word


def _parse_args() -> argparse.Namespace:
    # choices=
    parser = argparse.ArgumentParser(description="translator.py will translate a word from start to end language.")
    parser.add_argument("language_start", type=str, default="english",
                        help="Starting language for translation. Example \"english\".")
    parser.add_argument("language_end", type=str, default="spanish",
                        help="Ending language for translation. Use 'all' to translate to all available languages. Example: \"spanish\".")
    parser.add_argument("word", type=str, default="hello", help="Word to translate. Example \"hello\".")
    parser.add_argument("--example_count", type=int, default=2, help="Number of example translations to return.")
    return parser.parse_args()


if __name__ == "__main__":
    # Parse command line arguments
    args = _parse_args()

    # Use command line arguments for starting language, ending language(s), and word to translate.
    language_start, language_end, word = args.language_start, args.language_end, args.word
    language_start = language_start.lower()

    if language_start not in SUPPORTED_LANGUAGES_LOWERCASE:
        print(f"Sorry, the program doesn't support {language_start}")
        quit()
    elif language_end != "all" and language_end not in SUPPORTED_LANGUAGES_LOWERCASE:
        print(f"Sorry, the program doesn't support {language_end}")
        quit()
    elif language_end == "all":
        all_language_end = SUPPORTED_LANGUAGES
    else:
        all_language_end = [language_end]

    # Count of examples to print and return in "word".txt file.
    example_count = args.example_count

    # Prompt the user to select starting language and ending language(s), plus a word to translate.
    # language_start, all_language_end, word = get_user_selection()

    # Request session
    my_session = requests.Session()

    # Request data from the translation website
    all_lines = []
    for language_end in all_language_end:
        language_end = language_end.lower()
        if language_start != language_end:
            # Create URL - e.g. https://context.reverso.net/translation/english-french/cheese
            url = f"https://context.reverso.net/translation/{language_start}-{language_end}/{word}"

            # Get the website data
            web_response = my_session.get(url, timeout=10, headers={'User-Agent': USER_AGENT})

            # Evaluate the HTTP status
            status_code = web_response.status_code
            if status_code == 200:
                pass
            elif status_code == 404:
                print(f"Sorry, unable to find {word}")
                quit()
            else:
                # print(f"{status_code}")
                print("Something wrong with your internet connection")

            # Process the response data with beatifulsoup4
            soup = BeautifulSoup(web_response.content, 'html.parser')

            # Find all the translations of the given word to the end language.
            all_word_translations = find_all_word_translations(soup=soup)

            # Find all the example sentences with the translated word in the end language.
            all_example_translation_sentences = find_all_translation_sentence_examples(soup=soup)

            # Print the results in a formatted manner
            current_lines = print_results_formatted(word_examples=all_word_translations,
                                                    sentence_examples=all_example_translation_sentences,
                                                    language_end=language_end, count=example_count)
            all_lines += current_lines

    # Save the results to a "word".txt file.
    path_save_file = PROJECT_ROOT / "translation_dump" / f"{word}.txt"
    with open(path_save_file, "w") as f:
        f.writelines(all_lines)
