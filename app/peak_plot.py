def peak_plot(df,col,sp,ep):
    from chart_studio import plotly
    import plotly.offline as py
    import plotly.graph_objs as go
    import plotly.express as px
    import numpy as np
    import peakutils
    x = [j for j in range(len(df))][sp:ep+1]
    y = df[col][sp:ep+1]
    y = y.tolist()
    cb = np.array(y)
    indices = peakutils.indexes(cb, thres=0.75, min_dist=1)
    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines',
        marker=dict(
            color='rgb(0,56,210)'
        ),
        name='Highlighted Plot'
    )

    trace2 = go.Scatter(
        x=indices + sp,
        y=[y[j] for j in indices],
        mode='markers',
        marker=dict(
            size=8,
            color='rgb(255,0,0)',
            symbol='cross'
        ),
        name='Detected Peaks'
    )

    data1 = [trace, trace2]
    py.plot(data1, filename='./app/templates/peak_plot.html', auto_open=False)
    return indices
