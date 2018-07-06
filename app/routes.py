from flask import render_template,  flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, InputForm, SNRtimeForm, CCDForm1, CCDForm2
from app.compute import bplot, snrarray, calctime, calcsnr
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


#@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def calc2():
    form = InputForm()
    snrtimeform = SNRtimeForm()
    ccdform1 = CCDForm1()

    #snr = request.form['choice-calc']
    #So that grapg appears after submit
    if ccdform1.validate_on_submit():
        result = True

        #Do the calculation based on selection:
        choice = request.form['choice-calc']
        
        #Define variables
        zeropoint = ccdform1.zeropoint1.data
        magnitude = ccdform1.magnitude1.data
        pixelscale = ccdform1.pixscale1.data
        skybrightness = ccdform1.skyb1.data
        radiusaperture = ccdform1.radius1.data
        readnoise = ccdform1.readnoise1.data
        gain = ccdform1.gain1.data
        darkcurrent = ccdform1.dark1.data


        if choice == 'snr':
            snr = snrtimeform.snr.data
            exptime = calctime(zeropoint, magnitude, pixelscale, 
                    skybrightness, radiusaperture, snr , readnoise, gain,darkcurrent)
            finalcalc = 'SNR: {}, Exposure Time: {} seconds. '.format(snr,exptime)
            
        elif choice == 'time':
            exptime = snrtimeform.exptime.data
            snr = calcsnr(zeropoint, magnitude, pixelscale, skybrightness, 
                            radiusaperture, exptime, readnoise, gain,darkcurrent)
            finalcalc = 'SNR: {}, Exposure Time: {} seconds. '.format(snr,exptime)
            
          
       #BOkeh plot from snrarray
        t,u = snrarray(zeropoint, magnitude, pixelscale, skybrightness, 
                radiusaperture, readnoise, gain,darkcurrent)

        #If wanted to plot
        script, div, js, css = bplot(t,u)
        
        html = render_template(
                'calc2.html',
                plot_script=script,
                plot_div=div,
                js_resources=js,
                css_resources=css,
                title='Exposure Time Calculator',
                form=form,
                snrtimeform=snrtimeform,
                finalcalc = finalcalc,
                ccdform1 = ccdform1,
                choice = choice,
                result=result)
    else:
        result = None
        choice = None
        html = render_template(
                'calc2.html',
                title='Exposure Time Calculator',
                form=form,
                snrtimeform=snrtimeform,
                ccdform1 = ccdform1,
                choice = choice,
                result=result)
    return encode_utf8(html)


#The same as calc2 but you get two forms with two different default options.
@app.route('/calc', methods=['GET', 'POST'])
def calc():
    form = InputForm()
    snrtimeform = SNRtimeForm()
    ccdform1 = CCDForm1()
    ccdform2 = CCDForm2()

    #snr = request.form['choice-calc']
    #So that grapg appears after submit
    if ccdform1.validate_on_submit() or ccdform2.validate_on_submit():
        result = True

        #Do the calculation based on selection:
        choice = request.form['choice-calc']
        choiceccd = request.form['choice-ccd']

        if choiceccd == 'ccd1':
            zeropoint = ccdform1.zeropoint1.data
            magnitude = ccdform1.magnitude1.data
            pixelscale = ccdform1.pixscale1.data
            skybrightness = ccdform1.skyb1.data
            radiusaperture = ccdform1.radius1.data
            readnoise = ccdform1.readnoise1.data
            gain = ccdform1.gain1.data
            darkcurrent = ccdform1.dark1.data

        elif choiceccd == 'ccd2':
            zeropoint = ccdform2.zeropoint2.data
            magnitude = ccdform2.magnitude2.data
            pixelscale = ccdform2.pixscale2.data
            skybrightness = ccdform2.skyb2.data
            radiusaperture = ccdform2.radius2.data
            readnoise = ccdform2.readnoise2.data
            gain = ccdform2.gain2.data
            darkcurrent = ccdform2.dark2.data


        if choice == 'snr':
            snr = snrtimeform.snr.data
            exptime = calctime(zeropoint, magnitude, pixelscale, 
                    skybrightness, radiusaperture, snr , readnoise, gain,darkcurrent)
            #exptime = snrtimeform.exptime.data
            #exptime = computeexptime(snr)
            finalcalc = 'Selected {}. SNR: {}, Exptime: {}. CCD selected: {}, ccdbins: {}, ccddark {}'.format(choice,snr,exptime,choiceccd,gain,darkcurrent)
            
        elif choice == 'time':
            exptime = snrtimeform.exptime.data
            snr = calcsnr(zeropoint, magnitude, pixelscale, skybrightness, 
                            radiusaperture, exptime, readnoise, gain,darkcurrent)
            #snr = snrtimeform.snr.data
            finalcalc = 'SSelected {}. SNR: {}, Exptime: {}. CCD selected: {}, ccdbins: {}, ccddark {}'.format(choice,snr,exptime,choiceccd,gain,darkcurrent)
            
          
       #BOkeh plot past example
        t,u = snrarray(zeropoint, magnitude, pixelscale, skybrightness, 
                radiusaperture, readnoise, gain,darkcurrent)

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
                ccdform1 = ccdform1,
                ccdform2 = ccdform2,
                result=result)
    else:
        result = None 
        html = render_template(
                'calc.html',
                title='O',
                form=form,
                snrtimeform=snrtimeform,
                ccdform1 = ccdform1,
                ccdform2 = ccdform2,
                result=result)

    return encode_utf8(html)
    #return render_template('bokeh.html', title='O no', form=form, result=None)
