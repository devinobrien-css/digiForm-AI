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
newForm = myOrg.generateNewForm("form.pdf", "Sample Form", "01/01/01")


# myOrg.addExisitngResponses()


# Org sends the form to all members, Bob Recieves it (Bob)
myOrg.sendFormRequest(newForm, myOrg.members)

# Member clicks on the form our org just created.
# In practice, this will be set when a form is clicked in UI
# This object then will be used to display and prompt member to fill in the fields

Bob.selectForm(myOrg, 0)
Joe.selectForm(myOrg, 0)

# myForm.display() 

# Bob responds no to first checkbox
Joe.respondToField(0, Consts.checkBoxDisplayYes)
Bob.respondToField(1, "Sup bro")

# Bob.respondToField(0, "Bob")
# Joe.respondToField(0, "Joe")

#Submit the currently active form from the earlier selectForm call
# NOTE: This will occur from frontend when user presses submit button.
# Action: when server recieves it will download the document and store it in the correct directory.
Bob.submitFormResponse() 
Joe.submitFormResponse() 


#TODO: 
# Fix weird text being hidden
# fix empty form throw error with copyPages function
# check radio compatibility
# make directory for blank forms???
""""""