import json
import pandas as pd
import streamlit as st
import time
import random
import re
import requests
from bs4 import BeautifulSoup as bs
import numpy as np
from os import path, mkdir
from datetime import datetime, timedelta, date


def daterange(date1, date2):
    for n in range(int((date2 - date1).days)+1):
        yield date1 + timedelta(n)


# Global variables
date_list = list()
for dt in daterange(date(2021, 9, 1), date.today()):
    date_list.append(dt)
num_dates = len(date_list)

data_names = ["pieacoulisse", "Miaimbouchon", "BOUCENNA", "fdn4444", "miled", "Caroline-46821",
              "Pompottewi", "Arsuol", "Yves-Marie", "Keyoke", "giso", "Yasuotarie"]
# data_names = ["pieacoulisse"]
# data_names_banned = ["Nyco"]

df_ranking = pd.DataFrame(columns=[])
df_scores = pd.DataFrame(columns=[])


def read_last_update():
    if(path.exists("data/updated_datetime.txt")):
        with open("data/updated_datetime.txt", "r") as txt_file:
            return txt_file.read()
    else:
        return "Never"


def write_last_update():
    file = open("data/updated_datetime.txt", "w")
    now = datetime.now() + timedelta(hours=1)
    file.write(now.strftime("%d/%m/%Y %H:%M:%S"))
    return True


def init_data():
    """
    loads initial datas (stored as csv)
    uses global variables to store them

    :return: False if data couldn't be loaded
    """
    global df_ranking, df_scores
    result = True
    if(path.exists("data/df_ranking.csv")):
        df_ranking = pd.read_csv('data/df_ranking.csv', index_col=0, sep="\t")
        df_ranking.sort_values(by=["scores"], inplace=True, ascending=False)
        df_ranking = df_ranking.reset_index(drop=True)
        df_ranking.index = df_ranking.index + 1
    else:
        result = False
    if(path.exists("data/df_scores.csv")):
        df_scores = pd.read_csv('data/df_scores.csv', index_col=0, sep="\t")
        df_scores.index = pd.to_datetime(df_scores.index)
    else:
        result = False
    if(not path.exists("data")):
        mkdir("data")

    return result


def ranking_dataframe():
    return df_ranking


def scores_dataframe():
    return df_scores


def scores_last_month_dataframe():
    df_scores_last_month = df_scores.iloc[-30:, :]
    df_scores_last_month.index = pd.to_datetime(df_scores_last_month.index)
    return df_scores_last_month


def scores_last_month_evolution_dataframe():
    df_scores_last_month = df_scores.iloc[-30:, :]
    progress = list()
    start_value = list()
    end_value = list()
    data_col = df_scores_last_month.columns.to_list()
    for col in data_col:
        last_date_valid_index = df_scores_last_month.loc[:, [
            col]].last_valid_index().to_pydatetime()
        progress.append(
            int(df_scores_last_month.loc[last_date_valid_index, col]-df_scores_last_month.iloc[0][col]))
        start_value.append(int(df_scores_last_month.iloc[0][col]))
        end_value.append(
            int(df_scores_last_month.loc[last_date_valid_index, col]))
    df_metrics = pd.DataFrame({
        'names': data_col,
        'progress': progress,
        'start_value': start_value,
        'end_value': end_value,
    })
    df_metrics.sort_values(
        by=["progress"], inplace=True, ascending=False)
    df_metrics = df_metrics.reset_index(drop=True)
    return df_metrics


