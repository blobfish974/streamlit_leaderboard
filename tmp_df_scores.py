import pandas as pd
df_scores = pd.read_csv('df_scores_1.csv', index_col=0, sep="\t")
df_scores_updated = pd.read_csv('df_scores_2.csv', index_col=0, sep="\t")


def update_df_scores(df, df_updated):
    list_col_df = df.columns.to_list()
    list_col_df_updated = df_updated.columns.to_list()
    common_col = set(list_col_df) & set(list_col_df_updated)
    print(common_col)
    for col in list_col_df_updated:
        if col not in common_col:
            print(col + " not present!")
        else:
            print(col + " found")
            print(df_updated.loc[:, [col]])
            # not best solution:
            df.loc[:, [col]] = df_updated.loc[:, [col]]

    # for col in df_updated.columns:
    #     print(col)
    #     index_name = df.index[df['names']
    #                           == col].tolist()
    #     if len(index_name) == 0:
    #         print("empty!")
    """
    for index, row in df_updated.iterrows():
        name = df_updated.loc[index, ['names']]['names']
        index_name = df.index[df['names']
                              == name].tolist()
        if len(index_name) == 0:
            print("empty!")
            # add to df
            score = df_updated.loc[index, ['scores']]['scores']
            new_row = {'names': name, 'scores': score}
            print(new_row)
            df = df.append(new_row, ignore_index=True)
            # print(df)
        else:
            index_name = index_name[0]
            # print(df[df['names'] == 'pieacoulisse'].index.values)
            # df.index[df['team'] == 'B'].tolist()
            # index_df = df.index[df['names'] == "pieacoulisse"]
            # print(index_df)
            # print(df.loc[index, ['scores']]['scores'])
            if(df_updated.loc[index, ['scores']]['scores'] != 0):
                df.loc[index_name, ['scores']
                       ] = df_updated.loc[index, ['scores']]['scores']
    """
    return df


df_scores = update_df_scores(df_scores, df_scores_updated)
# print(df_scores)
