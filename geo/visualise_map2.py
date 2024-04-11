import pandas as pd
import plotly.graph_objects as go


def get_abbreviations():
    df_abbrev = pd.read_csv("state_abbreviations.csv")
    return pd.Series(df_abbrev['Abbreviation'].values,
                     index=df_abbrev['State'].str.lower()).to_dict()


def get_state_figure(df_code, df_value, color_title, title) -> go.Figure:
    return go.Figure(
        data=go.Choropleth(
            locations=df_code,
            z=df_value.astype(float),
            locationmode='USA-states',
            colorscale='YlOrBr',
            autocolorscale=False,
            marker_line_color='white',
            colorbar_title=color_title,
            colorbar=dict(
                title_side='top',
                x=1.02
            )
        ),
        layout=dict(
            title={
                'text': title,
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            geo=dict(
                scope='usa',
                projection=go.layout.geo.Projection(type='albers usa'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)',
            ),
            width=800,
            height=450,
            margin=dict(l=10, r=10, t=50, b=0)
        )
    )


if __name__ == '__main__':
    # Read in the dataset
    df = pd.read_csv('../udataset/state_data.csv')
    VAL_COLUMN = 'below_poverty_line_percent'

    # Filter it so theres only one value per state
    df = df[df['year'] == 2022]
    df = df[['state', VAL_COLUMN]]
    df = df[df['state'] != 'puerto rico']
    df.reset_index(drop=True, inplace=True)

    # Adjust the values for easier plotting
    df[VAL_COLUMN] = df[VAL_COLUMN] * 100

    # Convert the state names into their abbreviations
    abbreviation = get_abbreviations()
    df['code'] = df['state'].apply(lambda x: abbreviation[x])

    # Make the figure
    fig = get_state_figure(
        df_code=df['code'],
        df_value=df[VAL_COLUMN],
        color_title='% in poverty',
        title='Percentage of people below the poverty line each state'
    )

    # fig.show() # In jupyter notebook
    fig.write_image("figure.svg")
    fig.write_image("figure.png")
