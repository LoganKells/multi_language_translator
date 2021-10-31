# Multi Language Translator

## Running the translator in command line
Run the python command, which will translate a given word to one, or all supported languages. 
A .txt file will be saved in *./translation_dump* containing all translations of the word plus 
example sentences translated with the word included.

    translator.py will translate a word from start to end language.

    positional arguments:
      language_start        Starting language for translation. Example "english".
      language_end          Ending language for translation. Use 'all' to translate to all available languages. Example: "spanish".
      word                  Word to translate. Example "hello".

    optional arguments:
      -h, --help            show this help message and exit
      --example_count EXAMPLE_COUNT
                            Number of example translations to return.

For example, the following command will translate "what" from English to Arabic. 

    python translator.py english arabic what

The file "what.txt" is saved with the following contents in *./translation_dump*.

    Arabic Translations:
    translation
    ما
    
    Arabic Examples:
    FBI! Everyone stop what what you're doing!
    مكتب التحقيقات الفدرالي الجميع أوقفوا ما تفعلونه
    Only what what are the little lord wants to hear.
    فقط ما يريد أن يسمعه اللورد الصغير

## Installation
See the requirements in *./requirements.txt*.
    
    requirements.txt