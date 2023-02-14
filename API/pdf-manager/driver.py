from digiFormClasses import Organization, Server
from pdfStructure import pdfResponse, Consts
from pdfManager import PdfGenerator
import os

# Sample Driver code 
server = Server()

myOrg = server.createOrg("ABC Construction")
Bob = myOrg.addMember("Bob") # Creates and adds the member. Then stores it here for testing
Joe = myOrg.addMember("Joe")

# Org creates the form
newForm = myOrg.generateNewForm("form3.pdf", "Student Form", "01/01/01")

# Can add responses that were for example emailed in
# TODO: NEXT ADD ABILITY TO SUBMIT ON BEHALF OF, IN ORGANIZATION FUNCTION
# -> submitOnBehalf(response, member) # this member will submit this response.
#myOrg.addExisitngResponses()


# Org sends the form to all members, Bob Recieves it (Bob)
myOrg.sendFormRequest(newForm, myOrg.members)

# Member clicks on the form our org just created.
# In practice, this will be set when a form is clicked in UI
# This object then will be used to display and prompt member to fill in the fields

Bob.selectForm(myOrg, 0)
Joe.selectForm(myOrg, 0)

# myForm.display() 

Bob.respondToField(0, "Bob")
Joe.respondToField(0, "Joe")

Joe.respondToField(1, Consts.checkBoxDisplayYes)

Bob.respondToField(2, "Math")
Joe.respondToField(2, "Science")

Bob.respondToField(3, "Summer")
Joe.respondToField(3, "Fall")

Bob.respondToField(5, Consts.checkBoxDisplayYes)
Joe.respondToField(5, Consts.checkBoxDisplayYes)
# Joe.respondToField(6, Consts.checkBoxDisplayYes)

#Submit the currently active form from the earlier selectForm call
# NOTE: This will occur from frontend when user presses submit button.
# Action: when server recieves it will download the document and store it in the correct directory.
Bob.submitFormResponse() 
Joe.submitFormResponse() 

# Generate excel 
PdfGenerator.generateExcel(newForm)

#TODO: 
# Fix weird text being hidden
# RADIO - strange behavior when changing response and when choosing not the first option. See commented out.
# RADIO - in generatePdf, must select the proper button and set it to yesState
# make directory for blank forms???
