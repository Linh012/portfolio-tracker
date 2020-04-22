import pandas as pd  #for data manipulation and analysis - data frame = 2 dimensional data structure
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from math import pi
from datetime import date #classes for manipulating dates

tools = "pan,box_zoom,wheel_zoom,save,reset"

def create_pricechart(x,y):
        # create a new plot with a title and axis labels
    p = figure(tools=tools, title="Price Chart", x_axis_type="datetime",
               x_axis_label='Datetime', y_axis_label='Price')

    # add a line renderer with legend and line thickness
    p.line(x, y, legend_label="Price", line_width=2)
    hover = HoverTool()
    hover.tooltips = "<div style=padding=5px>Price:@y</div>"
    p.add_tools(hover)

    return p

def create_piechart(inv):
    inv_dict = {}
    for x in inv:
        if x.date_end == None or x.date_end>=date.today():
            if x.symbol in inv_dict:
                inv_dict[x.symbol] += x.amount
            else:
                inv_dict[x.symbol] = x.amount

    data = pd.Series(inv_dict).reset_index(name='value').rename(columns={'index':'investment'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(inv_dict)]

    p = figure(plot_height=350, title="Portfolio Diversity",
               tools=tools+",hover", tooltips="@investment: @value", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='investment', source=data)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None
    return p
