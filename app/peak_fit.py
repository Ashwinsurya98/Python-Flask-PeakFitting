def peak_fit(df,col,sp,ep,indices,i):
    from chart_studio import plotly
    import plotly.offline as py
    import plotly.graph_objs as go
    import plotly.express as px
    import numpy as np
    import peakutils
    x = [j for j in range(len(df))][sp:ep]
    y = df[col][sp:ep]
    y = y.tolist()
    def gaussian(x, mu, sig):
        return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
    if len(indices)<2:
        gaussian_y_1 = y
        x_values_1=x
        y_values_1=np.array(0)
        gaussian_params_1=np.array([0,0])
    else:
        left_gauss_bound = sp+indices[i-2]
        right_gauss_bound = sp+indices[i]

        x_values_1 = np.asarray(x[left_gauss_bound-sp:right_gauss_bound-sp])
        y_values_1 = np.asarray(y[left_gauss_bound-sp:right_gauss_bound-sp])
        try:
            gaussian_params_1 = peakutils.gaussian_fit(x_values_1, y_values_1, center_only=False)
            gaussian_y_1 = [gaussian(x_dummy, gaussian_params_1[1], 1.5) for x_dummy in x_values_1]
        except:
            gaussian_y_1 = y

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

    trace3 = go.Scatter(
        x=x_values_1,
        #x=[item_x + 1 for item_x in x_values_1],
        y=[item_y+gaussian_params_1[0]-y_values_1.std()  for item_y in gaussian_y_1],
        mode='lines',
        marker=dict(
            size=2,
            color='rgb(200,0,250)',
        ),
        name='Gaussian Fit'
    )

    data2 = [trace, trace2, trace3]
    py.plot(data2, filename='./app/templates/peakfit_plot.html', auto_open=False)
    if len(indices)<2:
        y1 = y
    else:
        y1=[item_y+gaussian_params_1[0]-y_values_1.std()  for item_y in gaussian_y_1]
        df[col][left_gauss_bound:right_gauss_bound]=y1
    return df
