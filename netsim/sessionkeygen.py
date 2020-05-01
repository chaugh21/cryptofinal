import Crypto, Random

class SessionKeyGenerator:

    def genNonce(self):
        return Crypto.Random.get_random_bytes(256)
    #Produces DH1 = [g1X1mod(p1), g2x2mod(p2) , g1,g2,p1,p2]). See Design Document for details on each element
    def generate_dh1(self):
        #generate two large primes. to do so, generate a list of large primes and choose two randomly.
        P1 = Crypto.Util.number.getStrongPrime(2**64) # Strong primes have p-1 p+1 with a large prime factor.
        P2 = Crypto.Util.number.getStrongPrime(2**64)
        # create our generator G. from taking group theory that for all cyclic groups of prime numbers of order >2 all elements are generators so we can select one at random.
        G1 = Crypto.Random.random.randint(1, P1)
        G2 = Crypto.Random.random.randint(1, P2)
        # generate a random X1, X2.
        X1 = Crypto.Random.random.randint(1,2**64)
        X2 = Crypto.Random.random.randint(1,2**64)
        #do the math
        M1 = (G1**X1) * (P1%2) # mod base 2? TODO: Figure out if correct.
        M2 = (G2**X2) * (P2%2)
        # TODO: put it all in an array

        DH1 = {P1,P2,G1,G2,M1,M2,X1,X2}
        return DH1

    def generate_dh2(G1,G2,P1,P2,):
        Y1 = Crypto.Random.random.randint(1,2**64)
        Y2 = Crypto.Random.random.randint(1,2**64)
        MMESSAGE=(G1**Y2)%(P1)
        MMAC=(G2**Y2)%(P2)
        return M1,M2,Y1,Y2

    def calculate_keys(self, M1,M2,X1,X2,P1,P2):

        KMESSAGE = (M1**X1)%(P2)
        KMAC = (M2**X2)%(P2)
        return KMESSAGE,KMAC
