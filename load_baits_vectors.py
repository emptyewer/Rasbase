import sys

from db.models import Bait, Vector

bait_file_handle = open("_data/baits.csv")

for line in bait_file_handle.readlines():
    (name, re, orf, opt, prot) = line.rstrip().split(",")
    re3, re5 = re.split("/")
    b = Bait(name=name.rstrip(),
             restriction_enzyme_3=re3,
             restriction_enzyme_5=re5,
             sequence=orf,
             optimized_sequence=opt,
             protein_sequence=prot)
    b.save()

for v in ['pTEF_GBD_TRP', 'pGBKT7']:
    vec = Vector(name=v)
    vec.save()

