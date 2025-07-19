// Write a function to replace vowels with numbers
// Get practice with strings
// Get practice with command line
// Get practice with switch

#include <cs50.h>
#include <stdio.h>
#include <string.h>

string replace(string word);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
      printf("Usage: ./no-vowels <word>");
      return 1;
    }

    string word = argv[1];
    printf("word: %s\n", word);

    string leet_word = replace(word);
    printf("leet_word: %s\n", leet_word);
}

string replace(string word)
{
  int word_length = strlen(word);

  for (int i = 0; i < word_length; i++)
  {
    char c = word[i];

    if (c == 'a' || c == 'A')
    {
      word[i] = '6';
    }

    if (c == 'e' || c == 'E')
    {
      word[i] = '3';
    }

    if (c == 'i' || c == 'I')
    {
      word[i] = '1';
    }

    if (c == 'o' || c == 'O')
    {
      word[i] = '0';
    }
  }

  return word;
}
