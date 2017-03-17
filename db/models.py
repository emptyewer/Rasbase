from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class IndexedGenome(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False, unique=True)
    assembly_id = models.CharField(max_length=20, null=False, unique=True)

    def __str__(self):
        return self.name

class PreyLibrary(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False, unique=True)
    assembly_id = models.CharField(max_length=20, null=False, unique=True)
    feature = models.CharField(max_length=50, null=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.feature)

class Gene(models.Model):
    id = models.AutoField(primary_key=True)
    organism = models.ForeignKey(PreyLibrary)
    name = models.CharField(max_length=50, null=False)
    accession = models.CharField(max_length=20, null=False)
    chromosome = models.CharField(max_length=20, null=False)
    orientation = models.CharField(max_length=1, null=False)
    chr_start = models.IntegerField()
    chr_end = models.IntegerField()
    cds_start = models.IntegerField()
    cds_end = models.IntegerField()
    intron = models.BooleanField(default=False, null=False)
    sequence = models.TextField()
    protein_sequence = models.TextField()

    def __str__(self):
        return "%s (%s)" % (self.name, self.accession)


class Bait(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    restriction_enzyme_3 = models.CharField(max_length=20)
    restriction_enzyme_5 = models.CharField(max_length=20)
    sequence = models.TextField()
    optimized_sequence = models.TextField()
    protein_sequence = models.TextField()

    def __str__(self):
        return self.name

    def chunks(self, l, n):
        """ Yield successive n-sized chunks from l.
        """
        for i in xrange(0, len(l), n):
            yield l[i:i+n]

    def get_formatted_gene_sequence(self):
        sequence = ''
        for chunk in self.chunks(self.optimized_sequence, 80):
            sequence += chunk + '\n'
        return sequence

    def get_formatted_protein_sequence(self):
        sequence = ''
        for chunk in self.chunks(self.protein_sequence, 80):
            sequence += chunk + '\n'
        return sequence

class Vector(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name

class Experiment(models.Model):
    id = models.AutoField(primary_key=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    indexed_genome = models.ForeignKey(IndexedGenome)
    prey_library = models.ForeignKey(PreyLibrary)
    bait = models.ForeignKey(Bait)
    vector = models.ForeignKey(Vector)
    # # #
    project_name = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)
    threshold = models.IntegerField()
    bait_selected_filename = models.CharField(max_length=100, null=False)
    bait_non_selected_filename = models.CharField(max_length=100, null=False)
    base_selected_filename = models.CharField(max_length=100, null=False)
    base_non_selected_filename = models.CharField(max_length=100, null=False)
    vector_selected_filename = models.CharField(max_length=100, null=False)
    vector_non_selected_filename = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name

class Enrichment(models.Model):
    id = models.AutoField(primary_key=True)
    gene_name = models.CharField(max_length=50, default='')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    base_ppm = models.FloatField()
    vector_ppm = models.FloatField()
    bait_ppm = models.FloatField()
    value = models.FloatField()
    adj_value = models.FloatField()
    p_value = models.FloatField()

    def __str__(self):
        return self.gene.name


class SelectedJunctionStat(models.Model):
    id = models.AutoField(primary_key=True)
    in_frame_orf = models.FloatField(null=True)
    upstream = models.FloatField()
    in_orf = models.FloatField()
    downstream = models.FloatField()
    in_frame = models.FloatField()
    backwards = models.FloatField()
    intron = models.FloatField()
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    enrichment = models.ForeignKey(Enrichment)


class NonSelectedJunctionStat(models.Model):
    id = models.AutoField(primary_key=True)
    in_frame_orf = models.FloatField(null=True)
    upstream = models.FloatField()
    in_orf = models.FloatField()
    downstream = models.FloatField()
    in_frame = models.FloatField()
    backwards = models.FloatField()
    intron = models.FloatField()
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    enrichment = models.ForeignKey(Enrichment)


class SelectedJunction(models.Model):
    FRAME = (
        ('N', 'Not in Frame'),
        ('I', 'Intron'),
        ('F', 'In Frame'),
        ('B', 'Backwards'),
    )
    ORF = (
        ('O', 'In ORF'),
        ('U', 'Upstream'),
        ('D', 'Downstream')
    )
    id = models.AutoField(primary_key=True)
    accession_id = models.CharField(max_length=50, null=False)
    position = models.IntegerField()
    query_start = models.IntegerField()
    ppm = models.IntegerField()
    frame = models.CharField(choices=FRAME, max_length=1)
    orf = models.CharField(choices=ORF, max_length=1)
    gene_name = models.CharField(max_length=50, default='')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    enrichment = models.ForeignKey(Enrichment)

class NonSelectedJunction(models.Model):
    FRAME = (
        ('N', 'Not in Frame'),
        ('I', 'Intron'),
        ('F', 'In Frame'),
        ('O', 'Backwards'),
    )
    ORF = (
        ('O', 'In ORF'),
        ('U', 'Upstream'),
        ('D', 'Downstream')
    )
    id = models.AutoField(primary_key=True)
    accession_id = models.CharField(max_length=50, null=False)
    position = models.IntegerField()
    query_start = models.IntegerField()
    ppm = models.IntegerField()
    frame = models.CharField(choices=FRAME, max_length=1)
    orf = models.CharField(choices=ORF, max_length=1)
    gene_name = models.CharField(max_length=50, default='')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    enrichment = models.ForeignKey(Enrichment)

class Error(models.Model):
    id = models.AutoField(primary_key=True)
    experiment = models.CharField(max_length=100)




