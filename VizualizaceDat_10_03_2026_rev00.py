import pa0ndas as pd
import plotly.express as px
#import plotly.io as pio
#pio.renderers.default = "browser 

# 1. Data reading from  'data.csv'
# sep='\s+' can be spaces and tabs as separators
df = pd.read_csv('data.csv', sep=r'\s+', header=None, encoding='utf-16', 
                 names=['Datum', 'Cas', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6'])

# 2. Combining date and time into one column and converting to time format
df['Timestamp'] = pd.to_datetime(df['Datum'] + ' ' + df['Cas'], dayfirst=True)

# 3. Converting data to "long" format 
df_melted = df.melt(id_vars=['Timestamp'], 
                    #value_vars=['V1', 'V2', 'V3', 'V4', 'V5', 'V6'],
                    value_vars=['V1', 'V2','V4',],
                    var_name='Senzor', value_name='Teplota/Hodnota')

# 4. Create an interactive chart
fig = px.line(df_melted, x='Timestamp', y='Teplota/Hodnota', color='Senzor',
              title='Časový průběh hodnot (záznam po 10s)',
              labels={'Timestamp': 'Čas měření', 'Teplota/Hodnota': 'Naměřená hodnota [°C]'})

# Change the X-axis from time to categorical (shows only existing records)
fig.update_xaxes(type='category')

# Setting a fixed Y-axis range from 0 to 160
fig.update_yaxes(range=[0, 160])

# Viewing a chart in a browser
import keyboard

print("Zmáčkni 0 = Print na web, Zmáčkni 1 = Print do souboru graf.html")

while True:
    # WAiting for keyboard input
    if keyboard.is_pressed('0'):
        print("Print na web")
        fig.show()
        break  
    elif keyboard.is_pressed('1'):
        print("Print do souboru graf.html")
        # fig.show()0
        fig.write_html("graf.html")
        break  

        time.sleep(0.1)