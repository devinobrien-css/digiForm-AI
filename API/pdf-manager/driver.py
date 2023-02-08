from digiFormClasses import Organization

# Sample Driver code 
myOrg = Organization("ABC Construction")
myForm = myOrg.generateNewForm("form.pdf", "Sample Form", "01/01/01")
myForm.display()