# Buatlah sebuah fungsi `is_palindrome(s)` yang menerima string `s` dan mengembalikan `True` jika string tersebut palindrome, `False` jika tidak. String palindrome adalah string yang sama jika dibaca dari depan maupun belakang.
# Contoh:
# •	Input: katak
# Output: True
# •	Input: python
# Output: False
# ---

def is_palindrome(s):
    index = len(s)
    for i in s:
        if i == s[len(s) - index]:
            print(i)
        index -= 1

is_palindrome("sarung")