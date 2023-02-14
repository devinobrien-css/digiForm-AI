from pypdf import PdfReader, PdfWriter
from pdfrw import PdfReader as reader2, PdfWriter as writer2
from pdfStructure import pdfForm, pdfElement, Consts
from pypdf.generic import BooleanObject, NameObject, IndirectObject
import xlsxwriter


import shutil

# This is the first point of contact with the pdf from the Organization side once they upload
# We first must gather a list of all field names, their type, and location
# From there, we can send the data of the field names and type to the user side for the "Electronic Entry" mode.
   
    # Lifecycle of user electronically submitting pdf :
    # 1) Parse the BLANK pdf to gather a list of field names, and types (text or checkbox)
    # 2) Send this data to mobile users when we submit the form and display as a list where user can set values.
    # 3) When user submits responses electronically back to server, we interpret and WRITE responses to a duplicate of BLANK pdf


class PdfGenerator():

    # Generate excel from response
    def generateExcel(form):
        workbook = xlsxwriter.Workbook(form.name+".xlsx")
        worksheet = workbook.add_worksheet(form.name)
        visitedFields = [] # Used to keep track of radio groups so we only display once

        # First add the column headers
        col = 0
        
        for field in form.fields:
            # Was this field already visited? (Used not to dupicate radio field names)
            if field.name not in visitedFields:
                # Add this new field
                worksheet.write(0, col, field.name)
                visitedFields.append(field.name)
                col += 1
            else:
                pass # Here we can handle duplicate fields, likely MC buttons referencing same question

        # Next add the data values for each response
        row = 1
        for response in form.responses:
            
            # Each response has it's own row.
            row += 1
            col = 0
            radioIndex = 0 # used to specify which radio index was chosen
            for field in response.fields:
                if (field.type == Consts.checkBoxDisplay):

                    if (field.value == Consts.checkBoxYesState):
                        value = Consts.checkBoxDisplayYes
                    else:
                        value = Consts.checkBoxDisplayNo

                    worksheet.write(row, col, value) # Write the checkbox response in a readible fashion (yes/no)

                # MANAGE DISPLAY OF MULTIPLE CHOICE
                # TODO: for the one that is /0 ("Yes"), display its choice ("Male")
                # TODO: For the ones that are /Off (No) do row -= 1 and the continue to skip it.
                elif (field.type == Consts.mcDisplay):

                    if (field.value == Consts.checkBoxYesState):
                        value = "radio.option "+ str(radioIndex)
                        worksheet.write(row, col, value) # TODO: Write the MC response
                    else:
                        row -= 1
                        radioIndex += 1 #It was not the previous radio option!
                        continue

                # All other types just write its value! (text)
                else:
                    worksheet.write(row, col, field.value)

                col += 1
        worksheet.autofit()
        workbook.close()

        
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

                # If this is a checkbox or radio button, we must convert the "No" to "/Off", etc so pdf can understand.
                if (r.type == Consts.checkBoxDisplay or r.type == Consts.mcDisplay):
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

                        print(fieldData)
                        print("\n")

                        curFieldType = ""
                        curFieldValue = ""
                        curFieldIndex = fieldIndex
                        curFieldRect = fieldData["/Rect"]
                        try:
                            curFieldName = fieldData["/T"]
                        except: # Key error /T
                            continue # Skip this bad data type
                            #curFieldName = "Unsupported_"+str(fieldIndex)

                        try:
                            fieldTypeID = fieldData["/FT"]
                        except: # Unsupported field type (MC?)
                            # fieldTypeID = "UnsupportedType"
                            continue # Skip this bad data type

                        # Handle check box metadata
                        # Is it a check box or radio button
                        if (fieldTypeID == Consts.checkTypeID):
                            curFieldType = Consts.mcDisplay # Assume its MultipleChoice
                            try:
                                temp = fieldData["/BS"]
                            except: # This is a check box!
                                curFieldType = Consts.checkBoxDisplay
                            
                            try:
                                curFieldValue = fieldData["/V"]
                            except:
                                # Field is empty!
                                curFieldValue = ""


                            # Readable values to machine values
                            if (curFieldValue == Consts.checkBoxYesState):
                                curFieldValue = Consts.checkBoxDisplayYes
                            else:
                                curFieldValue = Consts.checkBoxDisplayNo

                        # Handle text box
                        elif (fieldTypeID == Consts.textTypeID):
                            curFieldType = Consts.textFieldDisplay
                            try:
                                curFieldValue = fieldData["/V"]
                            except:
                                # Field is empty!
                                curFieldValue = ""

                        # Append this field to our list
                        curField = pdfElement(curFieldName, curFieldType, curFieldValue, curFieldIndex, curFieldRect)
                        myFields.append(curField)
                        fieldIndex = fieldIndex + 1

        return pdfForm(title, formID, due, org, myFields, path)
