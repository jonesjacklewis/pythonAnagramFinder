# Anagram Finder

The code does the following:
1. Check if the file exists and if it is older than 7 days. If either of these conditions are true, download the file from the URI and save it to a file.
2. Read the contents of the file into a list of strings
3. Find all anagrams in the list of strings by converting each word to a standard form. The standard form is the word with the letters ordered alphabetically.
4. Filter the anagrams by finding anagrams which contain a minimum number of words. The default is 2 words.
5. Find the words with the most number of anagrams.
6. Find the words with the longest anagrams.
7. Print the results out to the console. 