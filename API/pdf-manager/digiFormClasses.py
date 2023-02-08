from pdfManager import PdfGenerator

# Organization class
class Organization:

    # A new organization is formed
    # Begin with a name and an empty list of forms.
    def __init__(self, name):
        self.name = name
        self.forms = []


    # NOTE: Previously, you could send a pdf out many times, each independent. Now, and better, creating a form is like
    # starting an event. It will be uniform for all members, even if they are added later. You will create the form object
    # first and then any added members will be associated with it through here via FormID. No matter at what time a member 
    # gets a forum request, they will all be associated to the same FormID to keep all responses together.

    # Organization wants to create a new form using the button. 
    # It must be given a new formID, the number of created forms.
    # returns the form object
    def generateNewForm(self, path, title, due):

        formID = self.forms.count
        newForm = PdfGenerator.generateForm(path, title, formID, due, self)
        return newForm

    # TODO: Send a request of this form to this target. Can be a list, or singleton
    def sendFormRequest(form, targets):
        for target in targets:
            pass # define code here