def fetch_datas(status_text, my_bar):
    """
    fetch datas from the site and grab the scores 

    :param status_text: the text printed in the streamlit
    :param my_bar: the progress bar printed in the streamlit
    :return: a list of the scores for each player and a matrix of their score evolution (dimensions = date*players)
    """
    status_text.text("0% Complete")
    data_score = list()
    pattern = "validations.push\({(.+?),[\s]*}\);"
    all_scores = np.zeros((num_dates, len(data_names)))
    len_data_names = len(data_names)
    for index, name in enumerate(data_names):
        print("Fetching " + name + "...")
        url = "https://www.root-me.org/" + name + "?inc=statistiques&lang=en"
        time.sleep(3+random.randint(3, 4))

        response = requests.get(url)
        html = response.content
        soup = bs(html, 'html.parser')
        h3 = soup.find_all('h3')
        try:
            points = int(h3[5].getText().strip())
        except:
            print("Error getting score")
            data_score.append(0)
            continue
        else:
            script = soup.find_all('script', src=None)
            raw_validation_push = re.findall(pattern, script[-1].string, re.S)
            json_struct = json.loads("[ ]")
            if raw_validation_push:
                for i in range(len(raw_validation_push)):
                    raw_validation_push[i] = re.sub(
                        r"'titre'\s*:.*", " ", raw_validation_push[i])
                    json_string = "{" + \
                        raw_validation_push[i].replace('\'', '\"') + "\n}"
                    data = json.loads(json_string)
                    json_struct.append(data)
                # Constructing the data array for points according to dates
                score_sum = 0
                scores = [0] * num_dates
                for x in json_struct:
                    date_time_str = x["date"]
                    date_time_obj = datetime.strptime(
                        date_time_str, '%Y-%m-%d %H:%M:%S')
                    if(date_time_obj.date() in date_list):
                        index_date = date_list.index(date_time_obj.date())
                    else:  # it happens when the user had points before the start date
                        index_date = 0
                    score_sum += int(x["score"])
                    for j in range(index_date, num_dates):
                        scores[j] = score_sum
                all_scores[:, index] = scores

            else:
                print("Error getting stats points")
            data_score.append(points)
            prog = int((index+1)*100/len_data_names)
            status_text.text("%i%% Complete" % prog)
            my_bar.progress(prog)
    status_text.text("100% Complete, Please refresh the page :)")
    return [data_score, all_scores]


def update_df_ranking(df, df_updated):
    """
    update existing ranking dataframe

    :param df: the original dataframe containing ranking
    :param df_updated: the fetched dataframe with new ranking
    :return: a dataframe of the 2 combined
    """
    print("Enter update_df_ranking")
    if df.empty:
        return df_updated
    for index, row in df_updated.iterrows():
        name = df_updated.loc[index, ['names']]['names']
        index_name = df.index[df['names']
                              == name].tolist()
        if len(index_name) == 0:
            score = df_updated.loc[index, ['scores']]['scores']
            new_row = {'names': name, 'scores': score}
            df = df.append(new_row, ignore_index=True)
        else:
            index_name = index_name[0]
            if(df_updated.loc[index, ['scores']]['scores'] != 0):
                df.loc[index_name, ['scores']
                       ] = df_updated.loc[index, ['scores']]['scores']
    df.sort_values(
        by=["scores"], inplace=True, ascending=False)
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    return df


def update_df_scores(df, df_updated):
    """
    append new datas to the existing scores dataframe

    :param df: the original dataframe containing scores
    :param df_updated: the fetched dataframe with new scores
    :return: a dataframe of the 2 combined
    """
    print("Enter update_df_scores")
    if df.empty:
        return df_updated
    list_col_df = df.columns.to_list()
    list_col_df_updated = df_updated.columns.to_list()
    common_col = set(list_col_df) & set(list_col_df_updated)
    for col in list_col_df_updated:
        last_index = df.index[-1].to_pydatetime()
        if col not in common_col:
            df = df.join(df_updated.loc[:, [col]])
        else:
            # if the dataframe already has all the indexes
            if(df_updated.index[-1] in df.index):
                last_date_valid_index = df.loc[:, [
                    col]].last_valid_index().to_pydatetime()
                # we check that there is no Nan value for an index before and for that column
                # if not we do nothing (all good!)
                if(last_index > last_date_valid_index):
                    df.loc[last_date_valid_index:, [col]
                           ] = df_updated.loc[last_date_valid_index:, [col]]
            else:
                df = df.append(
                    df_updated.loc[last_index + timedelta(days=1):, [col]])
    return df


def update_datas():
    global df_ranking, df_scores
    # fetch datas
    status_text = st.empty()
    my_bar = st.progress(0)
    [data_score, all_scores] = fetch_datas(status_text, my_bar)
    my_bar.empty()

    # Process ranking
    df_ranking_updated = pd.DataFrame({
        'names': data_names,
        'scores': data_score
    })
    df_ranking = update_df_ranking(df_ranking, df_ranking_updated)
    df_ranking.to_csv("data/df_ranking.csv", sep="\t")

    # Process scores
    df_scores_updated = pd.DataFrame(
        all_scores,
        columns=data_names
    )
    df_scores_updated['date'] = date_list
    df_scores_updated = df_scores_updated.set_index('date')
    df_scores_updated.index = pd.to_datetime(df_scores_updated.index)
    df_scores = update_df_scores(df_scores, df_scores_updated)
    df_scores.to_csv("data/df_scores.csv", sep="\t")

    write_last_update()
    return
