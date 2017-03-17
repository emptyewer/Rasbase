# Run this file in Django DB Shell

import sys
from db.models import PreyLibrary, IndexedGenome
from db.models import Gene

organism_name = 'Mus musculus'
assembly_id = 'mm10'
feature = 'Generic'
file = '_data/mm10GeneList.prn'

gene_list_handle = open(file)
o = PreyLibrary(name=organism_name, assembly_id=assembly_id, feature=feature)
o.save()

i = IndexedGenome(name=organism_name, assembly_id=assembly_id)
i.save()

for line in gene_list_handle.readlines():
    (nm, gene, chromosome, orient, chr_start, chr_end, cds_start, cds_end, intron, seq, protein_seq) = line.split()
    if intron == "--":
        intron = False
    else:
        intron = True
    g = Gene(organism=o,
             name=gene,
             accession=nm,
             chromosome=chromosome,
             orientation=orient,
             chr_start=int(chr_start),
             chr_end=int(chr_end),
             cds_start=int(cds_start),
             cds_end=int(cds_end),
             intron=intron,
             sequence=seq,
             protein_sequence=protein_seq)
    g.save()
