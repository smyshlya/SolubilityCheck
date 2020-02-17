import os
import parse_results


# this scrip cuts predefined number of residues from your protein (N or C-terminus) and calculates
# its solubility score

sol_hit = "1.fa"  # input file with your sequence in fasta format
out = "out.fa"  # output file, contains truncated versions of the protein
cut = 50  # number of residues to cut
Nterminus = False  # if False cuts from the C-terminus

seq_file = open(sol_hit, "r")
out_file = open(out, "w")
row = ""
name = ""
count = 0
row = seq_file.readline()
while row:
    if ">" in row:
        print("processing "+row)
    else:
        print("seq is "+row)
        seq = row
    row = seq_file.readline()
while count < cut:
    name = ">-"+str(count)
    print(name, file=out_file)
    print(seq, file=out_file)
    if Nterminus:
        seq = seq[1:]
    else:
        seq = seq[:-1]
    count += 1
out_file.close()
seq_file.close()
file2 = sol_hit+".sol_result"
print("Running Protein-Sol..")
if os.path.exists(file2) and os.path.getsize(file2) > 0:
    print("Sol results already exists, skipping..")
else:
    request4 = "./multiple_prediction_wrapper_export.sh "+out
    print(request4)
    os.system(request4)
    request5 = "cp seq_prediction.txt "+file2
    print(request5)
    os.system(request5)
parse_results.parse_solubility_results(file2, "Sol_prediction", False, 'line')
