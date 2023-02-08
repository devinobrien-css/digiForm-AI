# This is a Form object. It will store data such as:
    # Form name
    # Organization 
    # Due date
    # Fields

# Construct Form object with the given name, fields, due date and organization. 

    # CONSTRUCTED WHEN: Web server uploads a pdf to the server from their local machine.

        # Just prior to instantiation, the file will be scanned to obtain the "fields" data (Name, Type).
        # The remaining three attributes are created by the Organization on the web app (name, due, org).
        # All four will then be passed to this new object, which is sent over to the client
        
        # From there, the client will fill in each field.response, either by scan or manual entry.
        # This pdf object will then be updated with the field response values as well as client data upon submission.

class pdfRequest:
    def __init__(self, name, due, org, fields):
        # Fields determined by server, replicated from pdfForm before sending this request obj to client
        # This object will be created based off of the associated pdfForm object and sent out upon a delivery request
        self.name = name
        self.due = due
        self.org = org
        self.fields = fields


class pdfResponse:
    def __init__(self, responderID, completionDate, fields):

        # Fields that server will fill in after reciept based on sending client
        self.completionDate = "NA"
        self.responderID = -1
        self.fields = fields
    
class pdfForm:
    def __init__(self, name, formID, due, org, fields):

        # Fields determined by server (on creation)
        self.name = name
        self.due = due
        self.org = org
        self.fields = fields

        # No responses by default, of course
        # The FormID is used to connect responses to the correct form.
        self.responses = []
        self.formID = formID

    def display(self):
        
        print("\nForm Title: "+ self.name)
        print("Form Organizer: "+ self.org.name)
        print("Form Due Date: "+ self.due)
        print("-----------------------")
        for element in self.fields:
            print(element.name+" is a "+element.type+" with response: "+element.response)

class pdfElement:
    name = ""
    type = ""
    response = ""

# A class of constants to configure global properties and behavior, mostly semantics.
class Consts:
    textFieldDisplay = "text"
    checkBoxDisplay = "checkbox"
    checkBoxDisplayYes = "Yes"
    checkBoxDisplayNo = "No"
    checkBoxNoState = "/Off"

    # DO NOT EDIT (unless you're really, really smart)
    textTypeID = "/Tx"
    checkTypeID = "/Btn"
    dropTypeID = "/Ch" # /DV is default vals, /Opt is list of options.