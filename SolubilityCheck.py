import os
import parse_results
import glob


#  this scrip uses protein query to run blastp against genomes of interest and
#  calculates the solubility of the resulting sequences

blast_dir = "/Users/gera/Downloads/blast-2.2.18/bin"  # your blast bin folder
folder = "/Users/gera/PycharmProjects/SolubilityCheck/genomes/"  # here you store archived genomes (in *.fa.gz format)
all_genomes = glob.glob(folder+"/*.fa.gz")
query = blast_dir+"/RNH.fa"  # here is your  query file (somehow should be in the blast bin folder)

db_zipped = ""
for db in all_genomes:
    # checking the format of the genome, we'd like to have them all zipped after processing
    if ".gz" in db:
        zipped = True
        db_zipped = db
        db = db.strip(".gz")
    else:
        zipped = False
        db_zipped = db+".gz"
    genome_name = os.path.basename(db)
    out = db+"_out.txt"
    seq = db+"_seq.fa"

    # running tblastn
    if os.path.exists(out) and os.path.getsize(out) > 0:
        print("Blast results already exist, skipping")
    else:
        if zipped:
            print("gunzip " + db_zipped)
            os.system("gunzip " + db_zipped)
        request1 = "makeblastdb -in "+db+" -dbtype nucl"
        request2 = "tblastn -query "+query+" -db "+db+" -out "+out+" -outfmt \"6 sseqid sstart send sseq\""
        print(request1)
        print(request2)
        os.system(request1)
        os.system(request2)

    # processing results of tblastn
    if os.path.exists(seq) and os.path.getsize(seq) > 0:
        print("Blast results are already parsed, skipping")
    else:
        my_file = open(out, "r")
        seq_file = open(seq, "w")
        line2 = my_file.readline()
        count = 0
        all_hits = []
        while line2:
            if "*" not in line2:
                line2 = line2.rstrip()
                my_list = (line2.split("\t"))
                my_seq = my_list.pop(-1)
                if len(my_seq) > 500:
                    joined_string = "|".join([str(v) for v in my_list])
                    print(">", joined_string, file=seq_file, sep="")
                    print(my_seq, file=seq_file)
            line2 = my_file.readline()
        seq_file.close()

    # running Protein-Sol and parsing results
    file2 = db+"_seq_prediction.txt"
    if os.path.exists(file2) and os.path.getsize(file2) > 0:
        print("Protein-Sol results already exist")
    else:
        if os.path.exists(seq) and os.path.getsize(seq) > 0:
            print("Running Protein-Sol..")
            request4 = "./multiple_prediction_wrapper_export.sh "+seq
            print(request4)
            os.system(request4)
            request5 = "cp seq_prediction.txt "+file2
            print(request5)
            os.system(request5)
            parse_results.parse_solubility_results(file2, genome_name, True, 'bar')
        else:
            print("No homologues of"+query+"were found in"+genome_name)

    # zipping back previously unzipped large genome file
    if zipped:
        if os.path.exists(db_zipped):
            print(db+" still zipped")
        else:
            print("zipping back"+db)
            os.system("gzip " + db)
    else:
        print("zipping " + db)
        os.system("gzip " + db)

    print("++++++++++DONE++++++++++")