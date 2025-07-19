#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int validate_text(string text);
int check_subsequent_spaces(string text);
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int compute_coleman_liau_index(float l, float s);
void print_grade(int coleman_liau_index);

int no_words_err_code = 1;
int leading_space_err_code = 2;
int tailing_space_err_code = 3;
int sonsecutive_spaces_err_code = 4;

int main(void)
{
    string text = get_string("Text: ");

    int validation_result = validate_text(text);

    if (validation_result != 0)
    {
        return validation_result;
    }

    int letter_count = count_letters(text);
    int word_count = count_words(text);
    int sentence_count = count_sentences(text);

    float average_letters = (letter_count * 100.0) / word_count;
    float average_sentences = (sentence_count * 100.0) / word_count;

    int coleman_liau_index = compute_coleman_liau_index(average_letters, average_sentences);

    print_grade(coleman_liau_index);
}

int validate_text(string text)
{
    int text_length = strlen(text);

    if (text_length == 0)
    {
        printf("Text must have at least one word\n");
        return no_words_err_code;
    }

    if (isspace(text[0]))
    {
        printf("Text can't start with space character\n");
        return leading_space_err_code;
    }

    if (isspace(text[text_length - 1]))
    {
        printf("Text can't end with space character\n");
        return tailing_space_err_code;
    }

    int consecutive_spaces_result = check_subsequent_spaces(text);

    if (consecutive_spaces_result > 0)
    {
        printf("Text must contain only single space characters between words\n");
        return consecutive_spaces_result;
    }

    return 0;
}

int check_subsequent_spaces(string text)
{
    int text_length = strlen(text);

    int is_space = 0;
    for (int i = 0; i < text_length; i++)
    {
        char c = text[i];

        if (isspace(c))
        {
            is_space++;
        }
        else if (is_space > 1)
        {
            return sonsecutive_spaces_err_code;
        }
        else
        {
            is_space = 0;
        }
    }

    return 0;
}

int count_letters(string text)
{
    int text_length = strlen(text);

    int letter_count = 0;

    for (int i = 0; i < text_length; i++)
    {
        char c = text[i];
        if (isalpha(c))
        {
            letter_count++;
        }
    }

    return letter_count;
}

int count_words(string text)
{
    int text_length = strlen(text);

    int word_count = 0;

    if (text_length > 0)
    {
        word_count++;
    }

    for (int i = 0; i < text_length; i++)
    {
        char c = text[i];
        if (c == ' ')
        {
            word_count++;
        }
    }

    return word_count;
}

int count_sentences(string text)
{
    int text_length = strlen(text);

    int sentence_count = 0;

    for (int i = 0; i < text_length; i++)
    {
        char c = text[i];
        if (c == '.' || c == '?' || c == '!')
        {
            sentence_count++;
        }
    }

    return sentence_count;
}

int compute_coleman_liau_index(float l, float s)
{
    float index = 0.0588 * l - 0.296 * s - 15.8;

    int rounded = (int) (index + 0.5f);

    return rounded;
}

void print_grade(int coleman_liau_index)
{
    if (coleman_liau_index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (coleman_liau_index >= 1 && coleman_liau_index <= 16)
    {
        printf("Grade %d\n", coleman_liau_index);
    }
    else if (coleman_liau_index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade invalid\n");
    }
}
