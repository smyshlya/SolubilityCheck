import os
import pandas as pd
import matplotlib.pyplot as plt


def parse_solubility_results(result_file, genome_name, sorting, plot_kind):
    dataframe_array = []
    file_to_parse = open(result_file, "r")
    line_to_parse = file_to_parse.readline()
    while line_to_parse:
        line_to_parse = line_to_parse.rstrip()
        if "SEQUENCE PREDICTIONS" in line_to_parse:
            my_list = (line_to_parse.split(","))

        if "SEQUENCE DEVIATIONS" in line_to_parse:
            my_list2 = (line_to_parse.split(","))
            my_list.append(my_list2[4])
            dataframe_array.append(my_list)
        line_to_parse = file_to_parse.readline()
    df = pd.DataFrame(dataframe_array)
    df.rename(columns={1: 'Name', 2: 'Percent_Sol', 3: 'Solubility', 6: 'Length'}, inplace=True)
    if sorting:
        df.sort_values(['Solubility'], axis=0, ascending=False, inplace=True)
    df["Solubility"] = pd.to_numeric(df["Solubility"])
    df["Length"] = pd.to_numeric(df["Length"])
    df = df.head(n=50)
    print(df)
    ax = df.plot(y=['Solubility'], kind=plot_kind)
    ax.set_xticks(df.index)
    df['Name'] = df['Name'].str[2:]
    ax.set_xticklabels(df['Name'])
    plt.xticks(fontsize=8, rotation=90)
    #plt.axhline(y=0.45, linewidth=1, color='k', dashes=(5, 2, 1, 2))
    plt.title("RT-gRNH-aRNH solubilty in "+genome_name)
    plt.savefig(genome_name+".png")
