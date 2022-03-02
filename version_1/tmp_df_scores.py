import pandas as pd
from datetime import datetime, timedelta, date

df_scores = pd.read_csv('data/df_scores_1.csv', index_col=0, sep="\t")
df_scores_updated = pd.read_csv('data/df_scores_2.csv', index_col=0, sep="\t")
df_scores.index = pd.to_datetime(df_scores.index)
df_scores_updated.index = pd.to_datetime(df_scores_updated.index)


def update_df_scores(df, df_updated):
    if df.empty:
        return df_updated
    list_col_df = df.columns.to_list()
    list_col_df_updated = df_updated.columns.to_list()
    common_col = set(list_col_df) & set(list_col_df_updated)
    # print(common_col)
    for col in list_col_df_updated:
        last_index = df.index[-1].to_pydatetime()
        if col not in common_col:
            df = df.join(df_updated.loc[:, [col]])  # left join
            # df = pd.concat([df, df_updated.loc[:, [col]]], axis=1)
        else:
            # if(last_index in df_updated.index):
            if(df_updated.index[-1] in df.index):
                # we update tthe values
                last_date_valid_index = df.loc[:, [
                    col]].last_valid_index().to_pydatetime()
                # when we already appended the rows to the dataframe (otherwise duplicates appear)
                # print("last index: " + str(last_index))
                print("last valid index: " + str(last_date_valid_index))
                if(last_index > last_date_valid_index):
                    print('enter if')
                    #     print(df_updated.loc[last_index:, [col]])
                    print(
                        df_updated.loc[last_date_valid_index:, [col]])
                    df.loc[last_date_valid_index:, [col]
                           ] = df_updated.loc[last_date_valid_index:, [col]]
                else:
                    print("NOOOOO")
                #     df.loc[last_index:, [col]
                #            ] = df_updated.loc[last_index:, [col]]
            else:
                print('enter else')
                # print(df_updated.loc[last_index:, [col]])
                df = df.append(
                    df_updated.loc[last_index + timedelta(days=1):, [col]])
    return df


print(df_scores)
df_scores = update_df_scores(df_scores, df_scores_updated)
print(df_scores)
