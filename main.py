"""Find all anagrams in a word list
"""
import os
from datetime import datetime, timedelta
from typing import List, Dict
import requests

def check_if_file_exists(path: str) -> bool:
    """Checks if a file exists

    Args:
        path (str): A path to a file

    Returns:
        bool: True if the file exists, False otherwise
    """
    try:
        with open(path, "r", encoding = "utf-8") as _:
            return True
    except FileNotFoundError:
        return False

def check_if_file_newer_than_x_days(path: str, days: int = 7) -> bool:
    """Checks if a file is newer than a specified number of days

    Args:
        path (str): A path to a file
        days (int, optional): Number of days. Defaults to 7.

    Returns:
        bool: True if the file is newer than the specified number of days, False otherwise
    """

    if not check_if_file_exists(path):
        return False

    file_timestamp: datetime = datetime.fromtimestamp(os.path.getmtime(path))
    current_timestamp: datetime = datetime.now()

    if file_timestamp + timedelta(days = days) > current_timestamp:
        return True
    return False

def get_words_from_uri(uri: str, filename: str = "words.txt") -> None:
    """Returns a list of words from a URI

    Args:
        uri (str): A URI to get the words from
    Returns:
        List[str]: A list of words
    """
    print("From URI")
    response: requests.Response = requests.get(uri)
    text: str = response.text

    response.close()

    words: List[str] = [word.strip() + "\n" for word in text.split("\n")]

    with open(filename, "w", encoding = "utf-8") as file:
        file.writelines(words)

def get_words_from_file(path: str) -> List[str]:
    """Returns a list of words from a file

    Args:
        path (str): A path to a file
    Returns:
        List[str]: A list of words
    """
    print("From File")
    with open(path, "r", encoding = "utf-8") as file:
        words: List[str] = [word.strip() for word in file.readlines()]

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
    anagrams: Dict[str, List[str]], min_count: int = 2
) -> Dict[str, List[str]]:
    """Filters the anagram dictionary by finding anagrams which contain a minimum number of words

    Args:
        anagrams (Dict[str, List[str]]): A dict with the standard form of a word + words matching it
        min_count (int, optional): The minimum number of words to match. Defaults to 2.

    Returns:
        Dict[str, List[str]]: Dict filtered to the specified count
    """
    filtered: Dict[str, List[str]] = {
        key: value for key, value in anagrams.items() if len(value) >= min_count
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
        key: value for key, value in anagrams.items() if len(value) == most_anagrams
    }

    return filtered


def get_longest_anagram(anagrams: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Find the words with the longest anagrams

    Args:
        anagrams (Dict[str, List[str]]): List of all anagrams

    Returns:
        Dict[str, List[str]]: Longest anagrams
    """

    longest_word_length: int = max(
        len(word) for word in anagrams.keys() if len(anagrams[word]) > 1
    )

    filtered: Dict[str, List[str]] = {
        key: value
        for key, value in anagrams.items()
        if len(key) == longest_word_length and len(value) > 1
    }

    return filtered


def main() -> None:
    """Main method"""

    if not check_if_file_exists("words.txt") or not check_if_file_newer_than_x_days("words.txt"):
        word_list_uri: str = (
            "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
        )

        get_words_from_uri(word_list_uri)

    words: List[str] = get_words_from_file("words.txt")

    anagrams: Dict[str, List[str]] = find_anagrams(words)

    most_anagrams: Dict[str, List[str]] = get_most_anagram(anagrams)

    longest_anagrams: Dict[str, List[str]] = get_longest_anagram(anagrams)

    print("Most anagrams:")
    for key, value in most_anagrams.items():
        print(f"{key}: {value}")

    print("Longest anagrams:")
    for key, value in longest_anagrams.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
