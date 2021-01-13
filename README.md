# Thema06
### How to deal with difficult data

--- 
# PRC - Pipeline recreation
## Usage:
pip3 install -r requirements.txt --user


For help:
./Code_main/main.py -h

OUTPUT:
-
usage: main.py [-h] [-d FASTQDIR] [-k FILES [FILES ...]] [-o ORGANISM]
               [-out OUTPUTDIR] [-s SEQTYPE] [-p THREADS] [-t TRIM] [-S]
               [-q QUALITY] -r REFSEQ -g GTF [-l TRIMGALORE] [-c CUTADAPT]
               [-m MINIMAP2] [-f FASTQC] [-e FEATURECOUNTS]

optional arguments:
  -h, --help            show this help message and exit

  -d FASTQDIR, --fastqDir FASTQDIR

                            Directory to the fq.gz/fastq.gz files

  -k FILES [FILES ...], --files FILES [FILES ...]

                        Add a list of files to process

  -o ORGANISM, --organism ORGANISM

                        Define the two letter id for the organism for the
                        alignment: Human=hs Mouse=mm Macaque=mmu Rat=rn

  -out OUTPUTDIR, --outputDir OUTPUTDIR
               
                        Pathways to output directory
  -s SEQTYPE, --seqType SEQTYPE
               
                        Define SE for single end sequencing or PE for paired
                        end sequencing
  -p THREADS, --threads THREADS
               
                        Define number of threads to use
  -t TRIM, --trim TRIM  
  
                        Define the last bp to keep for trimming
  -q QUALITY, --quality QUALITY
            
                        Define cut-off value for trimming
  -r REFSEQ, --refseq REFSEQ
            
                        Reference genome to align to
  -g GTF, --gtf GTF     
    
                        Gtf file
  -l TRIMGALORE, --trimgalore TRIMGALORE
        
                        Path to Trimgalore
  -c CUTADAPT, --cutadapt CUTADAPT
        
                        Path to Cutadapt
  -m MINIMAP2, --minimap2 MINIMAP2
        
                        Path to minimap2
  -f FASTQC, --fastqc FASTQC
        
                        Path to Fastqc
  -e FEATURECOUNTS, --featurecounts FEATURECOUNTS
        
                        Path to Featurecounts
