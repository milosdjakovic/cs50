#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

string get_valid_key(int argc, char *argv[]);
void hasRepeatedChars(string str);
string encypher(string key, string plaintext);
void string_to_lower(string s);

int main(int argc, char *argv[])
{
    string key = get_valid_key(argc, argv);

    string plaintext = get_string("plaintext:  ");
    string cyphertext = encypher(key, plaintext);

    printf("ciphertext: %s\n", cyphertext);

    return 0;
}

string get_valid_key(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Provide exactly 1 key as an argument.\n");
        exit(1);
    }

    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isalpha(argv[1][i]))
        {
            printf("Usage: ./substitution KEY\n");
            exit(1);
        }
    }

    int key_length = strlen(argv[1]);

    if (key_length != 26)
    {
        printf("Key must contain 26 characters.\n");
        exit(1);
    }

    for (int i = 0; i < strlen(argv[1]); i++)
    {

        if (!isalpha(argv[1][i]))
        {
            printf("Usage: ./substitution KEY\n");
            exit(1);
        }
    }

    hasRepeatedChars(argv[1]);

    return argv[1];
}

void hasRepeatedChars(string str)
{
    char originalChars[26] = {0};
    int len = strlen(str);
    int originalCharsCount = 0;

    for (int i = 0; i < len; i++)
    {
        originalChars[originalCharsCount] = str[i];
        originalCharsCount++;
    }

    for (int i = 0; i < originalCharsCount; i++)
    {
        for (int j = i + 1; j < originalCharsCount; j++)
        {
            if (tolower(originalChars[i]) == tolower(originalChars[j]))
            {
                printf("Key must not contain repeated characters.\n");
                exit(1);
            }
        }
    }
}

string encypher(string key, string plaintext)
{
    int key_length = strlen(key);
    int plaintext_length = strlen(plaintext);

    string_to_lower(key);

    for (int i = 0; i < plaintext_length; i++)
    {
        int pc = plaintext[i];

        if (pc >= 65 && pc <= 90)
        {
            int pci = pc - 65;

            char kc = key[pci];

            plaintext[i] = toupper(kc);
        }

        if (pc >= 97 && pc <= 122)
        {
            int pci = pc - 97;

            char kc = key[pci];

            plaintext[i] = tolower(kc);
        }
    }

    return plaintext;
}

void string_to_lower(string s)
{
    for (int i = 0; i < strlen(s); i++)
    {
        s[i] = tolower(s[i]);
    }
}
