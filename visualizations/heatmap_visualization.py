import plotly.express as px
import pandas as pd

def create_heatmap():
    data = pd.read_csv('data/cleaned_restaurant_data.csv')
    fig = px.density_mapbox(
        data, lat='latitude', lon='longitude', z='rating',
        radius=10, mapbox_style='stamen-terrain'
    )
    fig.show()

if __name__ == '__main__':
    create_heatmap()
