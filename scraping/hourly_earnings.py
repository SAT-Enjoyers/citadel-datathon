import requests as rq
import pandas as pd

URL = '''https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0
&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450
&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0
&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes
&id=SMU{}000000500000003&scale=left&cosd=2007-01-01&coed=2024-02-01
&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3
&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin
&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2024-04-12
&revision_date=2024-04-12&nd=2007-01-01'''

OUTPUT_DIR = 'udataset/hourly_earnings.csv'
START_YEAR = 1900


def get_abbreviations():
    df_abbrev = pd.read_csv("eda/geo/state_abbreviations.csv")[:-5]
    return df_abbrev.set_index('Abbreviation')['State'].to_dict()


def get_data(i: int, state_name: str):
    # Make a response to the website
    response = rq.get(URL.format(str(i).rjust(2, "0")))

    if response.status_code != 200:
        return []

    # Turn response into list of lists
    data = response.text.split('\n')
    data = [item.split(',') for item in data][1:-1]

    # Filter by year range
    data = [item for item in data if START_YEAR <= int(item[0][:4])]

    # Format raw data in row into the table
    data = [[state_name.lower(), item[0][:7], float(item[1])]
            for item in data]

    return data


if __name__ == '__main__':
    abbreviations = get_abbreviations()
    data = []

    i = 1
    states = sorted(abbreviations.values())
    while states:
        state_full_name = states[0]
        new_data = get_data(i, state_full_name)
        if new_data:
            data += new_data
            states.pop(0)
            print(state_full_name)
        i += 1

    df = pd.DataFrame(data=data,
                      columns=['State', 'YearMonth', 'HourlyEarnings'])
    df.to_csv(OUTPUT_DIR, index=False)
