from pdfManager import PdfGenerator
from pdfStructure import *
import os

# Server class 
class Server:
    orgs = [] # A list of all organizations

    # NOTE: Is this necessary? Can we just pass Organization object around?
    def getOrgByID(self, id):
        return self.orgs[id]

    # Create, return and store a new organization
    def createOrg(self, name):
        newOrg = Organization(name)
        self.orgs.append(newOrg)
        return newOrg



# Member class
class Member:
    def __init__(self, name):
        self.name = name
        self.currentForm = None # The request we are viewing / modifying
        self.activeForms = [] # Requests that are in progress

    # Member selects this form. A request object exists already if we can see it. When we click it this happens.
    def selectForm(self, org, formID):
        # iterate over active forms to see if we already have data for this request
        for req in self.activeForms:
            if ((req.org == org) and (req.formID == formID)):
                # This requests matches our selection (org and ID match) so we already started it
                self.currentForm = req
                return self.currentForm

    # This member has been sent a form to complete, this is the request object
    def receiveFormRequest(self, req):
        self.activeForms.append(req)
        # TODO: UI updates and creates a visual form button for each req object, incl new one

    # This member wants to submit the form they currently are editing.
    def submitFormResponse(self):
        # No need to check currentForm is valid here, because submit button will only appear if it is.
        # We must call a recieveFormResponse in the Organization.
        # In that function, it will be appended to the list of responses. 
        # Then it can be clicked on, at which point the generatePDf(from response) will occur.

        org = self.currentForm.org
        fields = self.currentForm.fields
        formID = self.currentForm.formID
        # We need the responder's ID.. or can we just pass the responder object themself?
        # I will try to pass responder but I'm wondering how passing objects over the network will be
        # as opposed to passing the ID and then finding the object at the other end.
        
        response = pdfResponse(self, "Current_Date", fields, formID, org)
        org.receiveFormResponse(response)




    # Member updates a field in the currently selected response
    # We need to look at the fields and see if this one exists 
    # to know whether to create a new object or update existing.
    # NOTE: the fieldIndex will be the ChildIndex of this button in the scroll box
    # when the client is looking at all fields.

    def respondToField(self, fieldIndex, fieldValue):
        response = self.getFieldByIndex(fieldIndex)

        # NOTE: This will always be true, because we add all fields by default!
        if (response != None):
            response.value = fieldValue
            # print("UPDATED VALUE FOR "+self.name+" TO "+ fieldValue)


        # NOTE: We can not search by name because radio buttons share a name.
        # TODO: Current write method (genPDF) uses name though i think...

    # Return field with this index (NOT "at this index", not necessarily ordered by index, but probably is.)
    def getFieldByIndex(self, index):
        fields = self.currentForm.fields
        for field in fields:
            if (field.index == index):
                return field
        return None # Error field not here! Every field in the form shold be copied!
    


# Organization class
class Organization:

    # A new organization is formed
    # Begin with a name and an empty list of forms.
    def __init__(self, name):
        self.name = name
        self.forms = []
        self.responses = [] # Must be filtered by FormID
        self.members = []

    # NOTE: This should probably add a Member object. at a minimum, it needs to take more info
    # so that we can properly manage and reference the member
    def addMember(self, name):
        newMember = Member(name)
        self.members.append(newMember)
        return newMember


    # Return form object by ID
    def getFormByID(self, id):
        return self.forms[id]

    # Organization wants to create a new form using the button. 
    # It must be given a new formID, the number of created forms.
    # returns the form object
    def generateNewForm(self, path, title, due):

        formID = len(self.forms)
        newForm = PdfGenerator.generateForm(path, title, formID, due, self)
        self.forms.append(newForm)
        return newForm

    # Send a request of this form to this target. Can be a list, or singleton
    # NOTE: Called from: UI "Send Form" button from desktop by organization
    def sendFormRequest(self, form, targets):

        try:
            some_object_iterator = iter(targets)
        except TypeError as te:
            # Not iterable (singleton)
            fields = []
            for field in form.fields[:]:
                newField = pdfElement(field.name, field.type, field.value, field.index)
                fields.append(newField)

            newReq = pdfRequest(form.name, form.due, self, fields, form.formID)
            targets.receiveFormRequest(newReq)
            return

        for target in targets:
            # Create the request and call recieve in member
            fields = []
            for field in form.fields[:]:
                newField = pdfElement(field.name, field.type, field.value, field.index)
                fields.append(newField)
                
            newReq = pdfRequest(form.name, form.due, self, fields, form.formID)
            target.receiveFormRequest(newReq)

    # We have recieved a member's response! Append it and refresh our view list.
    # We must store this updated list to save the responses on the server
    def receiveFormResponse(self, response):
        self.responses.append(response)
        # TODO: Here we will refresh the UI on desktop to show the new response, and store the new result (database?)
        self.saveResponseAsPdf(response) # Creates a pdf with the responses and saves it to pc
        # TODO: Send email to organization that member has submitted!
        # TODO: Send confirmation email to member that their response was recieved



    # Store the response as a pdf
    # enters the necessary directory, or creates it
    # then, calls generatePdf which implicitly then populates the pdf with our responses

    def saveResponseAsPdf(self, response):

        formID = response.formID
        form = self.getFormByID(formID)
        formName = form.name
        
        try: 
            os.mkdir("responses") 
        except OSError as error: 
            pass # Directory exists

        try: 
            os.mkdir("responses/" + formName) 
        except OSError as error: 
            pass # Directory exists

        path = "responses/"+formName+"/"

        PdfGenerator.generatePdf(response, path)