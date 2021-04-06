import os
from flask import Flask, Response, request, abort, render_template_string, send_from_directory, redirect, url_for, request
from markupsafe import escape
from PIL import Image
from io import StringIO

app = Flask(__name__)

#trialSets is trialSetNum X question num X 3 [= 0: time, 1: App_num, 2: correct_answer_option]
trialSet = [
	[
		[ 10, 2, 0], # End Trial 6
		[ 20, 1, 1], # End Trial 1
		[ 15, 3, 0], # End Trial 2
		[ 10, 1, 1], # End Trial 3
		[ 45, 3, 1], # End Trial 4
		[ 10, 3, 0], # End Trial 5
		[ 30, 2, 0], # End Trial 7
		[ 15, 2, 1], # End Trial 8
		[ 15, 1, 0]  # End Trial 9
	], # End Trial Set 1
	[
		[ 45, 1, 1], # End Trial 15
		[ 20, 2, 1], # End Trial 14
		[ 10, 1, 1], # End Trial 13
		[ 15, 2, 0], # End Trial 12
		[ 30, 3, 0], # End Trial 11
		[ 10, 2, 1], # End Trial 10
		[ 15, 1, 0], # End Trial 9
		[ 15, 3, 0], # End Trial 8
		[ 20, 3, 1]  # End Trial 7
	]# End Trial Set 2
]

solo = True
questionNum = 0
ts_num = 0

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
<script src="http://luis-almeida.github.io/unveil/jquery.unveil.js" charset="utf-8"></script>
<script>
	$(document).ready(function() {
	$('img').unveil(1000);
	});
	const audio1 = new Audio("./audio/1.mp3");
	const audio2 = new Audio("./audio/2.mp3");
	const audio3 = new Audio("./audio/3.mp3");
</script>

</head>

<body>
<p> Trial number: "{{ t_num }}"
<table style="width:100%; height:100%; border:none;"> 
{% for image in images %}
	<tr>
		<td style="text-align: center; vertical-align: middle;">
	    	<a class="image" 
			href="{{ image.src[7:-4] }}" 
			style="width: {{ image.width }}px; height: {{ image.height }}px; position: relative; text-align: center; vertical-align: middle; top: 000px;">
			<img src="{{ image.src }}" data-src="{{ image.src }}" width="{{ image.width }}" height="{{ image.height }}" />  
			</a>
			<a href="{{ image.src[7:-4] }}">
				<H1 >{{ image.src[8:-4] }}
			</a>
		</td>
	</tr>
{% endfor %}
</table>
 <script>
audio1.play();
 </script>
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

<script src="https://code.jquery.com/jquery-1.10.2.min.js" charset="utf-8"></script>
<script src="http://luis-almeida.github.io/unveil/jquery.unveil.js" charset="utf-8"></script>
<script>
$(document).ready(function() {
$('img').unveil(1000);
});
</script>

</head>

<body>
<a class="back" href="/nxtTrial" ">
	<img src="./buttons/back.png" data-src="./buttons/back.png" href="\\nxtTrial" alt="HTML5 Icon" style="width:128px;height:128px;">
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


@app.route('/nxtTrial')
def nxtTrial():
	global questionNum
	questionNum += 1
	return redirect('/home')

@app.route('/')
@app.route('/index')
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
	# TODO: start ruinning the trialsets
	return render_template_string(HOME, **{
		'images': images, 't_num' : questionNum
	})

@app.route('/fitbit')
@app.route('/Fitbit')
def fitbit():
	global questionNum
	if questionNum >= 9:
		questionNum = 0
		return redirect('/setnum')
	ansOption = trialSet[ts_num][questionNum][2]
	bgImgUrl = "./bg/fitbit" + str(ansOption) + ".png"
	return render_template_string(APP, **{
	'bgimg': bgImgUrl
	})


@app.route('/weather')
@app.route('/Weather')
def weather():
	global questionNum
	if questionNum >= 9:
		questionNum = 0
		return redirect('/setnum')
	ansOption = trialSet[ts_num][questionNum][2]
	bgImgUrl = "./bg/weather" + str(ansOption) + ".png"
	return render_template_string(APP, **{
	'bgimg': bgImgUrl
	})


@app.route('/email')
@app.route('/Email')
def email():
	global questionNum
	if questionNum >= 9:
		questionNum = 0
		return redirect('/setnum')
	ansOption = trialSet[ts_num][questionNum][2]
	bgImgUrl = "./bg/email" + str(ansOption) + ".png"
	return render_template_string(APP, **{
	'bgimg': bgImgUrl
	})

@app.route('/setnum', methods=['GET', 'POST'])
def setTsNum():
	if request.method == 'POST':
		global questionNum
		ts_num = request.form['tsnum']
		questionNum = 0
		return redirect(url_for('index'))
	return '''<form method="post"> 
				<label for="fname">Trial set num:</label><br>
  				<input type="number" id="tsnum" name="tsnum"><br>
				<H1><input type=submit> 
			</form>'''

# def Start_nxt_Trial():
# 	string trial_line;
# 	if (questionNum > -1)
# 		trial_line = questionNum + ", " + 
# 						time_asked + ", " + Time.time + ", " + 
# 						trialSet[trialSetNum, questionNum, 1] + ", " + 
# 						trialSet[trialSetNum, questionNum, 2] + ", " + 
# 						GameObject.Find("Weather1").GetComponent<AppManager>().user_manual_override + ", " +
# 						GameObject.Find("Email2").GetComponent<AppManager>().user_manual_override + ", " +
# 						GameObject.Find("Fitbit3").GetComponent<AppManager>().user_manual_override;
# 		sessionLog.WriteLine(trial_line);
# 	questionNum++;
# 	if (questionNum < 9)
# 		time_to_ask_next_Q = trialSet[trialSetNum, questionNum, 0] + Time.time;
# 	else
# 		solo = false;
	
def Update_answer():
	trialSet[ts_num][2]

if __name__ == "__main__":
	# For running on Server
	#app.run(host = "0.0.0.0" , port = 4443, debug=True )
	# For running on localhodt:5000
	# Start running the trials
	app.run()


# //	{ 20, 2, 1}, // End Trial 10
# ////	{{ 20, 3, 4}, // End Trial 11
# //		{ 15, 2, 2}, // End Trial 12
# //		{ 10, 1, 2}, // End Trial 13
# //		{ 20, 2, 4}, // End Trial 14
# ////		{ 10, 1, 4} // End Trial 15
# //			{ 10, 2, 1}, // End Trial 6
# //			{ 10, 3, 3}, // End Trial 5
# //			{ 45, 3, 2}, // End Trial 4
# //			{ 10, 1, 1}, // End Trial 3
# //			{ 15, 3, 3}, // End Trial 2
# //			{ 20, 1, 4} // End Trial 1
# }