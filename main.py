"""Find all anagrams in a word list
"""
import os
from datetime import datetime, timedelta
from typing import List, Dict
import requests


def check_if_file_newer_than_x_days(path: str, max_days_old: int = 7) -> bool:
    """Checks if a file is newer than a specified number of days

    Args:
        path (str): A path to a file
        days (int, optional): Number of days. Defaults to 7.

    Returns:
        bool: True if the file is newer than the specified number of days, False otherwise
    """

    if not os.path.exists(path):
        return False

    file_timestamp: datetime = datetime.fromtimestamp(os.path.getmtime(path))
    current_timestamp: datetime = datetime.now()

    return file_timestamp + timedelta(days=max_days_old) > current_timestamp


def get_words_from_uri(words_uri: str, words_filename: str = "words.txt") -> None:
    """Returns a list of words from a URI

    Args:
        uri (str): A URI to get the words from
    Returns:
        List[str]: A list of words
    """
    words_uri_response: requests.Response = requests.get(words_uri)
    words_uri_text: str = words_uri_response.text

    words_uri_response.close()

    word_list: List[str] = [word.strip() + "\n" for word in words_uri_text.split("\n")]

    with open(words_filename, "w", encoding="utf-8") as file:
        file.writelines(word_list)


def get_words_from_file(words_path: str) -> List[str]:
    """Returns a list of words from a file

    Args:
        path (str): A path to a file
    Returns:
        List[str]: A list of words
    """
    with open(words_path, "r", encoding="utf-8") as file:
        word_list: List[str] = [word.strip() for word in file.readlines()]

    return word_list


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
    anagrams_dict: Dict[str, List[str]] = {}

    for word in word_list:
        standard_form: str = convert_to_standard_form(word)

        if standard_form in anagrams_dict:
            anagrams_dict[standard_form].append(word)
        else:
            anagrams_dict[standard_form] = [word]

    return anagrams_dict


def filter_anagrams_by_number(
    anagrams: Dict[str, List[str]], min_count: int = 2
) -> Dict[str, List[str]]:
    """Filters the anagram dictionary by finding anagrams which contain a minimum number of words

    Args:
        anagrams (Dict[str, List[str]]): A dict with the standard form of a word + words matching it
        min_count (int, optional): The minimum number of words to match. Defaults to 2.

    Returns:
        Dict[str, List[str]]: Dict filtered to the specified count
    """
    filtered_anagrams: Dict[str, List[str]] = {
        standard_form: anagram_list
        for standard_form, anagram_list in anagrams.items()
        if len(anagram_list) >= min_count
    }

    return filtered_anagrams


def get_most_anagram(anagrams: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Find the words with the most number of anagrams

    Args:
        anagrams (Dict[str, List[str]]): List of all anagrams

    Returns:
        Dict[str, List[str]]: Most anagrams
    """
    most_anagrams: int = max(len(anagram) for anagram in anagrams.values())

    filtered_anagrams: Dict[str, List[str]] = {
        standard_form: anagram_list
        for standard_form, anagram_list in anagrams.items()
        if len(anagram_list) == most_anagrams
    }

    return filtered_anagrams


def get_longest_anagram(anagrams: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Find the words with the longest anagrams

    Args:
        anagrams (Dict[str, List[str]]): List of all anagrams

    Returns:
        Dict[str, List[str]]: Longest anagrams
    """

    longest_word_length: int = max(
        len(word)
        for word in anagrams.keys()
        if len(anagrams[word]) > 1
    )

    filtered_anagrams: Dict[str, List[str]] = {
        standard_form: anagram_list
        for standard_form, anagram_list in anagrams.items()
        if len(standard_form) == longest_word_length and len(anagram_list) > 1
    }

    return filtered_anagrams


def main() -> None:
    """Main method"""

    if not os.path.exists("words.txt") or not check_if_file_newer_than_x_days(
        "words.txt"
    ):
        word_list_uri: str = (
            "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
        )

        get_words_from_uri(word_list_uri)

    word_list: List[str] = get_words_from_file("words.txt")

    anagrams: Dict[str, List[str]] = find_anagrams(word_list)

    most_anagrams: Dict[str, List[str]] = get_most_anagram(anagrams)

    longest_anagrams: Dict[str, List[str]] = get_longest_anagram(anagrams)

    print("Most anagrams:")
    for standard_form, anagram_list in most_anagrams.items():
        print(f"{standard_form}: {anagram_list}")

    print("Longest anagrams:")
    for standard_form, anagram_list in longest_anagrams.items():
        print(f"{standard_form}: {anagram_list}")


if __name__ == "__main__":
    main()
