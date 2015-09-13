# YouMu Web Server
- - -

## Usage

Before the first time use:

```
virtualenv env
```

When requirements changed (and the first time also):

```
./env/bin/pip install -r requirements.txt
```

General use:

```
python runserver.py
```

And visit [YouMu](http://0.0.0.0:5000)

You'll need [Node.js](http://nodejs.org/) to build the CSS from Sass.
After Node is installed, run

```
npm install --global gulp       # may require root
npm install
gulp                            # watch for changes
```

The gulp configuration includes a LiveReload server. You can get [the browser extension](http://go.livereload.com/extensions) to see stylesheet changes in real time.

## Knowledge Needed

### Front End
* AngularJS
* Asynchronous Web Design (AJAX jQuery)
* Responsive Web Design
* Self-Implemented Video Player

### Back End
* Python
* Flask
* MongoDB

