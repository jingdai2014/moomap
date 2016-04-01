import random

pam_seq = range(1, 17)
random.shuffle(pam_seq)
pam_seq = [str(i) for i in pam_seq]

for ps in range(len(pam_seq)):
    pam_seq[ps] = pam_seq[ps] + "_" + str(random.randint(1, 3))

print pam_seq