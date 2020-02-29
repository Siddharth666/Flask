from flask import Flask, jsonify, request, json

from flask_pymongo import PyMongo

from flask_cors import CORS

from flask_mail import Mail, Message

import speech_recognition as sr
import webbrowser

import WebScraping

#from flask_ext import excel
import flask_excel as excel

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'resthub'
#app.config['MONGO_URI'] = 'mongodb://username:password@hostname:port/databasename'
app.config['MONGO_URI'] = 'mongodb://localhost/resthub'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'datamoulds2016@gmail.com'
app.config['MAIL_PASSWORD'] = 'Tombofstone1987$'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mongo = PyMongo(app)

@app.route('/framework', methods=['GET'])
def get_all_frameworks():
    framework = mongo.db.framework 

    output = []

    for q in framework.find():
        output.append({'name' : q['name'], 'language' : q['language']})

    return jsonify({'result' : output})

@app.route('/framework/<name>', methods=['GET'])
def get_one_framework(name):
    framework = mongo.db.framework

    q = framework.find_one({'name' : name})

    if q:
        output = {'name' : q['name'], 'language' : q['language']}
    else:
        output = 'No results found'

    return jsonify({'result' : output})

@app.route('/framework/<name>', methods=['DELETE'])
def delete_one_framework(name):
    framework = mongo.db.framework

    q = framework.find_one({'name' : name})

    if q:
        framework_id = framework.remove({'name': name})
    output = {'name': name, 'Deleted': 'Sucessfully'}

    return jsonify({'result' : output})

@app.route('/framework/<name>', methods=['PUT'])
def update_one_framework(name):
    framework = mongo.db.framework

    q = framework.find_one({'name' : name})

    if q:
        #framework_id = framework.update({'name' : name, 'language' : language})
        app.logger.info('hehe')
        
        namess = request.json['name']
        language = request.json['language']

        framework_id = framework.update_one({'name' : name}, {"$set": {'name': namess,'language': language}})

        #new_framework = framework.find_one({'_id' : framework_id})

        output = {'message':'Successfully updated'}

        return jsonify({'result' : output})
 


@app.route('/framework', methods=['POST'])
def add_framework():
    framework = mongo.db.framework
   
    name = request.json['name']
    language = request.json['language']

    framework_id = framework.insert({'name' : name, 'language' : language})
    new_framework = framework.find_one({'_id' : framework_id})

    output = {'name' : new_framework['name'], 'language' : new_framework['language']}
    

    return jsonify({'result' : output})

mail = Mail(app)
@app.route('/frameworkEmail', methods=['POST'])
def SendEmail_framework():
    #framework = mongo.db.framework
   
    EmailId = request.json['EmailId']
    Messages = request.json['Messages']
    SenderEmail = 'datamoulds2016@gmail.com'

    msg = Message(sender="datamoulds2016@gmail.com", recipients=[EmailId])
    
    msg.body = Messages
    mail.send(msg)
    return jsonify({'Result': "Success"})

@app.route('/VoiceMessage', methods=['POST'])
def Voice_Mail():
    r =sr.Recognizer()
  
    with sr.Microphone() as source:
        print('Speak Something: ')
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print('You said: {}'.format(text))
            url = "https://google.com/search?q="+text
            webbrowser.get().open(url)
        except:
            print('Error occured')
    return jsonify({'result': text})


@app.route('/SayName', methods=['POST'])
def Say_Name():
    r1 =sr.Recognizer()
  
    with sr.Microphone() as source:
        print('Speak Something: ')
        audio1 = r1.listen(source)

        try:
            text1 = r1.recognize_google(audio1)
            print('You said: {}'.format(text1))
        except:
            print('Error occured')
    return jsonify({'result': text1})

# @app.route("/frameworks", methods=['GET'])
# def export_records():
    
#     framework = mongo.db.framework 

#     output = []

#     for q in framework.find():
#         output.append({q['name'], q['language']})

#     return excel.make_response_from_array([["Name", "Language"], [output[1], output[0]]], "csv", file_name="impp")

if __name__ == '__main__':
    excel.init_excel(app)
    app.run(debug=True)