#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = [None] * length

    """
    YOUR CODE HERE
    """

    # The first step will involve going through the tickets and inserting them into the hash table
    for ticket in tickets:
        hash_table_insert(hashtable, ticket.source, ticket.destination)

    # next, identify the first trip
    the_first_trip = hash_table_retrieve(hashtable, "NONE")
    route[0] = the_first_trip # on index 0

    # lastley, we loop through the rest of the trips
    for t in (trip + 1 for trip in range(len(route) -1)):
        route[t] = hash_table_retrieve(hashtable, route[t-1])

    return route
