# Exposure Calculator

Future exposure calculator using flask. Temporary at calc.manuelpm.me


## Deployment

Using [gunicorn](http://gunicorn.org/) and Apache ProxyPass.

```bash
chmod +x gunicornrun.sh
./gunicornrun.sh
```

Run in port 5000

To-Do:
 - [x] Implement SNR formula for CCD
 - [ ] Need to get rid of unnecessary form in routes
 - [x] Finish index.html page. Changed for calculator
 - [ ] Create appropriate footer
 - [ ] Conda environment with .yml file
 - [ ] Dockerize the application
 - [ ] Make Bokeh plot responsive. Too wide in big monitor
 - [ ] Use systemd or supervisord to monitor process

