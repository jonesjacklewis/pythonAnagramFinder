"""Find all anagrams in a word list
"""
from typing import List, Dict
import requests

def get_words_from_uri(uri: str) -> List[str]:
    """Returns a list of words from a URI

    Args:
        uri (str): A URI to get the words from
    Returns:
        List[str]: A list of words
    """

    response: requests.Response = requests.get(uri)
    text: str = response.text

    response.close()

    words: List[str] = [word.strip() for word in text.split("\n")]

    return words

def convert_to_standard_form(word: str) -> str:
    """Sorts a string alphabetically

    Args:
        word (str): Word to be sorted

    Returns:
        str: The word in alphabetical order
    """
    standard_form: str = "".join(sorted(word))

    return standard_form

def find_anagrams(word_list: List[str]) -> Dict[str, List[str]]:
    """Finds all anagrams in word list by converting to standard form

    Args:
        word_list (List[str]): A list of words to search through

    Returns:
        Dict[str, List[str]]: A dict with the standard form of a word and words matching it
    """
    anagrams: Dict[str, List[str]] = {}

    for word in word_list:
        standard_form = convert_to_standard_form(word)

        if standard_form in anagrams:
            anagrams[standard_form].append(word)
        else:
            anagrams[standard_form] = [word]

    return anagrams

def filter_anagrams_by_number(
        anagrams: Dict[str, List[str]],
        min_count: int = 2
    ) -> Dict[str, List[str]]:
    """Filters the anagram dictionary by finding anagrams which contain a minimum number of words

    Args:
        anagrams (Dict[str, List[str]]): A dict with the standard form of a word + words matching it
        min_count (int, optional): The minimum number of words to match. Defaults to 2.

    Returns:
        Dict[str, List[str]]: Dict filtered to the specified count
    """
    filtered: Dict[str, List[str]] = {
        key:value
        for key, value in anagrams.items()
        if len(value) >= min_count
    }

    return filtered

def get_most_anagram(anagrams: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Find the words with the most number of anagrams

    Args:
        anagrams (Dict[str, List[str]]): List of all anagrams

    Returns:
        Dict[str, List[str]]: Most anagrams
    """
    most_anagrams: int = max(len(anagram) for anagram in anagrams.values())

    filtered: Dict[str, List[str]] = {
        key:value
        for key, value in anagrams.items()
        if len(value) == most_anagrams
    }

    return filtered

def main() -> None:
    """Main method
    """

    word_list_uri: str = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"

    words: List[str] = get_words_from_uri(word_list_uri)

    anagrams: Dict[str, List[str]] = find_anagrams(words)

    most_anagrams = get_most_anagram(anagrams)

    for standard_form, word_list in most_anagrams.items():
        print(standard_form)
        print(word_list)
        print(len(word_list))
        print("############")

if __name__ == "__main__":
    main()
