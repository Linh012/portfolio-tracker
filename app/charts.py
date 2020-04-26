# for data manipulation and analysis - data frame = 2 dimensional data structure
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from math import pi
from datetime import date  # classes for manipulating dates
import yfinance as yf  # for YAHOO! FINANCE web scraping

tools = "pan,box_zoom,wheel_zoom,save,reset"


def bubblesort_date(inv):  # recursive bubble sorting
    for x in range(len(inv)):
        try:
            if inv[x + 1].date_start < inv[x].date_start:
                inv[x], inv[x + 1] = inv[x + 1], inv[x]
                bubblesort_date(inv)
        except IndexError:
            pass
    return inv


def create_pricechart(x, y):
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
        if x.date_end == None or x.date_end >= date.today():
            if x.symbol in inv_dict:
                inv_dict[x.symbol] += x.amount
            else:
                inv_dict[x.symbol] = x.amount

    data = pd.Series(inv_dict).reset_index(
        name='value').rename(columns={'index': 'investment'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi

    try:
        data['color'] = Category20c[len(inv_dict)]
    except KeyError:
        pass

    p = figure(plot_height=350, title="Portfolio Diversity",
               tools=tools + ",hover", tooltips="@investment: @value", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='investment', source=data)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    return p


def create_numberofinvestmentschart(inv):
    inv, invdates, y = bubblesort_date(inv), [], []
    for x in inv:
        invdates.append(x.date_start)
    for _ in range(1, len(invdates) + 1):
        y.append(_)
    p = figure(tools=tools, title="Number of Investments Chart", plot_height=350, x_axis_type="datetime",
               x_axis_label='Datetime', y_axis_label='Number of investments')
    p.step(invdates, y, legend_label="Price", line_width=2)

    return p


def create_portfoliovalue(inv, data):
    inv, lstdate, y = bubblesort_date(inv), [], [0] * 30

    for _ in range(30):
        lstdate.append(data[inv[0].symbol].index[-30 + _])
        for x in inv:
            if x.date_start <= lstdate[_]:
                tickerSymbol = x.symbol
                cprice = data[tickerSymbol]['Close']
                originalprice = float(cprice[cprice.index[0]])
                newprice = float(cprice[cprice.index[1]]) or float(
                    cprice[cprice.index[2]])
                change = ((newprice - originalprice) / originalprice) + 1
                y[_] += x.amount * change

    p = figure(tools=tools, title="30 Day Portfolio Value Chart", plot_height=350, x_axis_type="datetime",
               x_axis_label='Datetime', y_axis_label='Amount')
    # add a line renderer with legend and line thickness
    p.line(lstdate, y, legend_label="Value", line_width=2)
    return p


def create_barchart(inv, data):
    lstdate, performance = [], [0] * 7
    for _ in range(7):
        lstdate.append(data[inv[0].symbol].index[-7 + _])
        for x in inv:
            if x.date_start <= lstdate[_]:
                tickerSymbol = x.symbol
                cprice = data[tickerSymbol]['Close']
                originalprice = float(cprice[cprice.index[0 + _]])
                newprice = float(cprice[cprice.index[1 + _]])
                percentchange = ((newprice - originalprice) /
                                 originalprice) * 100
                performance[_] += percentchange

    psort = sorted(performance)
    strdate = []
    for d in lstdate:
        strdate.append(d.strftime("%Y-%m-%d"))
    p = figure(x_range=strdate, title="7 Day Performance (%change)", plot_height=350,
               tools=tools)
    p.vbar(x=strdate, top=performance, width=0.9)
    p.xgrid.grid_line_color = None

    return p
