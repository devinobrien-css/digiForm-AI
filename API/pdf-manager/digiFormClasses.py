from pdfManager import PdfGenerator, PdfReader
from pdfStructure import *
import os, time, shutil

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
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName
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

        # mark complete 
        self.currentForm.complete = True
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

    # TODO: When responding to radio button, set all others to no.
    def respondToField(self, fieldIndex, fieldValue):
        response = self.getFieldByIndex(fieldIndex)

        # NOTE: This will always be true, because we add all fields by default!
        if (response != None):
           
            # Field says firstname, so store the first name
            if response.name in Consts.firstNameFields:
                response.value = fieldValue.capitalize()

            # Field says name so its probably first and last
            elif response.name in Consts.nameFields:
                splitName = fieldValue.split(" ")
                
                # Store first and maybe last name
                firstName = splitName[0].capitalize()
                if len(splitName) == 2:
                    lastName = splitName[1].capitalize()
                    response.value = firstName+" "+lastName
                else: # Only have first name
                    response.value = firstName

                # We are given last name so store last name
            elif response.name in Consts.lastNameFields:
                response.value = fieldValue.capitalize()
            
            else: # Any non-name field need not be capitalized
                response.value = fieldValue


            # print("UPDATED VALUE FOR "+self.name+" TO "+ fieldValue)
        

        # Check if its a radio button (checkbox w $ prefix to denote single choice)
        if ((response.type == Consts.mcDisplay) and (response.singleChoice == True)):
            
            # It is! Set them all to no, then this one to yes, if we're choosing yes
            if (response.value == Consts.checkBoxDisplayYes or response.value == Consts.checkBoxYesState):
                
                # We said yes to this, so first say no to all others.
                for field in self.currentForm.fields:

                    # Is this field in the group we're targetting?
                    if (field.choiceGroup == response.choiceGroup):
                        field.value = Consts.checkBoxDisplayNo
                # All have been set to no, so set the desired to yes
                response.value = fieldValue


    # Return field with this index (NOT "at this index", not necessarily ordered by index, but probably is.)
    def getFieldByIndex(self, index):
        
        fields = self.currentForm.fields
        for field in fields:
            if (field.index == index):
                return field
        print("ERROR")
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
        self.currentForm = None

    # NOTE: This should probably add a Member object. at a minimum, it needs to take more info
    # so that we can properly manage and reference the member
    def addMember(self, member):
        self.members.append(member)
        return member


    # Return form object by ID
    def getFormByID(self, id):
        return self.forms[id]

    # Set the currnt form by ID. ID is same as child index in UI when listing all forms.
    # Current form is used when we want to "Add Existing Responses" we know which form its referred to.
    def setCurrentForm(self, id):
        self.currentForm = self.forms[id]

    # Organization wants to create a new form using the button. 
    # It must be given a new formID, the number of created forms.
    # returns the form object
    def generateNewForm(self, path, title, due):

        formID = len(self.forms)
        newForm = PdfGenerator.generateForm(path, title, formID, due, self)
        self.forms.append(newForm)
        self.currentForm = newForm
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
                newField = pdfElement(field.name, field.type, field.value, field.index, field.rect)
                fields.append(newField)

            newReq = pdfRequest(form.name, form.due, self, fields, form.formID)
            targets.receiveFormRequest(newReq)
            return

        for target in targets:
            # Create the request and call recieve in member
            fields = []
            for field in form.fields[:]:
                newField = pdfElement(field.name, field.type, field.value, field.index, field.rect)
                fields.append(newField)
                
            newReq = pdfRequest(form.name, form.due, self, fields, form.formID)
            target.receiveFormRequest(newReq)

    # We have recieved a member's response! Append it and refresh our view list.
    # We must store this updated list to save the responses on the server
    def receiveFormResponse(self, response):
        self.responses.append(response) # Cool, but we want to rather store this in the form's response list, not orgs
        id = response.formID
        form = self.forms[id]
        form.responses.append(response)

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


    # I uploaded a form on behalf of members. 
    # Turn each pdf into a form object
    # We have a reference to the current form, where we can gather most fields.

    def addExisitngResponses(self):
        for file in os.listdir("input"):
            matches = [] # Each file will have a new member list, found below:
            member = None
            firstName = ""
            lastName = ""

            if file.endswith(".pdf"):
                path = os.path.join("input", file)
                # First we must convert to a response object
                # I will first gather the fields by converting to form object
                complete = PdfGenerator.generateForm(path, self.currentForm.name, self.currentForm.formID, self.currentForm.due, self.currentForm.org)
                # I will now use complete.fields to gather the person who responded.

                
                
                for field in complete.fields:
                    # Field says firstname, so store the first name
                    if field.name in Consts.firstNameFields:
                        firstName = field.value.capitalize()

                    # Field says name so its probably first and last
                    if field.name in Consts.nameFields:
                        splitName = field.value.split(" ")
                        
                        # Store first and maybe last name
                        firstName = splitName[0].capitalize()
                        if len(splitName) == 2:
                            lastName = splitName[1].capitalize()

                     # We are given last name so store last name
                    if field.name in Consts.lastNameFields:
                        lastName = field.value.capitalize()

                    """ We have all possible info about the name, now try to find the member(s) matching the criteria """
                    if lastName:
                        # We have a last name so find all members with the last name AND first because we will always have first
                        for m in self.members:
                            if (m.lastName == lastName):
                                # Now check first name
                                if (m.firstName == firstName):
                                    matches.append(m)
                        # Here our matches must have at least one because we had a last name given.
                        # If we don't have any matches, it may be because last name not stored in system.
                        """ Widen search to just look for first names since we found none with last name"""
                        if len(matches) == 0:
                            for m in self.members:
                                if (m.firstName == firstName):
                                    matches.append(m)

                    # Try just searching first names if we got no matches
                    else: # We only have first name data
                        for m in self.members:
                            if (m.firstName == firstName):
                                matches.append(m)

                    """ We're ready to parse results. If one is found, perfect! it is our member. """
                    if len(matches) == 1:
                        member = matches[0]
                    
                    """ We're finished gathering results. If multiple, show UI to select or create new. """
                    if len(matches) == 0: # No matches found! Must select from all, or add new!
                        print(firstName + " "+ lastName +" was not a member so we have added them. This should prompt org, not just do it by auto!")
                        member = Member(firstName, lastName)
                        self.members.append(member)

                    # If we have multiple members with this name, present UI to choose which one
                    elif (len(matches) > 1):
                        #TODO: UI will determine which member (auto - detect halts)
                        # When response comes, we continue
                        # NOTE: at this point, member is set to the first occurance of the member that we found w this name
                        print("Multiple members found with name "+firstName+" "+lastName+"! Add UI to prompt which one in digiFormClasses.addExistingResponse().")
                    # Here we successfully have set the value of member (after UI prompt)


                    break # We already found the member so no need to keep looking


                if (member == None):
                    # We failed to set the member because we could not find the name!
                    # TODO: Present UI with option to select member from list where we can search for a member,
                    # OR we have option to add a new member as a button at the bottom of the widget.
                    print("No field 'name' found! Add UI to prompt member selection / addition in digiFormClasses.addExistingResponse().")
                    return # FOR NOW WE FAIL TO ADD THIS FORM UNTIL WE LEARN HOW TO CHOOSE MEMBER FROM UI AS ABOVE
                # Member is found!
                        
                # Gather time of last modification
                ti_m = os.path.getmtime(path)
                m_ti = time.ctime(ti_m)

                # Create and add the complete response to the array of responses
                response = pdfResponse(member, m_ti, complete.fields, self.currentForm.formID, self.currentForm.org)
                self.currentForm.responses.append(response) 

                # Add the form file to folder of complete PDF documents
                self.saveResponseAsPdf(response)
