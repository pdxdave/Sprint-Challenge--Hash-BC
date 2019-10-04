#  Hint:  You may not need all of these.  Remove the unused functions.
#  What if we store each weight in the input list as keys? What would be a useful thing to store as the value for each key? 
#  If we store each weight's list index as its value, we can then check to see if the hash table contains an entry for `limit - weight`. If it does, then we've found the two items whose weights sum up to the `limit`!

from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    h_table = HashTable(16) # looks like 16 buckets

    """
    YOUR CODE HERE
    """

    # first, loop through the items and insert them into the hashtable
    for j in range(0, length):
        hash_table_insert(h_table, weights[j], j)

    # next, loop through and check the weights.
    for j in range(0, length):
        item = limit - weights[j]  # hint
        index = hash_table_retrieve(h_table, item)
        if index:
            return (index, j)

    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
