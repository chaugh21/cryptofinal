from Crypto.Util import number
from Crypto.Random import random

class SessionKeyGenerator:

    #TODO: GENERATE LARGER PRIMES

    #Produces DH1 = [g1X1mod(p1), g2x2mod(p2) , g1,g2,p1,p2]). See Design Document for details on each element
    def generate_dh1():
        #generate two large primes. to do so, generate a list of large primes and choose two randomly.
        P1 = int(number.getPrime(2**4)) # Strong primes have p-1 p+1 with a large prime factor.
        P2 = int(number.getPrime(2**4))
        # create our generator G. from taking group theory that for all cyclic groups of prime numbers of order >2 all elements are generators so we can select one at random.
        G1 = random.randint(1, P1)
        G2 = random.randint(1, P2)

        # generate a random X1, X2.
        X1 = random.randint(1,P1)
        X2 = random.randint(1,P2)

        #do the math
        M1 = (G1**X1) % (P1)
        M2 = (G2**X2) % (P2)

        return {'M1':M1,'M2': M2, 'G1': G1,'G2': G2, 'P1': P1, 'P2': P2, 'X1': X1, 'X2': X2}

        #[MA,MB,Y1,Y2]
    def generate_dh2(G1,G2,P1,P2):
        Y1 = random.randint(1,2**4)
        Y2 = random.randint(1,2**4)
        MA=(G1**Y1)%P1
        MB=(G2**Y2)%P2
        return {'MA':MA,'MB':MB,'Y1':Y1,'Y2':Y2}

    def calculate_keys(M1,M2,X1,X2,P1,P2):
        KMESSAGE = (M1**X1)%P1
        KMAC = (M2**X2)%P2
        return [KMESSAGE.to_bytes(length=4, byteorder='big'),KMAC.to_bytes(length=4, byteorder='big')]

    def genNonce():
        return random.getrandbits(32)
