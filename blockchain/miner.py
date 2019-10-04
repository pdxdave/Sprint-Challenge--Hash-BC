import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random

# Ok, what do I know?  
# I know that I need to validate the proof. 
# I know that I have to create a hash using SHA-256.  The hash will go in the valid_proof def. The instructions refer to it there.
# I know that in order to validate the proof I will have to loop through a series of numbers.  
# I know that I will need some sort of solution to compare the first six numbers of the hash to the last six numbers of the hash.
# I see in the notes they are specifically saying last hash and new hash.
# The class example for SHA-256 included .hexdigest().
# Doesn't it have to be encoded too?  Combine the two?  How would I do that? 

# TEST RESULTS
# The first test didn't work.  I got the following error 
# last_h = hashlib.sha256(encode(last_hash)).hexdigest()
#    NameError: name 'encode' is not defined
# I see that proof is a string in the print out.  Maybe I need to send the hash through a string then encode it
# I changed it so the proof was sent through the string.  That seemed to work, but still got an error regarding
# last hash.  Since they're comparing against each other, I'll send the last_h through the string as well.

# Got my butt kicked.  Starting over again.  I wasn't getting errors, so I thought all was good. WRONG!
# Changes:
# Set my proof to an random integer when it comes back.  Maybe the plus 5 I had before is too generic

def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    - Note:  We are adding the hash of the last proof to a number/nonce for the new proof
    """

    start = timer()

    last_p = f'{last_proof}'.encode()
    last_p_hash = hashlib.sha256(last_p).hexdigest()

    print("Searching for next proof")

    #  TODO: Your code here
    proof = 6584754

    while valid_proof(last_p_hash, proof) is False:
        proof += 8

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the proof?

    IE:  last_hash: ...AE9123456, new hash 123456888...
    """

   # TODO: Your code here!

    guess = f'{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return last_hash[-6:] == guess_hash[:6]

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
