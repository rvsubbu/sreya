import pandas as pd
import plotly.express as px
import plotly.io as pio

#import pdb; pdb.set_trace()

pio.renderers.default = "notebook_connected+pdf"

df_2020 = pd.read_csv('311_covid.csv', low_memory=False)
#print(df_2020.head())

df_2020["Created Date"] = pd.to_datetime(df_2020["Created Date"], format="%m/%d/%Y %I:%M:%S %p")
#print(df_2020.dtypes)

date_counts= df_2020.groupby(['Complaint Type']).resample('D', on='Created Date').size().reset_index(name='count_requests')
#print(date_counts)

fig = px.line(date_counts,x="Created Date",y="count_requests", color = 'Complaint Type', title="Complaints Over Time")
#fig.show()

start_date = '02-29-2020'
end_date = '04-01-2020'

mar_counts = df_2020[df_2020['Created Date'].between(start_date, end_date, inclusive="neither")].groupby('Complaint Type').size().to_frame().rename(columns={0: '2020'})
#print(mar_counts)

#merged_counts = date_counts[date_counts['Created Date'].between(start_date, end_date, inclusive="neither")].groupby('Complaint Type').size().to_frame()
#print(merged_counts)

mar_2019 = pd.read_csv('311_mar_2019.csv', low_memory=False)
mar_2019["Created Date"] = pd.to_datetime(mar_2019["Created Date"], format="%m/%d/%Y %I:%M:%S %p")
#print(mar_2019.dtypes)

start_date_2019 = '03-01-2019'
end_date_2019 = '03-31-2019'
mar_2019_counts = mar_2019[mar_2019['Created Date'].between(start_date_2019, end_date_2019, inclusive="neither")].groupby('Complaint Type').size().to_frame().rename(columns={0:'2019'})
print(mar_2019_counts)
merged_counts = pd.merge(mar_counts, mar_2019_counts, how="outer", on="Complaint Type")
merged_counts = merged_counts.astype(int, errors="ignore")
print(merged_counts)
#mar_counts = mar_counts.join(mar_2019_counts, how="outer", on="Complaint Type")
#print(mar_counts)

#merged_counts['2020'] = merged_counts['2020'].fillna(0)
#merged_counts['2019'] = merged_counts['2019'].fillna(0)
merged_counts["pct_change"] = 100.0 * ((merged_counts['2019'] - merged_counts['2020'])/merged_counts['2019'])
#print(merged_counts.round(2))
print(merged_counts.to_csv())

condition1 = merged_counts['2020'] >= 50
condition2 = merged_counts['pct_change'].abs() > 90.0
all_conditions = condition1 & condition2
top_changed = merged_counts[all_conditions]
print(top_changed)
print(type(top_changed))
print(type(top_changed.columns))

#top_complaints = top_changed['Complaint Type'].values
#print(top_complaints)
