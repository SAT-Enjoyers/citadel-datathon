import requests as rq
import pandas as pd

URL = '''https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0
&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450
&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0
&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id={}URN
&scale=left&cosd=1976-01-01&coed=2024-02-01&line_color=%234572a7
&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999
&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01
&line_index=1&transformation=lin&vintage_date=2024-04-11
&revision_date=2024-04-11&nd=1976-01-01'''

OUTPUT_DIR = 'udataset/unemployment_by_state.csv'
SEASONALLY_ADJUSTED = False
START_YEAR = 2010

def get_abbreviations():
    df_abbrev = pd.read_csv("geo/state_abbreviations.csv")[:-4]
    return df_abbrev.set_index('Abbreviation')['State'].to_dict()

def fix_puerto_rico(data):
    for i, item in enumerate(data):
        if item[1] == '.':
            if item[0].startswith('2020-03'):
                data[i][1] = '9.0' if SEASONALLY_ADJUSTED else '8.4'
            if item[0].startswith('2020-04'):
                data[i][1] = '9.0'

def get_data(state: str, state_full_name: str):
    print(state_full_name)
    
    # Make a response to the website
    response = rq.get(URL.format(state))
    
    # Turn response into list of lists
    data = response.text.split('\n')
    data = [item.split(',') for item in data][1:-1]
    
    data = [item for item in data if int(item[0][:4]) >= START_YEAR]
    
    if state == 'PR':
        fix_puerto_rico(data)
    
    data = [[state_full_name.lower(), item[0][:7], float(item[1])] for item in data]
    
    
    return data

if __name__ == '__main__':
    abbreviations = get_abbreviations()
    data = []
    
    for state, state_full_name in abbreviations.items():
        data += get_data(state, state_full_name)

    df = pd.DataFrame(data=data, columns=['State', 'YearMonth', 'UnemploymentRate'])
    df.to_csv(OUTPUT_DIR, index=False)
