// Check that a password has at least one lowercase letter, uppercase letter, number and symbol
// Practice iterating through a string
// Practice using the ctype library

#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

bool valid(string password);

int main(void)
{
    string password = get_string("Enter your password: ");
    if (valid(password))
    {
        printf("Your password is valid!\n");
    }
    else
    {
        printf("Your password needs at least one uppercase letter, lowercase letter, number and "
               "symbol\n");
    }
}

// TODO: Complete the Boolean function below
bool valid(string password)
{
    int pass_len = strlen(password);

    int upper = 0;
    int lower = 0;
    int digit = 0;
    int symbol = 0;

    for (int i = 0; i < pass_len; i++)
    {
        char c = password[i];

        if (islower(c))
        {
            upper++;
        }

        if (isupper(c))
        {
            lower++;
        }

        if (isdigit(c))
        {
            digit++;
        }

        if (ispunct(c))
        {
            symbol++;
        }
    }

    if (upper > 0 && lower > 0 && digit > 0 && symbol > 0)
    {
        return true;
    }

    return false;
}
