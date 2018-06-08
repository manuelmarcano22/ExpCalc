from flask import render_template,  flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, InputForm, SNRtimeForm
from app.compute import compute, bplot
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}, Sin(X)={:.4f}'.format(
            form.username.data, form.remember_me.data, sin(form.sin.data)))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/bokeh', methods=['GET', 'POST'])
def plot():
    form = InputForm()
    snrtimeform = SNRtimeForm()

    snr = snrtimeform.snr.data
    #So that grapg appears after submit
    if form.validate_on_submit():
        result = True
        #Call the bokeh plot
        t,u = compute(form.A.data, form.b.data,form.w.data, form.T.data)
        script, div, js, css = bplot(t,u)
        
        html = render_template(
                'tryhide.html',
                plot_script=script,
                plot_div=div,
                js_resources=js,
                css_resources=css,
                title='O',
                form=form,
                snrtimeform=snrtimeform,
                snr=snr,
                result=result)
    else:
        result = None 
        html = render_template(
                'tryhide.html',
                title='O',
                form=form,
                snrtimeform=snrtimeform,
                snr=snr,
                result=result)

    return encode_utf8(html)
    #return render_template('bokeh.html', title='O no', form=form, result=None)


