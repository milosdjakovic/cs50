#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int is_jpg_header_signature(unsigned char buffer[512])
{
    uint8_t first_byte = buffer[0];
    uint8_t second_byte = buffer[1];
    uint8_t third_byte = buffer[2];
    uint8_t fourth_byte = buffer[3];

    if (first_byte != 0xff)
        return 0;

    if (second_byte != 0xd8)
        return 0;

    if (third_byte != 0xff)
        return 0;

    if ((fourth_byte & 0xf0) != 0xe0)
        return 0;

    return 1;
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image.raw\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    unsigned char buffer[512];
    int jpg_found_count = 0;
    char jpg_filename[8] = "000.jpg";

    FILE *output = NULL;

    while (fread(&buffer, sizeof(buffer), 1, input))
    {
        int is_jpg = is_jpg_header_signature(buffer);

        if (is_jpg)
        {
            if (output != NULL)
            {
                fclose(output);
            }

            sprintf(jpg_filename, "%03i.jpg", jpg_found_count);

            output = fopen(jpg_filename, "wb");

            if (output == NULL)
            {
                printf("Error opening file!\n");
                fclose(input);
                return 1;
            }

            jpg_found_count++;
        }

        if (output != NULL)
        {
            if (fwrite(buffer, 1, sizeof(buffer), output) != sizeof(buffer))
            {
                printf("Error writing to file!\n");
                fclose(output);
                fclose(input);
                return 1;
            }
        }
    }

    if (output != NULL)
    {
        fclose(output);
    }

    fclose(input);

    printf("Memory card image reading completed!\n");
    return 0;
}
