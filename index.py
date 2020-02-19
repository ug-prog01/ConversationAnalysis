from flask import Flask, jsonify, request, redirect, flash, render_template
import os
import transcription as ts
import action_items as ac
import analysis as sd
import get_topic as gp
import word_cloud as wc
import productivity as prod
import line_plot as lp
import os
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = "secret key"

if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

OUTPUT_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = OUTPUT_FOLDER

IMAGE_FOLDER = os.path.join('static', 'results')
app.config['OLO_FOLDER'] = IMAGE_FOLDER

# IMAGE_FOLDER = os.path.join('static', 'results')
# app.config['OLO_FOLDER'] = IMAGE_FOLDER

full_filename = os.path.join(app.config['OLO_FOLDER'], 'virtusa-logo.png')

ALLOWED_EXTENSIONS = set(['json', 'txt', 'wav'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def homepage():

  	return render_template('index.html', image=full_filename)


@app.route('/action_items', methods=['GET', 'POST'])
def action_items():
	if(request.method == 'POST'):
		if 'file' not in request.files:
			print('No file part')
			return redirect(request.url)
		file = request.files['file']
		if(file.filename == ''):
			flash('No file selected for uploading')
			return redirect(request.url)
			
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			filepath = str(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			action_file = ac.filter(filepath)
			flash('File successfully uploaded')
			action = os.path.join(app.config['OLO_FOLDER'], action_file)
			return render_template('action.html', image=full_filename, action_item=action, class1='upload-wrapper', hidden='none')
		else:
			flash('Allowed file types are json')
			return redirect(request.url)
	return render_template('action.html', image=full_filename, hidden='none')


@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
	if(request.method == 'POST'):
		if 'file' not in request.files:
			print('No file part')
			return redirect(request.url)
		file = request.files['file']
		if(file.filename == ''):
			flash('No file selected for uploading')
			return redirect(request.url)
			
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			filepath = str(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			images = sd.analysis_of_json(filepath)
			flash('File successfully uploaded')
			# print(images)
			# print(type(images))
			conf2 = os.path.join(app.config['OLO_FOLDER'], images[0])
			time2 = os.path.join(app.config['OLO_FOLDER'], images[1])
			print(conf2, time2)
			return render_template('analysis.html', image=full_filename, conf=conf2, time=time2, hidden='block')
		else:
			flash('Allowed file types are json')
			return redirect(request.url)
	return render_template('analysis.html', image=full_filename, hidden='none')


@app.route('/topicmodelling', methods=['GET', 'POST'])
def topicmodelling():
  # topic_info = request.form['topic_input']
	if(request.method == 'POST'):
		topic = request.form['topic_info']
		speaker_count = request.form['speaker_count']

		if 'file' not in request.files:
			print('No file part')
			return redirect(request.url)
		files = request.files.getlist('file')
		# if(file.filename == ''):
		# 	flash('No file selected for uploading')
		# 	return redirect(request.url)

		filename1 = secure_filename(files[0].filename)
		filename2 = secure_filename(files[1].filename)

		files[0].save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
		files[1].save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))

		filepath1 = str(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
		filepath2 = str(os.path.join(app.config['UPLOAD_FOLDER'], filename2))

		flash('File successfully uploaded')

		# print(filepath1, filepath2)

		plot_file = lp.plot_positivity_scores(int(speaker_count), filepath1)
		plot_file = os.path.join(app.config['OLO_FOLDER'], plot_file)
		modelling_file = gp.topic_modelling(filepath2)
		modelling_file[0] = os.path.join(app.config['OLO_FOLDER'], modelling_file[0])
		modelling_file[1] = os.path.join(app.config['OLO_FOLDER'], modelling_file[1])
		productivity_score = prod.get_productivity(topic, filepath2)
		return_list = wc.draw_word_clouds()
		
		flag = 0

		if(len(return_list) > 1):
			return_list[0] = os.path.join(app.config['OLO_FOLDER'], return_list[0])
			return_list[1] = os.path.join(app.config['OLO_FOLDER'], return_list[1])
			return render_template('topicmodelling.html', image=full_filename, lp=plot_file, mf1=modelling_file[0], mf2=modelling_file[1], prod=productivity_score, pos=return_list[0], neg=return_list[1], hidden='block', hidden1='block')
		else:
			return_list[0] = os.path.join(app.config['OLO_FOLDER'], return_list[0])
			return render_template('topicmodelling.html', image=full_filename, lp=plot_file, mf1=modelling_file[0], mf2=modelling_file[1], prod=productivity_score, pos=return_list[0], hidden='block', hidden1='none')

		# print(plot_file, modelling_file, productivity_score, return_list)
		# return str(productivity_score) + str('\n'+modelling_file) + str(return_list)
	return render_template('topicmodelling.html', image=full_filename, hidden='none', hidden1='none')
# , image=full_filename

@app.route('/transcription', methods=['GET', 'POST'])
def transcription():
	if(request.method == "POST"):
		json_fil = ''
		if(request.form['btn'] == 'Upload file'):
			
			if 'file' not in request.files:
				print('No file part')
				return redirect(request.url)
			
			file = request.files['file']
			if(file.filename == ''):
				flash('No file selected for uploading')
				return redirect(request.url)
				
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				filepath = str(os.path.join(app.config['UPLOAD_FOLDER'], filename))

				transcribed, json_fil = ts.transcription(filepath)
				
				with open(transcribed) as tx:
					data = tx.read()
				data = data.split('\n')
				print(len(data))
				data_olo = []
				
				for i in data:
					data_olo.append([str(i).split(':')])

				data_olo = data_olo[:len(data_olo) - 1]
				# for i in data:
				# 	print(i)
				flash('File successfully uploaded')

				return render_template('transcript.html', hidden='block', hidden1='block', sentences=data_olo, image=full_filename, json_file=json_fil, transc=transcribed)
			else:
				flash('Allowed file types are json')

				return redirect(request.url)


		elif(request.form['btn'] == 'Save edited Changes'):
			# print(request.form)
			speaker_data = request.form.getlist('speaker')
			transcript_data = request.form.getlist('transcript')
			# print(speaker_data)
			# print(transcript_data)
			transcript_data = list(zip(speaker_data, transcript_data))
			print(transcript_data)
			print(type(transcript_data))
			print('SAVE')
			updated_transcript = 'static/results/up_transcript.txt'
			with open(updated_transcript, 'w') as ut:
				for i in transcript_data:
					ut.write(str(i[0]) +': '+ str(i[1]) +'\n')

			with open(updated_transcript) as tx:
				data = tx.read()
			data = data.split('\n')
			print(len(data))
			data_olo = []
			
			for i in data:
				data_olo.append([str(i).split(':')])

			data_olo = data_olo[:len(data_olo) - 1]
			print('DONE. EDITED AND SAVED')

			return render_template('transcript.html', hidden='block', hidden1='none', sentences=data_olo, confirm='block', image=full_filename, transc=updated_transcript)

	return render_template('transcript.html', hidden='none', image=full_filename, hidden1='none')


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.debug = True
    app.run(host='0.0.0.0', port=port)


































# from flask import Flask, render_template, request, url_for, jsonify
# app = Flask(__name__)

# @app.route('/tests/endpoint', methods=['POST'])
# def my_test_endpoint():
#     input_json = request.get_json(force=True) 
#     # force=True, above, is necessary if another developer 
#     # forgot to set the MIME type to 'application/json'
#     print('data from client:', input_json)
#     dictToReturn = {'answer':42}
#     return jsonify(dictToReturn)

# if __name__ == '__main__':
#     app.run(debug=True)