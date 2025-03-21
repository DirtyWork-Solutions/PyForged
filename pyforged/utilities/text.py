"""
This module provides utilities for working with text/strings such as converting strings into various naming conventions
(commonly referred to as "cases"), including but not limited to:
- snake_case
- camelCase
- PascalCase
- kebab-case
- SCREAMING-KEBAB-CASE
- COBOL-CASE (alias)
- Train-Case
- Title Case
- dot.case
- space case
- slash/case
- backslash\case
- mixed delimiter case
"""

import re

class CaseTransformer:
    """
    A utility class that transforms input strings into various casing styles.

    Usage:
        CaseTransformer.to_snake_case("MyExampleString")  -> "my_example_string"
        CaseTransformer.to_pascal_case("my_example_string") -> "MyExampleString"
    """

    @staticmethod
    def to_snake_case(text: str) -> str:
        """
        Converts the input text to snake_case.

        Example:
            "MyTestString" -> "my_test_string"
        """
        return "_".join(CaseTransformer._normalize_text(text)).lower()

    @staticmethod
    def to_upper_snake_case(text: str) -> str:
        """
        Converts the input text to UPPER_SNAKE_CASE.

        Example:
            "MyTestString" -> "MY_TEST_STRING"
        """
        return "_".join(CaseTransformer._normalize_text(text)).upper()

    @staticmethod
    def to_camel_case(text: str) -> str:
        """
        Converts the input text to camelCase.

        Example:
            "MyTestString" -> "myTestString"
        """
        words = CaseTransformer._normalize_text(text)
        return words[0].lower() + "".join(w.capitalize() for w in words[1:])

    @staticmethod
    def to_pascal_case(text: str) -> str:
        """
        Converts the input text to PascalCase.

        Example:
            "my_test_string" -> "MyTestString"
        """
        return "".join(w.capitalize() for w in CaseTransformer._normalize_text(text))

    @staticmethod
    def to_kebab_case(text: str) -> str:
        """
        Converts the input text to kebab-case (lowercase words joined with dashes).

        Example:
            "MyTestString" -> "my-test-string"
        """
        return "-".join(CaseTransformer._normalize_text(text)).lower()

    @staticmethod
    def to_screaming_kebab_case(text: str) -> str:
        """
        Converts the input text to SCREAMING-KEBAB-CASE (uppercase words joined with dashes).

        Example:
            "MyTestString" -> "MY-TEST-STRING"
        """
        return "-".join(CaseTransformer._normalize_text(text)).upper()

    @staticmethod
    def to_cobol_case(text: str) -> str:
        """
        Alias for SCREAMING-KEBAB-CASE. Used in legacy or enterprise systems.

        Example:
            "MyTestString" -> "MY-TEST-STRING"
        """
        return CaseTransformer.to_screaming_kebab_case(text)

    @staticmethod
    def to_train_case(text: str) -> str:
        """
        Converts the input text to Train-Case (Pascal-style kebab-case).

        Example:
            "my_test_string" -> "My-Test-String"
        """
        return "-".join(w.capitalize() for w in CaseTransformer._normalize_text(text))

    @staticmethod
    def to_title_case(text: str) -> str:
        """
        Converts the input text to Title Case (each word capitalized and space-separated).

        Example:
            "my_test_string" -> "My Test String"
        """
        return " ".join(w.capitalize() for w in CaseTransformer._normalize_text(text))

    @staticmethod
    def to_dot_case(text: str) -> str:
        """
        Converts the input text to dot.case (lowercase words joined with periods).

        Example:
            "MyTestString" -> "my.test.string"
        """
        return ".".join(CaseTransformer._normalize_text(text)).lower()

    @staticmethod
    def to_space_case(text: str) -> str:
        """
        Converts the input text to space case (lowercase words separated by spaces).

        Example:
            "MyTestString" -> "my test string"
        """
        return " ".join(CaseTransformer._normalize_text(text)).lower()

    @staticmethod
    def to_slash_case(text: str) -> str:
        """
        Converts the input text to slash/case (words separated by slashes).

        Example:
            "MyTestString" -> "my/test/string"
        """
        return "/".join(CaseTransformer._normalize_text(text)).lower()

    @staticmethod
    def to_backslash_case(text: str) -> str:
        """
        Converts the input text to backslash\case (words separated by backslashes).

        Example:
            "MyTestString" -> "my\\test\\string"
        """
        return "\\".join(CaseTransformer._normalize_text(text)).lower()

    @staticmethod
    def to_mixed_delimiter_case(text: str) -> str:
        """
        Converts the input text into a quirky mixed-delimiter format:
        Underscore for first word, dash for second, dot for the rest.

        Example:
            "MyTestString" -> "my-test.string"
        """
        cleaned = CaseTransformer._normalize_text(text)
        if len(cleaned) > 2:
            return "_".join(cleaned[:1]) + "-" + cleaned[1] + "." + ".".join(cleaned[2:])
        elif len(cleaned) == 2:
            return "_".join(cleaned[:1]) + "-" + cleaned[1]
        return "_".join(cleaned)

    @staticmethod
    def _normalize_text(text: str) -> list:
        """
        Internal utility method to normalize and split text into words:
        - Converts delimiters (underscore, hyphen, dot, slash, backslash) to spaces
        - Splits camelCase and PascalCase
        - Lowercases and splits into a list of words

        Example:
            "myTestString-Example" -> ['my', 'test', 'string', 'example']
        """
        text = re.sub(r'[_\-.\\/]', ' ', text)
        text = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', text)
        text = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', ' ', text)
        return text.lower().split()


# 1. Slug Generator
def slugify(text: str) -> str:
    """
    Converts a given text to a URL-friendly slug.

    Args:
        text (str): The input text to be slugified.

    Returns:
        str: The slugified version of the input text.
    """
    return re.sub(r'[^a-zA-Z0-9]+', '-', text.lower()).strip('-')

# 2.


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