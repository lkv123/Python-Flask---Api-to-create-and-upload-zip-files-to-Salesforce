import base64
import zipfile
from flask import Flask
from flask_restful import Resource, Api, reqparse, request
import json
from simple_salesforce import Salesforce
import requests

app = Flask(__name__)
api = Api(app)

userName = 'test216@test.com'
password = 'SoujanyaDec01'
securityToken = '5TFQGZqXzmheyvYcxvGc1zHc'
instance = 'AP4'

class postFiles(Resource):
    #code here


    def post(self):
        sf = Salesforce(username=userName, password=password, security_token=securityToken)
        sessionId = sf.session_id
        parser = reqparse.RequestParser()
        data = request.data

        base64string1 = json.loads(data)['base64_filebody']
        decodedstring1 = base64.b64decode(base64string1)
        output_file = open(json.loads(data)['filename']+'.txt', 'w+', encoding="utf-8")
        output_file.write(decodedstring1.decode("utf-8"))
        filepath = 'ZipFileSample1.zip'
        with zipfile.ZipFile(filepath, 'a') as zipf:
            zipf.writestr(json.loads(data)['filename']+'.txt', decodedstring1)
        #body = base64.b64encode(filepath.read())
        #with open(filepath, "rb") as f:
         #   bytes = f.read()
          #  encoded = base64.b64encode(bytes)

        with open(filepath, 'rb') as open_file:
            byte_content = open_file.read()
        base64_bytes = base64.b64encode(byte_content)
        base64_string = base64_bytes.decode('utf-8')

        response = requests.post('https://%s.salesforce.com/services/data/v50.0/sobjects/ContentVersion/' % instance,
                                 headers={'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % sessionId},
                                 data=json.dumps({
                                     'Title': filepath,
                                     'PathOnClient': filepath,
                                     'VersionData': base64_string

                                 })
                            )

        return {'data': json.loads(response.text)["id"]}, 200
api.add_resource(postFiles, '/postFiles')

if __name__ == '__main__':
    app.run()  # run our Flask app