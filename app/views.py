from fileinput import filename
from flask import *
from app import app
from app import basic_plot
from app import peak_plot
from app import peak_fit
import pandas as pd
# import peakutils

@app.route("/")
def index():
    return render_template("main.html")

@app.route('/success', methods = ['GET','POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)  
        file_name='../../'+f.filename
        session['file_name']=file_name
        df=pd.read_csv(file_name)
        basic_plot.basic_plot(df)
        return render_template('basic_view.html',col=list(df.columns),mrang=len(df))
    else:
        file_name = session.get('file_name', None)
        df=pd.read_csv(file_name)
        basic_plot.basic_plot(df)
        return render_template('basic_view.html',col=list(df.columns),mrang=len(df))

@app.route('/peak', methods = ['GET','POST'])  
def peak():
    if request.method == 'POST': 
        if int(request.form.get("StartingPoint"))<0: 
            flash('Starting Point should be greater than 0')
            return redirect(url_for('success'))              
        file_name = session.get('file_name', None)
        df=pd.read_csv(file_name)
        if int(request.form.get("EndingPoint"))>len(df): 
            flash('Ending Point entered is greater than '+str(len(df)))
            return redirect(url_for('success')) 
        if int(request.form.get("EndingPoint"))<int(request.form.get("StartingPoint")): 
            flash('Ending Point should be greater than Starting Point')
            return redirect(url_for('success'))
        session['col']=request.form.get("Column")
        session['sp']=int(request.form.get("StartingPoint"))
        session['ep']=int(request.form.get("EndingPoint"))
        session['indexes']=peak_plot.peak_plot(df,session['col'],session['sp'],session['ep'])
        indexes=peak_plot.peak_plot(df,session['col'],session['sp'],session['ep'])
        return render_template("peak_view.html",ind_range=len(indexes))
    else:
        file_name = session.get('file_name', None)
        df=pd.read_csv(file_name)
        col = session.get('col', None)
        sp = session.get('sp', None)
        ep = session.get('ep', None)
        indexes=session.get('indexes', None)
        return render_template("peak_view.html",ind_range=len(indexes))

@app.route('/peak_index', methods = ['POST'])  
def peak_index():
    if request.method == 'POST':
        ind=int(request.form.get("index"))
        file_name = session.get('file_name', None)
        df=pd.read_csv(file_name)
        col = session.get('col', None)
        sp = session.get('sp', None)
        ep = session.get('ep', None)
        indexes=session.get('indexes', None)
        if ind not in range(1,len(indexes)+1):
            flash('Select indexes from the range')
            return redirect(url_for('peak'))
        up_df=peak_fit.peak_fit(df,col,sp,ep,indexes,ind)
        up_df.to_csv("./app/output/Peakfit.csv",index=False)
        return render_template("peakfit_view.html")

@app.route('/download')
def download():
    path = "./output/Peakfit.csv"
    return send_file(path, as_attachment=True)

@app.route('/repeat',methods=['GET'])
def repeat():
    if request.method == 'GET':
        session['file_name']="./app/output/Peakfit.csv"
        return redirect(url_for('success'))