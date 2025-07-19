#include <cs50.h>
#include <stdio.h>

void draw_level(int height);
void draw_line(int spaces, int bricks);

int main(void)
{
    int height;

    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    draw_level(height);
}

void draw_level(int height)
{
    for (int i = 1; i <= height; i++)
    {
        int spaces = height - i;
        int bricks = i;

        draw_line(spaces, bricks);
    }
}

void draw_line(int spaces, int bricks)
{
    for (int i = 0; i < spaces; i++)
    {
        printf(" ");
    }

    for (int i = 0; i < bricks; i++)
    {
        printf("#");
    }

    printf("  ");

    for (int i = 0; i < bricks; i++)
    {
        printf("#");
    }

    printf("\n");
}
