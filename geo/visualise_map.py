# Dataset importing
import pandas as pd

# Geospatial data
import geopandas as gpd
from shapely.geometry import Polygon

# Plotting
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter

# Mathematical
from math import floor, ceil

SHAPEFILE = 'geo/cb_2022_us_state_500k'
EXCLUDE_STATES = ['PR', 'MP', 'GU', 'VI', 'AS']
OTHER_STATES = ['AK', 'HI']


def get_abbreviations():
    df_abbrev = pd.read_csv("geo/state_abbreviations.csv")
    return pd.Series(df_abbrev['Abbreviation'].values,
                     index=df_abbrev['State'].str.lower()).to_dict()


def plot_extra_territory(fig, ax_loc, territory_gdf, polygon):
    ax = fig.add_axes(ax_loc)
    ax.axis('off')
    territory_gdf.clip(polygon).plot(
        color=territory_gdf['value_color'],
        linewidth=0.8,
        ax=ax,
        edgecolor='0.8'
    )


def plot_state_data(df: pd.DataFrame,
                    val_column: str,
                    title: str = None,
                    col_title: str = None):
    # Convert the state names into their abbreviations
    abbreviation = get_abbreviations()
    df['state'] = df['state'].apply(lambda x: abbreviation[x])

    # Exclude outlier states from visualisations
    df = df[~df['state'].isin(EXCLUDE_STATES)]

    # ## Load the spacial data
    # Read in the geospatial data using `geopandas`
    gdf = gpd.read_file(SHAPEFILE)

    # Merge the geospatial with the state data
    gdf = gdf.merge(df, left_on='STUSPS', right_on='state')

    # Calculate the min and max values
    v_min = floor(gdf[val_column].min())
    v_max = ceil(gdf[val_column].max())

    # Create norm and Mapper for the colour conversion
    norm = mcolors.Normalize(vmin=v_min, vmax=v_max, clip=True)
    mapper = plt.cm.ScalarMappable(norm=norm, cmap=plt.cm.YlOrBr)

    # Calculate the colors for each state
    gdf['value_color'] = gdf[val_column].apply(
        lambda x: mcolors.to_hex(mapper.to_rgba(x)))

    # Create a re-projected gdf using EPSG 2163 for equal area projections
    visframe = gdf.to_crs({'init': 'epsg:2163'})

    # Create the figure
    fig, ax = plt.subplots(1, figsize=(18, 14))
    ax.axis('off')
    ax.set_title(title)

    # Color bar
    cbax = fig.add_axes([0.89, 0.21, 0.03, 0.31])   # [l,b,w,h]
    cbax.set_title(col_title)
    sm = plt.cm.ScalarMappable(cmap="YlOrBr",
                               norm=plt.Normalize(vmin=v_min, vmax=v_max))
    sm._A = []
    comma_fmt = FuncFormatter(lambda x, p: format(x/100, '.0%'))
    fig.colorbar(sm, cax=cbax, format=comma_fmt)
    tick_font_size = 16
    cbax.tick_params(labelsize=tick_font_size)

    # Create map
    for row in visframe.itertuples():
        if row.state not in OTHER_STATES:
            vf = visframe[visframe.state == row.state]
            c = gdf[gdf.state == row.state][0:1].value_color.item()
            vf.plot(color=c, linewidth=0.8, ax=ax, edgecolor='0.8')

    plot_extra_territory(
        fig=fig,
        ax_loc=[0.08, 0.17, 0.25, 0.19],
        territory_gdf=gdf[gdf.state == 'AK'],
        polygon=Polygon([(-170, 50), (-170, 72), (-140, 72), (-140, 50)])
    )

    plot_extra_territory(
        fig=fig,
        ax_loc=[.28, 0.20, 0.1, 0.1],
        territory_gdf=gdf[gdf.state == 'HI'],
        polygon=Polygon([(-160, 0), (-160, 90), (-120, 90), (-120, 0)])
    )

    return plt


if __name__ == "__main__":
    df = pd.read_csv("udataset/state_data.csv")
    val_column = 'below_poverty_line_percent'

    # Filter it so theres only one value per state
    df = df[df['year'] == 2022]
    df = df[['state', val_column]]

    # Adjust the values for easier plotting
    df[val_column] = df[val_column] * 100

    plot = plot_state_data(df, val_column, "Title", "Color title")
    plot.savefig("geo/test.png")
