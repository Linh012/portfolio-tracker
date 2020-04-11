from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool

tools = "pan,box_zoom,wheel_zoom,save,reset"

def create_pchart(x,y):
        # create a new plot with a title and axis labels
    p = figure(tools=tools, title="Price Chart", x_axis_type="datetime",
               x_axis_label='Datetime', y_axis_label='Price')

    # add a line renderer with legend and line thickness
    p.line(x, y, legend_label="Price", line_width=2)
    hover = HoverTool()
    hover.tooltips = "<div style=padding=5px>Price:@y</div>"
    p.add_tools(hover)

    return p
