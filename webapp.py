import os
from flask import Flask, Response, request, abort, render_template_string, send_from_directory
from PIL import Image
from io import StringIO

app = Flask(__name__)

WIDTH = 320
HEIGHT = 180

HOME = '''
<!DOCTYPE html>
<html>
<head>
<title></title>
<meta charset="utf-8" />
<style>
body {
margin: 0;
background-color: #333;
}
.image {
display: inline-block;
margin: 3em 14px;
background-color: #444;
box-shadow: 0 0 10px rgba(0,0,0,0.3);

}

img {
display: block;
}
</style>
<script src="https://code.jquery.com/jquery-1.10.2.min.js" charset="utf-8"></script>
<script src="http://luis-almeida.github.io/unveil/jquery.unveil.min.js" charset="utf-8"></script>
<script>

$(document).ready(function() {
$('img').unveil(1000);
});
</script>
</head>
<body>

{% for image in images %}
	<a class="image" href="{{ image.src[7:-4] }}" style="width: {{ image.width }}px; height: {{ image.height }}px; position: relative; top: 000px;">
		<img src="{{ image.src }}" data-src="{{ image.src }}?w={{ image.width }}&amp;h={{ image.height }} " width="{{ image.width }}" height="{{ image.height }}" />  
	</a>
{% endfor %}
</body>
'''

APP = '''
<!DOCTYPE html>
<html>
<head>
<style>
body {
  background-image: url({{bgimg}});
  background-repeat: no-repeat;
  background-attachment: fixed; 
  background-size: 100% 100%;
}
</style>
</head>
<body>
<a class="back" href="/home" ">
	<img src="./buttons/back.png" href="\\home" alt="HTML5 Icon" style="width:128px;height:128px;">
</a>
</body>
</html>

'''


@app.route('/<path:filename>')
def image(filename):
	try:
		w = int(request.args['w'])
		h = int(request.args['h'])
	except (KeyError, ValueError):
		return send_from_directory('.', filename)

	try:
		im = Image.open(filename)
		im.thumbnail((w, h), Image.ANTIALIAS)
		io = StringIO.StringIO()
		im.save(io, format='JPEG')
		return Response(io.getvalue(), mimetype='image/jpeg')

	except IOError:
		abort(404)

	return send_from_directory('.', filename)

@app.route('/')
@app.route('/home')
def index():
	images = []
	for root, dirs, files in os.walk('./icons'):
		files.sort()
		for filename in [os.path.join(root, name) for name in files]:
			if not filename.endswith('.png'):
				continue
			im = Image.open(filename)
			w, h = im.size
			aspect = 1.0*w/h
			if aspect > 1.0*WIDTH/HEIGHT:
				width = min(w, WIDTH)
				height = width/aspect
			else:
				height = min(h, HEIGHT)
				width = height*aspect
			images.append({
				'width': int(width),
				'height': int(height),
				'src': filename
			})

	return render_template_string(HOME, **{
		'images': images
	})

@app.route('/fitbit')
def fitbit():
	return render_template_string(APP, **{
		'bgimg': "./bg/fitbit.png"
	})


@app.route('/weather')
def weather():
	# TODO: bad code can be same with argument
	# TODO: change the answer value before showing
		return render_template_string(APP, **{
		'bgimg': "./bg/weather.png"
	})


@app.route('/email')
def email():
		return render_template_string(APP, **{
		'bgimg': "./bg/email.png"
	})


if __name__ == "__main__":
	# For running on Server
	#app.run(host = "0.0.0.0" , port = 4443, debug=True )
	# For running on localhodt:5000
	app.run()
