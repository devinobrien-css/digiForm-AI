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
    def __init__(self, name, due, org, fields, formID):
        # Fields determined by server, replicated from pdfForm before sending this request obj to client
        # This object will be created based off of the associated pdfForm object and sent out upon a delivery request
        self.name = name
        self.due = due
        self.org = org
        self.fields = fields
        self.formID = formID
        self.complete = False

    # Display this request object: Mostly debug for now
    # NOTE: Eventually, will pull up page and populate with field entry instead.
    def display(self):
        
        print("\nForm Title: "+ self.name)
        print("Form Organizer: "+ self.org.name)
        print("Form Due Date: "+ self.due)
        print("-----------------------")
        for element in self.fields:
            print(element.name+" is a "+element.type+" with response: "+element.response)


class pdfResponse:
    def __init__(self, responder, completionDate, fields, formID, org):

        # Fields that server will fill in after reciept based on sending client
        self.completionDate = completionDate
        self.responder = responder
        self.fields = fields
        self.org = org
        self.formID = formID
    
class pdfForm:
    def __init__(self, name, formID, due, org, fields, path):

        # Fields determined by server (on creation)
        self.name = name
        self.due = due
        self.org = org
        self.fields = fields
        self.path = path

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
            print(element.name+" is a "+element.type+" with response: "+element.value)

# A readible struct. We create when a user updates a value for a field 
class pdfElement:
    def __init__(self, name, type, value, index, rect):
        self.name = name
        self.type = type
        self.value = value
        self.index = index
        self.rect = rect
        
        # Multiple choice properties
        self.singleChoice = False
        self.choiceGroup = "" # Example: 'Gender'
        self.choiceValue = "" # Example: 'Female' 
        # NOTE: self.name is the unformatted, human-defined data. Example: $Gender:Female
            # NOTE: $ denotes singleResponse, i.e. can only choose one gender at a time.
        
        # NOTE: self.value for multiple choice checkbox will be yes or no, denoting whether this value was selected.

        if (type == Consts.mcDisplay):

            # Determine the group and value for this option.
            args = self.name.split(":")

            self.choiceGroup = args[0]
            self.choiceValue = args[1]

            # Check if it is single choice only
            if (self.name.find("$") == 0):
                self.singleChoice = True
                self.choiceGroup = self.choiceGroup.removeprefix("$")
            



# A class of constants to configure global properties and behavior, mostly semantics.
class Consts:
    textFieldDisplay = "text"
    checkBoxDisplay = "checkbox"
    mcDisplay = "mc"

    checkBoxDisplayYes = "Yes"
    checkBoxDisplayNo = "No"
    checkBoxNoState = "/Off"
    checkBoxYesState = "/0"

    # DO NOT EDIT (unless you're really, really smart)
    textTypeID = "/Tx"
    checkTypeID = "/Btn"
    dropTypeID = "/Ch" # /DV is default vals, /Opt is list of options.

    nameFields = ["name", "Name"]
    firstNameFields = ["firstName", "first", "First", "First Name", "FirstName", "first name", "First name", "Firstname"]
    lastNameFields = ["lastName", "first", "Last", "Last Name", "LastName", "first name", "Last name", "Lastname"]