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

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    int gx[3][3] = {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1},
    };

    int gy[3][3] = {
        {-1, -2, -1},
        {0, 0, 0},
        {1, 2, 1},
    };

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE box[3][3] = {{copy[i - 1][j - 1], copy[i - 1][j], copy[i - 1][j + 1]},
                                   {copy[i][j - 1], copy[i][j], copy[i][j + 1]},
                                   {copy[i + 1][j - 1], copy[i + 1][j], copy[i + 1][j + 1]}};

            int gx_blue = 0;
            int gx_green = 0;
            int gx_red = 0;

            int gy_blue = 0;
            int gy_green = 0;
            int gy_red = 0;

            int has_top_row = i != 0;
            int has_bottom_row = i != height - 1;
            int has_left_column = j != 0;
            int has_right_column = j != width - 1;

            // [0][0]
            if (has_top_row && has_left_column)
            {
                gx_blue += box[0][0].rgbtBlue * gx[0][0];
                gx_green += box[0][0].rgbtGreen * gx[0][0];
                gx_red += box[0][0].rgbtRed * gx[0][0];

                gy_blue += box[0][0].rgbtBlue * gy[0][0];
                gy_green += box[0][0].rgbtGreen * gy[0][0];
                gy_red += box[0][0].rgbtRed * gy[0][0];
            }
            else
            {
                gx_blue += 0 * gx[0][0];
                gx_green += 0 * gx[0][0];
                gx_red += 0 * gx[0][0];

                gy_blue += 0 * gy[0][0];
                gy_green += 0 * gy[0][0];
                gy_red += 0 * gy[0][0];
            }

            // [0][1]
            if (has_top_row)
            {
                gx_blue += box[0][1].rgbtBlue * gx[0][1];
                gx_green += box[0][1].rgbtGreen * gx[0][1];
                gx_red += box[0][1].rgbtRed * gx[0][1];

                gy_blue += box[0][1].rgbtBlue * gy[0][1];
                gy_green += box[0][1].rgbtGreen * gy[0][1];
                gy_red += box[0][1].rgbtRed * gy[0][1];
            }
            else
            {
                gx_blue += 0 * gx[0][1];
                gx_green += 0 * gx[0][1];
                gx_red += 0 * gx[0][1];

                gy_blue += 0 * gy[0][1];
                gy_green += 0 * gy[0][1];
                gy_red += 0 * gy[0][1];
            }

            // [0][2]
            if (has_top_row && has_right_column)
            {
                gx_blue += box[0][2].rgbtBlue * gx[0][2];
                gx_green += box[0][2].rgbtGreen * gx[0][2];
                gx_red += box[0][2].rgbtRed * gx[0][2];

                gy_blue += box[0][2].rgbtBlue * gy[0][2];
                gy_green += box[0][2].rgbtGreen * gy[0][2];
                gy_red += box[0][2].rgbtRed * gy[0][2];
            }
            else
            {
                gx_blue += 0 * gx[0][2];
                gx_green += 0 * gx[0][2];
                gx_red += 0 * gx[0][2];

                gy_blue += 0 * gy[0][2];
                gy_green += 0 * gy[0][2];
                gy_red += 0 * gy[0][2];
            }

            // [1][0]
            if (has_left_column)
            {
                gx_blue += box[1][0].rgbtBlue * gx[1][0];
                gx_green += box[1][0].rgbtGreen * gx[1][0];
                gx_red += box[1][0].rgbtRed * gx[1][0];

                gy_blue += box[1][0].rgbtBlue * gy[1][0];
                gy_green += box[1][0].rgbtGreen * gy[1][0];
                gy_red += box[1][0].rgbtRed * gy[1][0];
            }
            else
            {
                gx_blue += 0 * gx[1][0];
                gx_green += 0 * gx[1][0];
                gx_red += 0 * gx[1][0];

                gy_blue += 0 * gy[1][0];
                gy_green += 0 * gy[1][0];
                gy_red += 0 * gy[1][0];
            }

            // [1][1]
            gx_blue += box[1][1].rgbtBlue * gx[1][1];
            gx_green += box[1][1].rgbtGreen * gx[1][1];
            gx_red += box[1][1].rgbtRed * gx[1][1];

            gy_blue += box[1][1].rgbtBlue * gy[1][1];
            gy_green += box[1][1].rgbtGreen * gy[1][1];
            gy_red += box[1][1].rgbtRed * gy[1][1];

            // [1][2]
            if (has_right_column)
            {
                gx_blue += box[1][2].rgbtBlue * gx[1][2];
                gx_green += box[1][2].rgbtGreen * gx[1][2];
                gx_red += box[1][2].rgbtRed * gx[1][2];

                gy_blue += box[1][2].rgbtBlue * gy[1][2];
                gy_green += box[1][2].rgbtGreen * gy[1][2];
                gy_red += box[1][2].rgbtRed * gy[1][2];
            }
            else
            {
                gx_blue += 0 * gx[1][2];
                gx_green += 0 * gx[1][2];
                gx_red += 0 * gx[1][2];

                gy_blue += 0 * gy[1][2];
                gy_green += 0 * gy[1][2];
                gy_red += 0 * gy[1][2];
            }

            // [2][0]
            if (has_bottom_row && has_left_column)
            {
                gx_blue += box[2][0].rgbtBlue * gx[2][0];
                gx_green += box[2][0].rgbtGreen * gx[2][0];
                gx_red += box[2][0].rgbtRed * gx[2][0];

                gy_blue += box[2][0].rgbtBlue * gy[2][0];
                gy_green += box[2][0].rgbtGreen * gy[2][0];
                gy_red += box[2][0].rgbtRed * gy[2][0];
            }
            else
            {
                gx_blue += 0 * gx[2][0];
                gx_green += 0 * gx[2][0];
                gx_red += 0 * gx[2][0];

                gy_blue += 0 * gy[2][0];
                gy_green += 0 * gy[2][0];
                gy_red += 0 * gy[2][0];
            }

            // [2][1]
            if (has_bottom_row)
            {
                gx_blue += box[2][1].rgbtBlue * gx[2][1];
                gx_green += box[2][1].rgbtGreen * gx[2][1];
                gx_red += box[2][1].rgbtRed * gx[2][1];

                gy_blue += box[2][1].rgbtBlue * gy[2][1];
                gy_green += box[2][1].rgbtGreen * gy[2][1];
                gy_red += box[2][1].rgbtRed * gy[2][1];
            }
            else
            {
                gx_blue += 0 * gx[2][1];
                gx_green += 0 * gx[2][1];
                gx_red += 0 * gx[2][1];

                gy_blue += 0 * gy[2][1];
                gy_green += 0 * gy[2][1];
                gy_red += 0 * gy[2][1];
            }

            // [2][2]
            if (has_bottom_row && has_right_column)
            {
                gx_blue += box[2][2].rgbtBlue * gx[2][2];
                gx_green += box[2][2].rgbtGreen * gx[2][2];
                gx_red += box[2][2].rgbtRed * gx[2][2];

                gy_blue += box[2][2].rgbtBlue * gy[2][2];
                gy_green += box[2][2].rgbtGreen * gy[2][2];
                gy_red += box[2][2].rgbtRed * gy[2][2];
            }
            else
            {
                gx_blue += 0 * gx[2][2];
                gx_green += 0 * gx[2][2];
                gx_red += 0 * gx[2][2];

                gy_blue += 0 * gy[2][2];
                gy_green += 0 * gy[2][2];
                gy_red += 0 * gy[2][2];
            }

            float blue = round(sqrt(gx_blue * gx_blue + gy_blue * gy_blue));
            float green = round(sqrt(gx_green * gx_green + gy_green * gy_green));
            float red = round(sqrt(gx_red * gx_red + gy_red * gy_red));

            if (blue > 255)
            {
                blue = 255;
            }

            if (green > 255)
            {
                green = 255;
            }

            if (red > 255)
            {
                red = 255;
            }

            image[i][j].rgbtBlue = blue;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtRed = red;
        }
    }
}
