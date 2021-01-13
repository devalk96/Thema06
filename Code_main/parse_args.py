import argparse


def construct_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--fastqDir', help='Directory to the fq.gz/fastq.gz files', required=True)
    parser.add_argument('-o', '--organism',
                        help='Define the two letter id for the organism for the '
                             'alignment:\nHuman=hs\nMouse=mm\nMacaque=mmu\nRat=rn')
    parser.add_argument('-out', '--outputDir', help='Pathways to output directory')
    parser.add_argument('-s', '--seqType',
                        help='Define SE for single end sequencing or PE for paired end sequencing')
    parser.add_argument('-p', '--threads', help='Define number of threads to use', default=4, type=int)
    parser.add_argument('-t', '--trim', help='Define the last bp to keep for trimming')
    parser.add_argument('-S', '--skip', help='Skip already processed files', action="store_true", default=False)
    parser.add_argument('-q', '--quality', help='Define cut-off value for trimming', type=int, default=20)
    parser.add_argument('-r', '--refseq', help='Reference genome to align to', type=str, required=True)
    parser.add_argument('-g', '--gtf', help='Gtf file', type=str, required=True)
    parser.add_argument('-l', '--trimgalore', help='Path to Trimgalore', type=str, required=True)
    parser.add_argument('-c', '--cutadapt', help='Path to Cutadapt', type=str, required=True)
    parser.add_argument('-m', '--minimap2', help='Path to minimap2', type=str, required=True)
    parser.add_argument('-f', '--fastqc', help='Path to Fastqc', type=str, required=True)
    parser.add_argument('-e', '--featurecounts', help='Path to Featurecounts', type=str, required=True)

    return parser
