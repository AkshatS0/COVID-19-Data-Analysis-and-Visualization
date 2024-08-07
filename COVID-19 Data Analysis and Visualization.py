import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("covid_19_clean_complete.csv", parse_dates = ['Date'])
df.head()

# Renaming columns for easy usage
df.rename(columns = {'Date': 'date',
                      'Province/State': 'state',
                      'Country/Region': 'country',
                      'Lat' : 'lat', 'Long': 'long',
                      'Confirmed' : 'confirmed',
                      'Deaths' : 'deaths',
                      'Recovered' : 'recovered'},
            inplace = True)

# Active Cases
df['active'] = df['confirmed'] - df['deaths'] - df['recovered']

# combining the latest data for the countries
top = df[df['date'] == df['date'].max()]
world = top.groupby('country')['confirmed', 'active', 'deaths'].sum().reset_index()
world.head()

figure = px.choropleth(world, locations = 'country',
                        locationmode = 'country names', color = 'active',
                        hover_name = 'country', range_color = [1,1000],
                        color_continuous_scale = "greens",
                        title = "Countries with Active Cases")

figure.show()

# Determine the Total Confimed Cases grouped by Date
total_cases = df.groupby('date')['date', 'confirmed'].sum().reset_index()
total_cases.head()

plt.figure(figsize = (10,8))
plt.xticks(rotation = 90, fontsize= 10)
plt.yticks (fontsize = 15)
plt.xlabel("Dates", fontsize = 30)
plt.ylabel("Total Cases", fontsize = 30)
plt.title("Worldwide Confirmed Cases Over Time", fontsize = 30)

ax = sns.pointplot(x = total_cases.date.dt.date, y = total_cases.confirmed, color = 'r')
ax.set(xlabel = 'Dates', ylabel = 'Total Cases')

# Current Top Countries having most Active Cases
top_actives = top.groupby(by = 'country')['active'].sum().sort_values(ascending=False).head(20).reset_index()

plt.figure(figsize = (15,10))
plt.xticks(fontsize= 15)
plt.yticks (fontsize = 15)
plt.xlabel("Total Cases", fontsize = 30)
plt.ylabel("Country", fontsize = 30)
plt.title("Top 20 countries having most active cases", fontsize = 30)

ax = sns.barplot(x = top_actives.active, y = top_actives.country)

for i, (value, name) in enumerate(zip(top_actives.active, top_actives.country)):
    ax.text(value, i-.05, f'{value:,.0f}', size=10, ha ='left', va = 'center')

ax.set(xlabel = 'Total cases', ylabel = 'Country')

# Data of China
china = df[df.country == 'China']
china = china.groupby(by = 'date')['recovered', 'deaths', 'confirmed', 'active'].sum().reset_index()
china.head()

# Data of USA
us = df[df.country == 'US']
us = us.groupby(by = 'date')['recovered', 'deaths', 'confirmed', 'active'].sum().reset_index()
us = us.iloc[33:].reset_index().drop('index', axis = 1)
us.head()

# Data of Italy
italy = df[df.country == 'Italy']
italy = italy.groupby(by = 'date')['recovered', 'deaths', 'confirmed', 'active'].sum().reset_index()
italy = italy.iloc[9:].reset_index().drop('index', axis = 1)
italy.head()

india = df[df.country == 'India']
india = india.groupby(by = 'date')['recovered', 'deaths', 'confirmed', 'active'].sum().reset_index()
india = india.iloc[8:].reset_index().drop('index', axis = 1)
india.head()

plt.figure(figsize=(15,10))
sns.pointplot(x =china.index, y=china.confirmed, color='red')
sns.pointplot(x =us.index, y=us.confirmed, color='green')
sns.pointplot(x =italy.index, y=italy.confirmed, color='blue')
sns.pointplot(x =india.index, y=india.confirmed, color='orange')
plt.title('Confirmed Cases Over Time', fontsize = 25)
plt.xlabel('No. Of Days', fontsize = 15)
plt.ylabel('Confirmed Cases', fontsize = 15)
plt.show()

