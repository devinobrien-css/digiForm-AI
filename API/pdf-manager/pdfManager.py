from pypdf import PdfReader, PdfWriter
from pdfrw import PdfReader as reader2, PdfWriter as writer2
from pdfStructure import pdfForm, pdfElement, Consts
from pypdf.generic import BooleanObject, NameObject, IndirectObject


import shutil

# This is the first point of contact with the pdf from the Organization side once they upload
# We first must gather a list of all field names, their type, and location
# From there, we can send the data of the field names and type to the user side for the "Electronic Entry" mode.
   
    # Lifecycle of user electronically submitting pdf :
    # 1) Parse the BLANK pdf to gather a list of field names, and types (text or checkbox)
    # 2) Send this data to mobile users when we submit the form and display as a list where user can set values.
    # 3) When user submits responses electronically back to server, we interpret and WRITE responses to a duplicate of BLANK pdf


class PdfGenerator():

    # This function will take an existing form response object
    # that has been return with it's responses by a client and create a new blank forum, then fill it in.
    # NOTE: This means we must store 'blank' copy as an attribute in the form object, which will server 3 purposes
        # 1) If we implement client endpoint on the web server, they can view the blank copy there and fill it on a PC
        # 2) We can display a visual of the pdf to users on the app
        # 3) When the server recieves a response in object form, it can use the 'blank' to make the duplicate and fill in

    # Should take a form RESPONSE
    def generatePdf(response, formFolder): #formFolder passed as 'path'
        # Get the form that this response associates to
        # org = Server.getOrgByID(response.orgID)
        org = response.org
        sourceForm = org.getFormByID(response.formID)

        # Used to grab by ID: org.members[response.responderID]
        newFile = formFolder + response.responder.name +".pdf" # Name it responder.pdf
        # shutil.copy(sourceForm.path, newFile)

    # TODO: Now we must WRITE TO THE PDF the given fields.
        reader = PdfReader(sourceForm.path)
        if "/AcroForm" in reader.trailer["/Root"]:
            reader.trailer["/Root"]["/AcroForm"].update({NameObject("/NeedAppearances"): BooleanObject(True)})

        writer = PdfWriter()
        writer.append_pages_from_reader(reader)
        try:
            catalog = writer._root_object
            # get the AcroForm tree
            if "/AcroForm" not in catalog:
                writer._root_object.update({
                    NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)
                })

            need_appearances = NameObject("/NeedAppearances")
            writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
            # del writer._root_object["/AcroForm"]['NeedAppearances']

        except Exception as e:
            print('set_need_appearances_writer() catch : ', repr(e))

        if "/AcroForm" in writer._root_object:
            writer._root_object["/AcroForm"].update({NameObject("/NeedAppearances"): BooleanObject(True)})

        

        responses = response.fields

        # On each page
        for page in writer.pages:
            # For each response
            for r in responses[:]:

                if (r.type == Consts.checkBoxDisplay):
                    if (r.value == Consts.checkBoxDisplayYes):
                        r.value = Consts.checkBoxYesState
                    else:
                        r.value = Consts.checkBoxNoState
                writer.update_page_form_field_values( page, {r.name: r.value} )
                # print("WROTE "+r.value+" to "+ newFile)

        if "/AcroForm" in reader.trailer["/Root"]:
            writer._root_object.update({NameObject('/AcroForm'): reader.trailer["/Root"]["/AcroForm"]})

        # write "output" to pypdf-output.pdf
        with open(newFile, "wb") as output_stream:
            writer.write(output_stream)
        output_stream.close()
    
    
    # This function will generate a new form object. It can be thought of as "Starting an Event", and members of the organization
    # are per say "Invited to the event". In this case, that means being sent a "pdfRequest" object - a request to fill in
    # the fields. This form object will be referenced in the code for Organization, when sendRequest(form, client) is called.
    def generateForm(path, title, formID, due, org):

        reader = PdfReader(path)
        if "/AcroForm" in reader.trailer["/Root"]:
            reader.trailer["/Root"]["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)}
    )
        fields = reader.get_fields()
        
        myFields = []
        fieldIndex = 0

        for page in reader.pages:
            if "/Annots" in page:
                for annot in page["/Annots"]:
                    fieldData = annot.get_object()
                    if (fieldData["/Subtype"] == "/Widget"):

                        # print(fieldData)
                        # print("\n")

                        curFieldType = ""
                        curFieldValue = ""
                        curFieldIndex = fieldIndex
                        curFieldRect = fieldData["/Rect"]
                        curFieldName = fieldData["/T"]

                        # Handle check box metadata
                        if (fieldData["/FT"] == Consts.checkTypeID):
                            curFieldType = "checkbox"
                            if (fieldData["/V"] == Consts.checkBoxNoState):
                                curFieldValue = Consts.checkBoxDisplayNo
                            else:
                                curFieldValue = Consts.checkBoxDisplayYes

                        # Handle text box metadata
                        else:
                            if (fieldData["/FT"] == Consts.textTypeID):
                                curFieldType = Consts.textFieldDisplay
                                curFieldValue = fieldData["/V"]

                                # TODO: ^ Handle KeyError: "/V" here for empty forms values! ^

                        # Append this field to our list
                        curField = pdfElement(curFieldName, curFieldType, curFieldValue, curFieldIndex, curFieldRect)
                        myFields.append(curField)
                        fieldIndex = fieldIndex + 1

        return pdfForm(title, formID, due, org, myFields, path)
