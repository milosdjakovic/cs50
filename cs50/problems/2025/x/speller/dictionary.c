// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 200;

// Hash table
node *table[N];

unsigned int word_count;

void print_linked_list(node *n)
{
    if (n == NULL)
    {
        printf("\n");
        return;
    }

    printf("(%s)", n->word);
    if (n->next != NULL)
    {
        printf("->");
    }

    print_linked_list(n->next);
}

void print_hash_table()
{
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            printf("---\n");

            printf("Bucket %04i:", i);

            print_linked_list(table[i]);
        }

        if (i == N - 1)
        {
            printf("---\n");
        }
    }
}

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    unsigned int index = hash(word);

    if (table[index] == NULL)
    {
        return false;
    }

    node *cursor = table[index];

    while (cursor != NULL)
    {
        int word_found = strcasecmp(word, cursor->word) == 0;

        if (word_found)
        {
            return true;
        }

        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int i = 0;
    unsigned int ascii_sum = 0;

    while (word[i] != '\0')
    {
        ascii_sum += toupper(word[i]);
        i++;
    }

    return ascii_sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        fclose(source);
        return false;
    }

    char *word = malloc(LENGTH + 1);

    while (fscanf(source, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            free(word);
            fclose(source);
            return false;
        }

        strcpy(n->word, word);
        n->next = NULL;

        unsigned int index = hash(word);

        if (table[index] == NULL)
        {
            table[index] = n;
        }
        else
        {
            n->next = table[index];
            table[index] = n;
        }
        word_count++;
    }

    // print_hash_table();

    free(word);
    fclose(source);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        if (table[i] == NULL)
        {
            continue;
        }

        node *cursor = table[i];
        node *tmp = NULL;

        while (cursor != NULL)
        {
            tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }

    return true;
}
