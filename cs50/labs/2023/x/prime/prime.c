#include <cs50.h>
#include <math.h>
#include <stdio.h>

bool prime(int number);
bool prime_1(int number);
bool prime_2(int number);

int main(void)
{
    int min;
    do
    {
        min = get_int("Minimum: ");
    }
    while (min < 1);

    int max;
    do
    {
        max = get_int("Maximum: ");
    }
    while (min >= max);

    for (int i = min; i <= max; i++)
    {
        if (prime(i))
        {
            printf("%i\n", i);
        }
    }
}

bool prime(int number)
{
    return prime_2(number);
}

bool prime_1(int number)
{
    if (number <= 2)
    {
        return true;
    }

    for (int i = 2; i < number; i++)
    {
        if (number % i == 0)
        {
            return false;
        }
    }

    return true;
}

bool prime_2(int number)
{
    if (number <= 2)
    {
        return true;
    }

    int square_root = sqrt(number);


    for (int i = 2; i <= square_root; i++)
    {
        if (number % i == 0)
        {
            return false;
        }
    }

    return true;
}
