# From the Deep

In this problem, you'll write freeform responses to the questions provided in the specification.

## Random Partitioning

The advantage of random partitioning is that it spreads the data evenly across all boats, no matter what time the observations were made. This helps avoid one boat getting overloaded.

The disadvantage is that to find observations from a specific time range, a researcher would need to query all boats, since the data is placed randomly.

## Partitioning by Hour

The advantage of partitioning by hour is that if we know the time of the observation, we can go straight to the right boat. For example, if we need data from midnight to 1am, we only need to check Boat A. This makes time-based queries faster and more efficient.

The disadvantage is that when a lot of data is collected during the same time window, like midnight to 1am, it all goes to one boat. That can lead to that boat getting overloaded, making the system less balanced and possibly filling up its memory faster than the others.

## Partitioning by Hash Value

The advantage of hash partitioning is similar to random partitioning. It spreads the data evenly across all boats which keeps the system balanced and avoids overloading a single boat. The disadvantage is also similar because when searching for a range of times we still have to query all boats since the data is not grouped by time.

Where hash partitioning differs is when looking for a specific timestamp. If we know the exact timestamp we can compute its hash and know exactly which boat it was sent to. That makes it really fast to find a single specific entry.
