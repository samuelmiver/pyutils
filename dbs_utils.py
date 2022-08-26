#!/usr/bin/env python

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
# from Bio.Alphabet import IUPAC
from Bio.SeqFeature import SeqFeature, FeatureLocation

def fastawriter(sequence, identifier, outfile):
    with open(outfile, 'w') as fo:
        fo.write('>'+identifier+'\n'+sequence+'\n'


def load_multifasta(inFile):
    """ Return a dictionary wit the sequences from a multifasta file """
    your_sequences = {}
    handle = open(inFile, 'rU')
    for record in SeqIO.parse(handle, "fasta"):
        your_sequences[record.id]=str(record.seq)
    handle.close()
    return your_sequences


def load_multifasta_info(inFile):
    """ Return a dictionary wit the sequences from a multifasta file """
    your_sequences = {}
    handle = open(inFile, 'rU')
    for record in SeqIO.parse(handle, "fasta"):
        your_sequences[record.id+'//'+record.description]=str(record.seq)
    handle.close()
    return your_sequences


def load_genome(genome):
    # Determine the file type:
    if genome.endswith('gb') or genome.endswith('gbk') or genome.endswith('genbank'):
        tipo = 'genbank'
    else:
        tipo = 'fasta'
    handle = open(genome, 'rU')
    for record in SeqIO.parse(handle, tipo):
        return str(record.seq)
    handle.close()



def create_genbank(genome_sequence, annotation_dic, outfile, ide='your_genome', name='your_organism'):

    # Create a sequence
    sequence_string = genome_sequence
    sequence_object = Seq(sequence_string)
    # IUPAC.unambiguous_dna ## Removing outdated dependency

    # Create a record
    record = SeqRecord(sequence_object,
            id=ide,
            name=name,
            description='Custom annotation file')

    # Add annotation
    for gene, values in annotation_dic.iteritems():
        if values[-1]=='+':
            strand = 1
        else:
            strand = -1
        feature = SeqFeature(FeatureLocation(start=values[0], end=values[1], strand=strand), type='CDS')
        feature.qualifiers['gene']=gene
        record.features.append(feature)

    # Save as GenBank file
    output_file = open(outfile, 'w')
    SeqIO.write(record, output_file, 'genbank')


def genbank2annotation(genome):
    annotation = {}
    with open(genome, "rU") as input_handle:
        for record in SeqIO.parse(input_handle, "genbank"):
            for feat in record.features:
                if feat.type in ['CDS', 'rRNA', 'tRNA', 'ncRNA']:
                    annotation[feat.qualifiers['locus_tag'][0]] = [int(feat.location.start)+1, int(feat.location.end), '+' if feat.location.strand==1 else '-']
                    # +1 required for the start, if not included the returned positions does not correspond to the annotation. I think biopython changes the notation to base 0
    return annotation


def genbank2gff3(inFile, outFile):
    """
    Given a genome in genbank format <inFile>
    creates a gff3 file <outFile>
    format described here: https://www.ensembl.org/info/website/upload/gff3.html
    """

    fo = open(outFile, 'w')
    fo.write('##gff-version 3\n')

    with open(genome, "rU") as input_handle:
        for record in SeqIO.parse(input_handle, "genbank"):
            for feat in record.features:
                if feat.type in ['CDS', 'rRNA', 'tRNA', 'ncRNA']:
                    line = [record.id, '.', feat.type, feat.location.start, feat.location.end, '.', '+' if feat.location.strand==1 else '-', '.', 'ID=']
                    fo.write('\t'.join([str(i) for i in line])+'\n')
    fo.close()
