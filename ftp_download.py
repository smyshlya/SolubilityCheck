from ftplib import FTP
from datetime import datetime
import os


start = datetime.now()
ftp = FTP('ftp.ensemblgenomes.org')
ftp.login()

# Get All Filespwd
ftp.cwd('/pub/release-46/plants/fasta/')
genome_folders = ftp.nlst()

# Print out the files
for genome in genome_folders:
    ftp.cwd(genome+'/dna/')
    genome_dna_files = ftp.nlst()
    for sequence_file in genome_dna_files:
        if ".dna.toplevel.fa.gz" in sequence_file:
            print(sequence_file)
            genome_file="/Users/gera/PycharmProjects/SolubilityCheck/genomes/"+sequence_file
            if os.path.exists(genome_file) and os.path.getsize(genome_file) > 0:
                print("Genome file already exist, skipping")
            else:
                ftp.retrbinary("RETR " + sequence_file, open(genome_file, 'wb').write)
    ftp.cwd('/pub/release-46/plants/fasta/')
ftp.close()

end = datetime.now()
diff = end - start
print('All files downloaded for ' + str(diff.seconds) + 's')