import re

# 7.1 Slug Generator
def slugify(text: str) -> str:
    """
    Converts a given text to a URL-friendly slug.

    Args:
        text (str): The input text to be slugified.

    Returns:
        str: The slugified version of the input text.
    """
    return re.sub(r'[^a-zA-Z0-9]+', '-', text.lower()).strip('-')

# 7.2 Camel Case Converter
def to_camel_case(text: str) -> str:
    """
    Converts a given text to camel case.

    Args:
        text (str): The input text to be converted.

    Returns:
        str: The camel case version of the input text.
    """
    words = re.split(r'[^a-zA-Z0-9]', text)
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

# 7.3 Snake Case Converter
def to_snake_case(text: str) -> str:
    """
    Converts a given text to snake case.

    Args:
        text (str): The input text to be converted.

    Returns:
        str: The snake case version of the input text.
    """
    return re.sub(r'[^a-zA-Z0-9]+', '_', text).lower()

# 7.4 Kebab Case Converter
def to_kebab_case(text: str) -> str:
    """
    Converts a given text to kebab case.

    Args:
        text (str): The input text to be converted.

    Returns:
        str: The kebab case version of the input text.
    """
    return re.sub(r'[^a-zA-Z0-9]+', '-', text).lower()

# 7.5 Regex Utility Collection
COMMON_PATTERNS = {
    "email": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    "url": r"^(https?|ftp)://[^\s/$.?#].[^\s]*$",
    "date": r"^\d{4}-\d{2}-\d{2}$",
    "time": r"^\d{2}:\d{2}(:\d{2})?$",
    "ipv6": r"^([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4}|:)$",
    "hex_color": r"^#?([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$",
    "uuid": r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
    "ssn": r"^\d{3}-\d{2}-\d{4}$",
    "mac_address": r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
}
"""
A collection of common regular expression patterns for various types of data.

Patterns:
    email: Matches a valid email address.
    url: Matches a valid URL.
    date: Matches a date in the format YYYY-MM-DD.
    time: Matches a time in the format HH:MM or HH:MM:SS.
    ipv6: Matches a valid IPv6 address.
    hex_color: Matches a valid hexadecimal color code.
    uuid: Matches a valid UUID.
    ssn: Matches a valid US Social Security Number.
    mac_address: Matches a valid MAC address.
"""

# 7.6 Levenshtein Distance Helper
def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculates the Levenshtein distance between two strings.

    Args:
        s1 (str): The first string.
        s2 (str): The second string.

    Returns:
        int: The Levenshtein distance between the two strings.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

# 7.7 Title Case Converter
def to_title_case(text: str) -> str:
    """
    Converts a given text to title case.

    Args:
        text (str): The input text to be converted.

    Returns:
        str: The title case version of the input text.
    """
    return text.title()

# 7.8 Reverse String
def reverse_string(text: str) -> str:
    """
    Reverses the given text.

    Args:
        text (str): The input text to be reversed.

    Returns:
        str: The reversed version of the input text.
    """
    return text[::-1]

# 7.9 Remove Vowels
def remove_vowels(text: str) -> str:
    """
    Removes all vowels from the given text.

    Args:
        text (str): The input text from which vowels will be removed.

    Returns:
        str: The text without vowels.
    """
    return re.sub(r'[aeiouAEIOU]', '', text)

# 7.10 Count Words
def count_words(text: str) -> int:
    """
    Counts the number of words in the given text.

    Args:
        text (str): The input text to be counted.

    Returns:
        int: The number of words in the input text.
    """
    return len(re.findall(r'\b\w+\b', text))

# 7.11 Check Palindrome
def is_palindrome(text: str) -> bool:
    """
    Checks if the given text is a palindrome.

    Args:
        text (str): The input text to be checked.

    Returns:
        bool: True if the text is a palindrome, False otherwise.
    """
    cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
    return cleaned_text == cleaned_text[::-1]