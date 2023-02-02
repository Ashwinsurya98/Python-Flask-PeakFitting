def basic_plot(df):
    from chart_studio import plotly
    import plotly.offline as py
    import plotly.graph_objs as go
    import plotly.express as px
    fig = px.line(df,y=df.columns[0],hover_data=df.columns)

    buttonlist = []
    for col in df.columns:

          buttonlist.append(
            dict(
                args=['y',[df[str(col)]] ],
                label=str(col),
                method='restyle'
            )
          )

    fig.update_layout(
        title="Total Plot",
        yaxis_title="Value",
        xaxis_title="Column",
        # Add dropdown
        updatemenus=[
            go.layout.Updatemenu(
                buttons=buttonlist,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ],
        autosize=True
    )
    return py.plot(fig,filename='./app/templates/basic_plot.html', auto_open=False)

