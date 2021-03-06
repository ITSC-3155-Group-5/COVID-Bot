import discord as d
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

TOKEN = 'BOT_TOKEN'
GUILD = 'ITSC 3155'

client = d.Client()

#lets us know that we are connected to a specific guild
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

#creating different graphs based on user specification
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    #help with commands
    if message.content == '!help':
        helpMessage = '!linechart - create a line chart with current data' + '\n' + '!barchart - create a bar chart with current data' + '\n' + '!'
        await message.channel.send(helpMessage)
    
    #create a line chart
    if message.content == '!linechart':
        df = pd.read_csv('CoronaTimeSeries.csv')
        df['Date'] = pd.to_datetime(df['Date'])

        data = [go.Scatter(x=df['Date'], y=df['Confirmed'], mode='lines', name='Death')]

        layout = go.Layout(title='Corona Virus Confirmed Cases From 2020-01-22 to 2020-03-17', xaxis_title='Date', yaxis_title="Number of Cases")

        fig = go.Figure(data=data, layout=layout)
        fig.write_image("fig2.png")

        await message.channel.send(file=d.File('fig2.png'))
        
    #create a barchart
    if message.content == '!barchart':
        df = pd.read_csv('CoronavirusTotal.csv')
        
        filtered_df = df[df['Country'] == 'US']

        filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        new_df = filtered_df.groupby(['State'])['Confirmed'].sum().reset_index()

        new_df = new_df.sort_values(by=['Confirmed'], ascending=[False]).head(20)

        data = [go.Bar(x=new_df['State'], y=new_df['Confirmed'])]
        
        layout = go.Layout(title='Corona Virus Confirmed Cases in The US', xaxis_title="States", yaxis_title="Number of confirmed cases")

        fig = go.Figure(data=data, layout=layout)
        fig.write_image("fig1.png")

        await message.channel.send(file=d.File('fig1.png'))

client.run(TOKEN)
