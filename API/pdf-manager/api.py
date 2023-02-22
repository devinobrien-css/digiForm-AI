from flask import Flask, current_app
from digiFormClasses import Member, Organization, Server
import json

class Api:

    app = Flask(__name__)
    server = Server() # Make new static test server

    myOrg = server.createOrg("ABC Construction")
    newForm = myOrg.generateNewForm("sample.pdf", "My Form", "01/01/01")

    myMember = Member("Test", "Member")
    myOrg.addMember(myMember)

    myOrg.sendFormRequest(newForm, myMember)


    # This member will retrieve all its form requests
    @app.route('/getAllForms/', methods = ['GET'])
    def getAllForms():
        
        
        dict = {  }
        for form in Api.myMember.activeForms:

            dict.update( {form.formID: {"index": form.formID,"complete": form.complete, "name": form.name, "due": form.due, "organizer": form.org.name}} )

        return dict
    
    # Specific form details from id. This id is not index of activeForms. We must search active forms for this formID.
    @app.route('/getForm/<id>/', methods = ['GET'])
    def getForm(id):
        form = None
        for f in Api.myMember.activeForms:
            print(id)
            if f.formID == int(id):
                form = f
                break
        if form:
            # We found the form!
            response = {"data": {"index": form.formID,"complete": form.complete, "name": form.name, "due": form.due, "organizer": form.org.name}}

            # Now add the fields
            fields = {}
            for field in form.fields:
                fields.update( 
                    { field.index: 
                     {"name": field.name, 
                      "index": field.index, 
                      "type": field.type, 
                      "value": field.value,
                      "rect": field.rect,

                      "singleSelectionOnly": field.singleChoice,
                      "groupName": field.choiceGroup,
                      "choiceName": field.choiceValue,
                      } } )
                
            response.update( {"fields": fields} )
            return response
        else:
            return "404 Form not found!"
    
    
    def __init__(self):
        self.app.run(debug=True)

    


