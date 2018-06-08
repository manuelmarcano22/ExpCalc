from flask import render_template,  flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, InputForm, SNRtimeForm
from app.compute import compute, bplot, computeexptime
#Bokeh
from bokeh.util.string import encode_utf8
import glob
from random import randint

#Error handler
@app.errorhandler(404)
def page_not_found(e):
    lista = glob.glob('./**/static/Jokes/*.jpg', recursive=True)
    ra = randint(0,len(lista))
    names = lista[ra].split('/')[-1]
    return render_template('404.html',name=names), 404


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Manuel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/calc', methods=['GET', 'POST'])
def calc():
    form = InputForm()
    snrtimeform = SNRtimeForm()

    #snr = request.form['choice-calc']
    #So that grapg appears after submit
    if form.validate_on_submit():
        result = True

        #Do the calculation based on selection:
        choice = request.form['choice-calc']
        if choice == 'snr':
            snr = snrtimeform.snr.data
            exptime = snrtimeform.exptime.data
            exptime = computeexptime(snr)
            finalcalc = 'Selected {}. SNR: {}, Exptime: {}'.format(choice,snr,exptime)
            
        elif choice == 'time':
            snr = snrtimeform.snr.data
            exptime = snrtimeform.exptime.data
            exptime = computeexptime(snr)
            finalcalc = 'SSelected {}. SNR: {}, Exptime: {}'.format(choice,snr,exptime)
            
          
       #BOkeh plot past example
        t,u = compute(form.A.data, form.b.data,form.w.data, form.T.data)
        #If wanted to plot
        script, div, js, css = bplot(t,u)
        
        html = render_template(
                'calc.html',
                plot_script=script,
                plot_div=div,
                js_resources=js,
                css_resources=css,
                title='O',
                form=form,
                snrtimeform=snrtimeform,
                finalcalc = finalcalc,
                result=result)
    else:
        result = None 
        html = render_template(
                'calc.html',
                title='O',
                form=form,
                snrtimeform=snrtimeform,
                result=result)

    return encode_utf8(html)
    #return render_template('bokeh.html', title='O no', form=form, result=None)


