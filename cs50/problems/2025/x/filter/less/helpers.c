#include <math.h>
#include <stdio.h>

#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            BYTE average =
                (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed + 1) / 3;

            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }

    return;
}

typedef struct
{
    float red;
    float green;
    float blue;
} Modifier;

BYTE calculate_sepia_channel(Modifier m, RGBTRIPLE pixel)
{
    float sepia_red = m.red * pixel.rgbtRed;
    float sepia_green = m.green * pixel.rgbtGreen;
    float sepia_blue = m.blue * pixel.rgbtBlue;

    int sepia_value = round(sepia_red + sepia_green + sepia_blue);

    if (sepia_value > 255)
    {
        sepia_value = 255;
    }

    return (BYTE) sepia_value;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            Modifier sepia_red_modifiers = {.393, .769, .189};
            Modifier sepia_green_modifiers = {.349, .686, .168};
            Modifier sepia_blue_modifiers = {.272, .534, .131};

            BYTE sepia_red = calculate_sepia_channel(sepia_red_modifiers, image[i][j]);
            BYTE sepia_green = calculate_sepia_channel(sepia_green_modifiers, image[i][j]);
            BYTE sepia_blue = calculate_sepia_channel(sepia_blue_modifiers, image[i][j]);

            image[i][j].rgbtRed = sepia_red;
            image[i][j].rgbtGreen = sepia_green;
            image[i][j].rgbtBlue = sepia_blue;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        int width_half = width / 2;

        RGBTRIPLE start_p;
        RGBTRIPLE end_p;

        for (int j = 0; j < width_half; j++)
        {
            start_p = image[i][j];
            end_p = image[i][width - 1 - j];

            image[i][j] = end_p;
            image[i][width - 1 - j] = start_p;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE box[3][3] = {{copy[i - 1][j - 1], copy[i - 1][j], copy[i - 1][j + 1]},
                                   {copy[i][j - 1], copy[i][j], copy[i][j + 1]},
                                   {copy[i + 1][j - 1], copy[i + 1][j], copy[i + 1][j + 1]}};

            int blue = 0;
            int green = 0;
            int red = 0;

            int has_top_row = i != 0;
            int has_bottom_row = i != height - 1;
            int has_left_column = j != 0;
            int has_right_column = j != width - 1;

            int count = 0;

            // [0][0]
            if (has_top_row && has_left_column)
            {
                blue += box[0][0].rgbtBlue;
                green += box[0][0].rgbtGreen;
                red += box[0][0].rgbtRed;
                count++;
            }

            // [0][1]
            if (has_top_row)
            {
                blue += box[0][1].rgbtBlue;
                green += box[0][1].rgbtGreen;
                red += box[0][1].rgbtRed;
                count++;
            }

            // [0][2]
            if (has_top_row && has_right_column)
            {
                blue += box[0][2].rgbtBlue;
                green += box[0][2].rgbtGreen;
                red += box[0][2].rgbtRed;
                count++;
            }

            // [1][0]
            if (has_left_column)
            {
                blue += box[1][0].rgbtBlue;
                green += box[1][0].rgbtGreen;
                red += box[1][0].rgbtRed;
                count++;
            }

            // [1][1]
            blue += box[1][1].rgbtBlue;
            green += box[1][1].rgbtGreen;
            red += box[1][1].rgbtRed;
            count++;

            // [1][2]
            if (has_right_column)
            {
                blue += box[1][2].rgbtBlue;
                green += box[1][2].rgbtGreen;
                red += box[1][2].rgbtRed;
                count++;
            }

            // [2][0]
            if (has_bottom_row && has_left_column)
            {
                blue += box[2][0].rgbtBlue;
                green += box[2][0].rgbtGreen;
                red += box[2][0].rgbtRed;
                count++;
            }

            // [2][1]
            if (has_bottom_row)
            {
                blue += box[2][1].rgbtBlue;
                green += box[2][1].rgbtGreen;
                red += box[2][1].rgbtRed;
                count++;
            }

            // [2][2]
            if (has_bottom_row && has_right_column)
            {
                blue += box[2][2].rgbtBlue;
                green += box[2][2].rgbtGreen;
                red += box[2][2].rgbtRed;
                count++;
            }

            int avg_blue = round((float) blue / count);
            int avg_green = round((float) green / count);
            int avg_red = round((float) red / count);

            image[i][j].rgbtBlue = avg_blue;
            image[i][j].rgbtGreen = avg_green;
            image[i][j].rgbtRed = avg_red;
        }
    }

    return;
}