plt.figure(figsize=(15,10))

sns.pointplot(x = china.index, y = china.deaths, color='red')
sns.pointplot(x = us.index,y =  us.deaths, color='green')
sns.pointplot(x = italy.index,y = italy.deaths, color='blue')
sns.pointplot(x = india.index,y = india.deaths, color='orange')
plt.title('Death Cases Over Time', fontsize = 25)
plt.xlabel('No. Of Days', fontsize = 15)
plt.ylabel('Death Cases', fontsize = 15)
plt.show()

plt.figure(figsize=(15,10))

sns.pointplot(x=china.index,y= china.recovered, color='red')
sns.pointplot(x =us.index,y = us.recovered, color='green')
sns.pointplot(x = italy.index,y= italy.recovered, color='blue')
sns.pointplot(x =india.index,y = india.recovered, color='orange')
plt.title('Recovered Cases Over Time', fontsize = 25)
plt.xlabel('No. Of Days', fontsize = 15)
plt.ylabel('Recovered Cases', fontsize = 15)
plt.show()

"""# Detailed Analysis of COVID Cases in India"""

df_india = pd.read_excel('covid_19_india.xlsx')
df_india.head()

df_india['Total Cases'] = df_india['Total Confirmed cases (Indian National)'] + df_india['Total Confirmed cases ( Foreign National )']

df_india['Total Active'] = df_india['Total Cases'] - (df_india['Death'] + df_india['Cured'])
total_active = df_india['Total Active'].sum()
print('Total Number of Active COVID 19 cases across India', total_active)
Tot_Cases = df_india.groupby('Name of State / UT')['Total Active'].sum().sort_values(ascending = False).to_frame()
Tot_Cases.style.background_gradient(cmap='hot_r')

f,ax= plt.subplots(figsize=(12,8))
data = df_india[['Name of State / UT','Total Cases','Cured','Death']]
data.sort_values('Total Cases', ascending=False, inplace = True)
sns.set_color_codes("pastel")
sns.barplot(x="Total Cases", y="Name of State / UT", data=data, label="Total", color ="r")

sns.set_color_codes("muted")
sns.barplot(x="Cured", y="Name of State / UT", data=data, label="Cured", color ="g")

ax.legend(ncol=2, loc="lower right", frameon = True)
ax.set(ylabel="States and UT", xlabel="Cases")

dbd_india = pd.read_excel('per_day_cases.xlsx',parse_dates=True, sheet_name='India')

fig = go.Figure()
fig.add_trace(go.Scatter(x=dbd_india['Date'], y=dbd_india['Total Cases'], mode='lines+markers', name='Total Cases'))
fig.update_layout(title_text='Trend of Coronavirus cases in India (Cumulative Cases)', plot_bgcolor='rgb(230, 230, 230)')
fig.show()
fig = px.bar(dbd_india, x="Date", y="New Cases", barmode='group', height=400)
fig.update_layout(title_text='Coronavirus cases in India on daily basis', plot_bgcolor='rgb(230, 230, 230)')
fig.show()

"""# Insights into COVID cases globally"""

df_confirmed = pd.read_csv('time_series_covid19_confirmed_global.csv')
df_recovered = pd.read_csv('time_series_covid19_recovered_global.csv')
df_deaths = pd.read_csv('time_series_covid19_deaths_global.csv')

df_confirmed.rename(columns = {'Country/Region':'Country'}, inplace=True)
df_recovered.rename(columns = {'Country/Region':'Country'}, inplace=True)
df_deaths.rename(columns = {'Country/Region':'Country'}, inplace=True)

df_confirmed.head()

df_recovered.head()

df_deaths.head()

df.head()

df2 = df.groupby(['date', 'country', 'state'])[['date', 'state', 'country', 'confirmed', 'deaths', 'recovered']]
df2.head()

