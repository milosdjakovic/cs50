#include <cs50.h>
#include <stdio.h>

void validate_card(long card_number);
void verify_luhn_checksum(long card_number, string card_issuer_name);

int main(void)
{
    long card_number;

    card_number = get_long("Card: ");

    validate_card(card_number);
}

void validate_card(long card_number)
{
    // Check Mastercard: 16 digits, starts with 51,52,53,54,55
    if (card_number >= 5100000000000000 && card_number < 5600000000000000)
    {
        verify_luhn_checksum(card_number, "MASTERCARD");
    }
    // Check Amex: 15 digits, starts with 34 or 37
    else if ((card_number >= 340000000000000 && card_number < 350000000000000) ||
             (card_number >= 370000000000000 && card_number < 380000000000000))
    {
        verify_luhn_checksum(card_number, "AMEX");
    }
    // Check Visa: 13 or 16 digits, starts with 4
    else if ((card_number >= 4000000000000 && card_number < 5000000000000) ||
             (card_number >= 4000000000000000 && card_number < 5000000000000000))
    {
        verify_luhn_checksum(card_number, "VISA");
    }
    // Check if Invalid
    else
    {
        printf("INVALID\n");
    }
}

void verify_luhn_checksum(long card_number, string card_issuer_name)
{
    // Extract individual digits from right to left
    int d1 = card_number % 10;
    int d2 = (card_number / 10) % 10;
    int d3 = (card_number / 100) % 10;
    int d4 = (card_number / 1000) % 10;
    int d5 = (card_number / 10000) % 10;
    int d6 = (card_number / 100000) % 10;
    int d7 = (card_number / 1000000) % 10;
    int d8 = (card_number / 10000000) % 10;
    int d9 = (card_number / 100000000) % 10;
    int d10 = (card_number / 1000000000) % 10;
    int d11 = (card_number / 10000000000) % 10;
    int d12 = (card_number / 100000000000) % 10;
    int d13 = (card_number / 1000000000000) % 10;
    int d14 = (card_number / 10000000000000) % 10;
    int d15 = (card_number / 100000000000000) % 10;
    int d16 = (card_number / 1000000000000000) % 10;

    // Luhn's algorithm: Double every second digit from right
    int double_d2 = d2 * 2;
    int double_d4 = d4 * 2;
    int double_d6 = d6 * 2;
    int double_d8 = d8 * 2;
    int double_d10 = d10 * 2;
    int double_d12 = d12 * 2;
    int double_d14 = d14 * 2;
    int double_d16 = d16 * 2;

    // Split and sum digits if product is > 9
    int luhn_sum_d2 = double_d2 > 9 ? (double_d2 % 10) + ((double_d2 / 10) % 10) : double_d2;
    int luhn_sum_d4 = double_d4 > 9 ? (double_d4 % 10) + ((double_d4 / 10) % 10) : double_d4;
    int luhn_sum_d6 = double_d6 > 9 ? (double_d6 % 10) + ((double_d6 / 10) % 10) : double_d6;
    int luhn_sum_d8 = double_d8 > 9 ? (double_d8 % 10) + ((double_d8 / 10) % 10) : double_d8;
    int luhn_sum_d10 = double_d10 > 9 ? (double_d10 % 10) + ((double_d10 / 10) % 10) : double_d10;
    int luhn_sum_d12 = double_d12 > 9 ? (double_d12 % 10) + ((double_d12 / 10) % 10) : double_d12;
    int luhn_sum_d14 = double_d14 > 9 ? (double_d14 % 10) + ((double_d14 / 10) % 10) : double_d14;
    int luhn_sum_d16 = double_d16 > 9 ? (double_d16 % 10) + ((double_d16 / 10) % 10) : double_d16;

    // Sum all doubled digits
    int doubled_digits_sum = luhn_sum_d2 + luhn_sum_d4 + luhn_sum_d6 + luhn_sum_d8 + luhn_sum_d10 +
                             luhn_sum_d12 + luhn_sum_d14 + luhn_sum_d16;

    // Sum remaining digits
    int remaining_digits_sum = d1 + d3 + d5 + d7 + d9 + d11 + d13 + d15;

    // Calculate final sum
    int checksum_total = doubled_digits_sum + remaining_digits_sum;

    // Valid if total is divisible by 10
    int checksum_remainder = checksum_total % 10;
    int is_valid_checksum = checksum_remainder == 0;

    if (is_valid_checksum)
    {
        printf("%s\n", card_issuer_name);
    }
    else
    {
        printf("INVALID\n");
    }
}
