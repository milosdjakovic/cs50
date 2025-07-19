#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

void compute_result(int score1, int score2);
int compute_score(string s);
int get_char_score(char c);
string str_to_lower(string s);

int main(void)
{
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    string lowercase_word1 = str_to_lower(word1);
    string lowercase_word2 = str_to_lower(word2);

    int score1 = compute_score(lowercase_word1);
    int score2 = compute_score(lowercase_word2);

    compute_result(score1, score2);
}

void compute_result(int score1, int score2)
{
    if (score1 > score2)
    {
        printf("Player 1 wins!");
    }

    else if (score1 < score2)
    {
        printf("Player 2 wins!");
    }

    else if (score1 == score2)
    {
        printf("Tie!");
    }

    printf("\n");
}

int compute_score(string s)
{
    int string_size = strlen(s);
    int score = 0;

    for (int i = 0; i < string_size; i++)
    {
        char c = s[i];
        int char_score = get_char_score(c);
        score = score + char_score;
    }

    return score;
}

int get_char_score(char c)
{
    switch (c)
    {
        case 'a':
        case 'e':
        case 'i':
        case 'l':
        case 'n':
        case 'o':
        case 'r':
        case 's':
        case 't':
        case 'u':
            return 1;
        case 'd':
        case 'g':
            return 2;
        case 'b':
        case 'c':
        case 'm':
        case 'p':
            return 3;
        case 'f':
        case 'h':
        case 'v':
        case 'w':
        case 'y':
            return 4;
        case 'k':
            return 5;
        case 'j':
        case 'x':
            return 8;
        case 'q':
        case 'z':
            return 10;
        default:
            return 0;
    }
}

string str_to_lower(string s)
{
    for (int i = 0; s[i] != '\0'; i++)
    {
        s[i] = tolower(s[i]);
    }
    return s;
}