df_india_cases = df.query('country == "India"').groupby("date")[['confirmed', 'deaths', 'recovered']].sum().reset_index()
india_confirmed, india_deaths, india_recovered = df_india_cases[['date', 'confirmed']], df_india_cases[['date', 'deaths']], df_india_cases[['date', 'recovered']]

df.groupby('date').sum().head()

confirmed = df.groupby('date').sum()['confirmed'].reset_index()
deaths = df.groupby('date').sum()['deaths'].reset_index()
recovered = df.groupby('date').sum()['recovered'].reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(x=confirmed['date'], y=confirmed['confirmed'], mode='lines+markers', name='confirmed', line = dict(color = 'blue')))
fig.add_trace(go.Scatter(x=deaths['date'], y=deaths['deaths'], mode='lines+markers', name='deaths', line = dict(color = 'red')))
fig.add_trace(go.Scatter(x=recovered['date'], y=recovered['recovered'], mode='lines+markers', name='recovered', line = dict(color = 'green')))
fig.update_layout(title_text='World wide COVID-19 Cases', xaxis_tickfont_size = 14, yaxis=dict(title='Number of Cases'), plot_bgcolor='rgb(230, 230, 230)')
fig.show()

"""# TimeSeries Analysis of COVID cases globally and India in Particular

### to install prophet in colab
"""

!pip install pystan~=2.14
!pip install fbprophet

from fbprophet import Prophet
import pandas as pd



import warnings;
warnings.simplefilter('ignore')

"""### taking the confirmed cases from the global dataset"""

confirmed.columns = ['ds', 'y']
confirmed['ds']= pd.to_datetime(confirmed['ds'])

"""1. interval_width is for selcting the samples out of population
2. periods is for the next coming days
3. forecast the target for the latest dates
"""

m = Prophet(interval_width=0.95)
m.fit(confirmed)
future=m.make_future_dataframe(periods=7)
future.tail()

"""1. yhat is the actual target
2. lower and upper are the ranges for the target
"""

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

confirmed_forecast_plot = m.plot(forecast)

"""1. we can observe on sunday and sat there are many new cases
2. on wed there are less cases
"""

confirmed_forecast_plot = m.plot_components(forecast)

"""1. same operation perform for the deaths of global dataset"""

deaths.columns = ['ds', 'y']
deaths['ds']= pd.to_datetime(deaths['ds'])

m = Prophet()
m.fit(deaths)
future=m.make_future_dataframe(periods=7)
future.tail()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

deaths_forecast_plot = m.plot(forecast)

deaths_forecast_plot = m.plot_components(forecast)

"""### for the recovered cases of the global dataset

"""

recovered.columns = ['ds', 'y']
recovered['ds']= pd.to_datetime(recovered['ds'])

m = Prophet()
m.fit(recovered)
future=m.make_future_dataframe(periods=7)
future.tail()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

recovered_forecast_plot = m.plot(forecast)

recovered_forecast_plot = m.plot_components(forecast)

"""### picking only indian confirmed cases"""

india_confirmed.columns = ['ds', 'y']
india_confirmed['ds']= pd.to_datetime(india_confirmed['ds'])

m = Prophet()
m.fit(india_confirmed)
future=m.make_future_dataframe(periods=7)
future.tail()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

india_confirmed_plot = m.plot(forecast)

india_confirmed_plot = m.plot_components(forecast)

"""### picking only indian death cases"""

india_deaths.columns = ['ds', 'y']
india_deaths['ds']= pd.to_datetime(india_deaths['ds'])

m = Prophet()
m.fit(india_deaths)
future=m.make_future_dataframe(periods=7)
future.tail()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

india_deaths_plot = m.plot(forecast)

india_deaths_plot = m.plot_components(forecast)

"""### picking only indian recovered cases"""

india_recovered.columns = ['ds', 'y']
india_recovered['ds']= pd.to_datetime(india_recovered['ds'])

m = Prophet()
m.fit(india_recovered)
future=m.make_future_dataframe(periods=7)
future.tail()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

india_recovered_plot = m.plot(forecast)

india_recovered_plot = m.plot_components(forecast)

