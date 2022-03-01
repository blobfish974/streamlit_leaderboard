import pandas as pd
df_scores = pd.read_csv('df_scores_1.csv', index_col=0, sep="\t")
df_scores_updated = pd.read_csv('df_scores_2.csv', index_col=0, sep="\t")


def update_df_scores(df, df_updated):
    list_col_df = df.columns.to_list()
    list_col_df_updated = df_updated.columns.to_list()
    common_col = set(list_col_df) & set(list_col_df_updated)
    print(common_col)
    last_index = df.index[-1]
    for col in list_col_df_updated:
        if col not in common_col:
            df = df.join(df_updated.loc[:, [col]])
        else:
            if(df_updated.index[-1] in df.index):
                # when we already appended the rows to the dataframe (otherwise duplicates appear)
                df.loc[last_index:, [col]] = df_updated.loc[last_index:, [col]]
            else:
                df = df.append(df_updated.loc[last_index:, [col]])
    return df


print(df_scores)
df_scores = update_df_scores(df_scores, df_scores_updated)
print(df_scores)
