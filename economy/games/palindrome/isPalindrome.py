#
# A Leetcode problem #125 for valid palindrome
# https://leetcode.com/problems/valid-palindrome/
#
# Time Complexity: O(n)
# Space Complexity: O(1)
#


def isPalindrome(word: str) -> bool:
    """
    Checks if a given strong is the same forward and backwards. If it is, return true, else return false

    :param word: a string where the word will be checked
    :return: True if palindrome else False
    """
    # Variables
    length_word = len(word)
    left_string = 0
    right_string = length_word - 1

    # While loop while left is less than right
    while left_string < right_string:
        # continue and increment left total if it is not alphanumeric
        if not word[left_string].isalnum():
            left_string += 1
            continue

        # continue and decrement right total if it is not alphanumeric
        if not word[right_string].isalnum():
            right_string -= 1
            continue

        # Check if the left does not match the right. Ignore cases here
        if word[left_string].lower() != word[right_string].lower():
            return False

        # Increment and decrement left and right
        left_string += 1
        right_string -= 1

    # return True if left matches right
    return True
