#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

bool is_cyclic(int winner, int looser);

// === Start - Utilities ===
void print_preferences();
void print_pairs(string label);
void print_locked(string label);
// === End - Utilities ===

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;

            return true;
        }
    }

    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }

    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (i == j)
            {
                continue;
            }

            int preference_1 = preferences[i][j];
            int preference_2 = preferences[j][i];

            if (preference_1 == preference_2)
            {
                continue;
            }

            pair p;

            if (preference_1 > preference_2)
            {
                p.winner = i;
                p.loser = j;
            }

            if (preference_1 < preference_2)
            {
                p.winner = j;
                p.loser = i;
            }

            pairs[pair_count] = p;
            pair_count++;
        }
    }

    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        pair pair_1 = pairs[i];
        int max_idx = i;

        for (int j = i + 1; j < pair_count; j++)
        {
            pair pair_2 = pairs[j];

            int preference_1 = preferences[pair_1.winner][pair_2.winner];
            int preference_2 = preferences[pair_2.winner][pair_1.winner];

            int margin_1 = preference_1 - preference_2;
            int margin_2 = preference_2 - preference_1;

            if (margin_1 > margin_2)
            {
                max_idx = i;
            }
            else
            {
                max_idx = j;
            }
        }

        pairs[i] = pairs[max_idx];
        pairs[max_idx] = pair_1;
    }

    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        pair p = pairs[i];
        int winner = p.winner;
        int loser = p.loser;

        if (is_cyclic(winner, loser) == true)
        {
            continue;
        }

        locked[winner][loser] = true;
    }

    return;
}

// Print the winner of the election
void print_winner(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        int empty_column_cells = 0;

        for (int j = 0; j < candidate_count; j++)
        {
            int is_locked = locked[j][i];

            if (!is_locked)
            {
                empty_column_cells++;
            }
        }

        bool empty_column = empty_column_cells == candidate_count;

        if (empty_column)
        {
            printf("%s\n", candidates[i]);
        }
    }

    return;
}

bool is_cyclic(int winner, int loser)
{

    for (int i = 0; i < pair_count; i++)
    {
        if (locked[loser][i])
        {
            if (i == winner)
            {
                return true;
            }
            if (is_cyclic(winner, i))
            {
                return true;
            }
        }
    }

    return false;
}

void print_preferences()
{
    printf("\n");
    printf("[\n");
    for (int i = 0; i < candidate_count; i++)
    {
        printf("  [");
        for (int j = 0; j < candidate_count; j++)
        {
            printf("%i", preferences[i][j]);
            if (j < candidate_count - 1)
            {
                printf(", ");
            }
        }
        printf("]");
        if (i < candidate_count - 1)
        {
            printf(", ");
        }
        printf("\n");
    }
    printf("]\n");
}

void print_pairs(string label)
{
    printf("\n");

    if (label != NULL)
    {
        printf("%s", label);
        printf("\n");
    }

    printf("[\n");

    for (int i = 0; i < pair_count; i++)
    {
        pair p = pairs[i];

        printf("  [%i, %i]", p.winner, p.loser);

        if (i < pair_count - 1)
        {
            printf(", ");
        }

        printf("\n");
    }

    printf("]");
    printf("\n");
}

void print_locked(string label)
{
    printf("\n");

    if (label != NULL)
    {
        printf("%s", label);
        printf("\n");
    }

    printf("[\n");

    for (int i = 0; i < candidate_count; i++)
    {
        printf("  [");
        for (int j = 0; j < candidate_count; j++)
        {

            bool p = locked[i][j];

            printf("%i", p);

            if (j < candidate_count - 1)
            {
                printf(", ");
            }
        }
        printf("]");
        printf("\n");
    }
    printf("]");
    printf("\n");
}
