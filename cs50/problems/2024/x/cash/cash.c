#include <cs50.h>
#include <stdio.h>

void count_coins(int change);

int main(void)
{

    int change;

    do
    {
        change = get_int("Change owed: ");
    }
    while (change < 0);

    count_coins(change);
}

void count_coins(int change)
{
    int quater_value = 25;
    int dime_value = 10;
    int nickel_value = 5;
    int penny_value = 1;

    int quater_count = 0;
    int dime_count = 0;
    int nickel_count = 0;
    int penny_count = 0;

    while (change > 0)
    {
        if (change >= quater_value)
        {
            change -= quater_value;
            quater_count++;
        }
        else if (change >= dime_value)
        {
            change -= dime_value;
            dime_count++;
        }
        else if (change >= nickel_value)
        {
            change -= nickel_value;
            nickel_count++;
        }
        else
        {
            change -= penny_value;
            penny_count++;
        }
    }

    int total_coin_count = quater_count + dime_count + nickel_count + penny_count;

    printf("%i\n", total_coin_count);
}
