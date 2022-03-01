import pandas as pd
df_ranking = pd.read_csv('df_ranking_old.csv', index_col=0, sep="\t")
df_ranking_updated = pd.read_csv('df_ranking_old_2.csv', index_col=0, sep="\t")


def update_df_ranking(df, df_updated):
    for index, row in df_updated.iterrows():
        name = df_updated.loc[index, ['names']]['names']
        index_name = df.index[df['names'] == name].tolist()
        if len(index_name) == 0:
            # print("empty!")
            # add to df
            score = df_updated.loc[index, ['scores']]['scores']
            new_row = {'names': name, 'scores': score}
            # print(new_row)
            df = df.append(new_row, ignore_index=True)
        else:
            index_name = index_name[0]
            if(df_updated.loc[index, ['scores']]['scores'] != 0):
                df.loc[index_name, ['scores']
                       ] = df_updated.loc[index, ['scores']]['scores']
    return df


print(df_ranking)
df_ranking = update_df_ranking(df_ranking, df_ranking_updated)
print(df_ranking)
