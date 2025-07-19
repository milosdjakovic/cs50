#include <cs50.h>
#include <stdio.h>

void draw_pyramid(int size);
void draw_row(int spaces, int bricks);

int main(void)
{
    int height;

    height = get_int("Height: ");

    while (height < 1 || height > 8)
    {
        printf("The value of the height must be between 1 and 8.\n");
        height = get_int("Height: ");
    }

    draw_pyramid(height);
}

void draw_pyramid(int size)
{
    for (int i = 0; i < size; i++)
    {
        int spaces = size - 1 - i;
        int bricks = i + 1;

        draw_row(spaces, bricks);
    }
}

void draw_row(int spaces, int bricks)
{
    for (int i = 0; i < spaces; i++)
    {
        printf(" ");
    }
    for (int i = 0; i < bricks; i++)
    {
        printf("#");
    }
    printf("\n");
}
