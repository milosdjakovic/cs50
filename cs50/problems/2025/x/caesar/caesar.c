#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int get_valid_key(int argc, char *argv[]);
string encypher(int key, string plaintext);

int main(int argc, char *argv[])
{

    int key = get_valid_key(argc, argv);
    if (key == -1)
    {
        return 1;
    }

    string plaintext = get_string("plaintext: ");
    string cyphertext = encypher(key, plaintext);

    printf("ciphertext: %s\n", cyphertext);
}

int get_valid_key(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Provide exactly 1 key value as an argument.\n");
        return -1;
    }

    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return -1;
        }
    }

    int key = atoi(argv[1]);

    if (key < 0)
    {
        printf("Key argument must contain non negative number.\n");
        return -1;
    }

    return key;
}

string encypher(int key, string plaintext)
{
    string cyphertext = plaintext;

    int plaintext_length = strlen(plaintext);

    for (int i = 0; i < plaintext_length; i++)
    {
        char c = plaintext[i];

        if (c >= 65 && c <= 90)
        {
            int cypher_char = ((c - 65 + key) % 26) + 65;
            cyphertext[i] = cypher_char;
        }

        if (c >= 97 && c <= 122)
        {
            int cypher_char = ((c - 97 + key) % 26) + 97;
            cyphertext[i] = cypher_char;
        }
    }

    return cyphertext;
}
