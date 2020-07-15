import pandas as pd # For manipulation of data frames (2 dimensional data structures)
# For plotting graphs
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from math import pi # Pie chart calculations
from datetime import date  # For manipulating date object
import yfinance as yf  # For YAHOO! FINANCE web scraping

# Tools for charts and allows user to save chart as image
TOOLS = "pan,box_zoom,wheel_zoom,save,reset"


def bubblesort_date(inv, j):  # Recursive bubble sorting
    if j == 1:
        return
    else:
        for i in range(j-1): # Traverse the list
            # Swap elements if one is bigger than other
            if inv[i + 1].date_start < inv[i].date_start:
                inv[i], inv[i + 1] = inv[i + 1], inv[i]
    bubblesort_date(inv,j-1)
    return inv

# Create price chart of ticker symbol
def create_pricechart(x, y):
    # Add plot, axis, tools and labels
    p = figure(tools=TOOLS, title="Price Chart", x_axis_type="datetime",
               x_axis_label='Datetime', y_axis_label='Price')

    # Add a line with legend and line thickness of 2
    p.line(x, y, legend_label="Price", line_width=2)

    hover = HoverTool() # Add feature to show data when hovering over chart
    hover.tooltips = "<div style=padding=5px>Price:@y</div>"
    p.add_tools(hover)

    return p


def create_piechart(inv):
    inv_dict = {} # Python dictionary (map)

    for x in inv: # For every investment
        if x.date_end == None: # If investment is active
            if x.symbol in inv_dict: # If key in dictionary, add amount to value
                inv_dict[x.symbol] += x.amount
            else: # Else add key and set value to amount
                inv_dict[x.symbol] = x.amount

    #Pandas series = one-dimensional n-dimensional array with axis labels
    data = pd.Series(inv_dict).reset_index(
        name='value').rename(columns={'index': 'investment'})

    # Calculate angle of each unique ticker symbol
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi

    # Add color to sectors of pie chart
    try:
        data['color'] = Category20c[len(inv_dict)]
    except KeyError: # If no sectors, pass
        pass

    # Add plot, title, tools, hover feature and x range
    p = figure(plot_height=350, title="Portfolio Diversity",
               tools=TOOLS + ",hover", tooltips="@investment: @value", x_range=(-0.5, 1.0))

    # Add sectors
    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='investment', source=data)

    p.axis.axis_label = None # No axis label
    p.axis.visible = False # Hide axis
    p.grid.grid_line_color = None # Hide grid lines
    return p

# Create number of investments chart
def create_numberofinvestmentschart(inv):
    inv, invdates, y = bubblesort_date(inv, len(inv)), [], []
    for x in inv: #Add dates to x-axis
        invdates.append(x.date_start)
    for _ in range(1, len(invdates) + 1): #Add values to y-axis
        y.append(_)
    # Add plot, tools, title, labels and set x-axis data type
    p = figure(tools=TOOLS, title="Number of Investments Chart", plot_height=350, x_axis_type="datetime",
               x_axis_label='Datetime', y_axis_label='Number of investments')
    # Add step line with thickness 2
    p.step(invdates, y, legend_label="Price", line_width=2)

    return p

# Create 30 day porfolio value chart
def create_portfoliovalue(inv, data):
    inv, lstdate, y = bubblesort_date(inv, len(inv)), [], [0] * 30

    for _ in range(30): # Loop 30 times for 30 days
        lstdate.append(data[inv[0].symbol].index[-30 + _]) # Add date to list of dates
        for x in inv: # Nested loop - for every investment during that date
            if x.date_start <= lstdate[_]: # Investment must be active
                tickerSymbol = x.symbol
                cprice = data[tickerSymbol]['Close'] # Get close prices of ticker symbol

                # Calculate investment value
                originalprice = float(cprice[cprice.index[0]])
                newprice = float(cprice[cprice.index[1]]) or float(
                    cprice[cprice.index[2]])
                change = ((newprice - originalprice) / originalprice) + 1
                # Add to list which will result in accurate portfolio value that takes in account changes in values of investments
                y[_] += x.amount * change

    # Add plot, tools, title, labels and set x-axis data type
    p = figure(tools=TOOLS, title="30 Day Portfolio Value Chart", plot_height=350, x_axis_type="datetime",
               x_axis_label='Datetime', y_axis_label='Amount')
    # Add a line renderer with legend label and line thickness 2
    p.line(lstdate, y, legend_label="Value", line_width=2)
    return p

# Create bar chart of 7 day portfolio performance
def create_barchart(inv, data):
    lstdate, performance = [], [0] * 7
    for _ in range(7): # Loop 7 times (for 7 days)
        lstdate.append(data[inv[0].symbol].index[-7 + _]) # Add date to list of dates
        inv_dict = {} # Python dictionary (map)

        # Calculate portfolio value for the date
        for x in inv: # For every investment
            if x.date_end == None: # If investment is active
                if x.symbol in inv_dict: # If key in dictionary, add amount to value
                    inv_dict[x.symbol] += x.amount
                else: # Else add key and set value to amount
                    inv_dict[x.symbol] = x.amount
        psum = sum(inv_dict.values())

        # Calculate investment percentage change relative to investment size
        for x in inv: # Nested loop - for every investment during that date
            if x.date_start <= lstdate[_]: # Investment must be active
                tickerSymbol = x.symbol
                cprice = data[tickerSymbol]['Close'] # Get close prices of ticker symbol
                # Calculate investment value percentage change
                originalprice = float(cprice[cprice.index[0 + _]])
                newprice = float(cprice[cprice.index[1 + _]])
                percentchange = ((newprice - originalprice) /
                                 originalprice) * 100
                performance[_] += percentchange*(x.amount/psum)

    # Convert date objects to string objects
    strdate = []
    for d in lstdate:
        strdate.append(d.strftime("%Y-%m-%d"))

    # Add plot, x-axis, title, tools and plot height
    p = figure(x_range=strdate, title="7 Day Performance (%change)", plot_height=350,
               tools=TOOLS)
    # Add vertical bars
    p.vbar(x=strdate, top=performance, width=0.8)
    p.xgrid.grid_line_color = None #Hide x-axis grid lines

    return p
