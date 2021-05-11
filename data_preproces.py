import csv
import pandas as pd

temp_df = pd.read_csv("./Coding-Exercise/temperature_daily.csv")
# print(temp_df.head())

## 1. Parse date and replace the month as categorical value
t_df = pd.DataFrame(temp_df.date.str.split('-', 2).tolist(),
                    columns = ['year', 'month', 'day']).astype({'year':'int'})#, 'month':'int', 'day':'int'})

cat_month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
t_df['cat_month'] = t_df['month'].replace(['01','02','03','04','05','06','07','08','09','10','11','12'], cat_month)

## 월별로 최대 최저 기온
temp_df = pd.concat([temp_df, t_df], axis=1)
# print(temp_df.head())

max = temp_df.groupby(['year', 'month'], as_index=False)['max_temperature'].max().rename(columns={'max_temperature':'tot_max'})
min = temp_df.groupby(['year', 'month'], as_index=False)['min_temperature'].min().rename(columns={'min_temperature':'tot_min'})

temp_df = pd.merge(max, temp_df, how='inner', left_on=['year', 'month'], right_on=['year', 'month'])
temp_df = pd.merge(min, temp_df, how='inner', left_on=['year', 'month'], right_on=['year', 'month'])

temp2_data = temp_df[temp_df['year']>=2008]
temp2_data = temp2_data.astype({'year':'str'})
temp2_data['year_month'] = temp2_data[['year', 'month']].apply(lambda x: '-'.join(x), axis=1)

temp2_data.to_csv('latest_year_temperature.csv', index=False)

temp_df = pd.read_csv("latest_year_temperature.csv")
print(temp_df)
# 2. Save column and data as [Year, Month, Date(2002-03), Min, Max]