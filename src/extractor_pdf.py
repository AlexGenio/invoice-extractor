import os
import re
import logging
import fitz

from openpyxl import Workbook
from openpyxl.styles import Font
from extractor import Extractor, OUTPUT_LOGGER

class ExtractorPDF(Extractor,object):

    def __init__(self, root_dir, output_dir):
        Extractor.__init__(self,
                            __name__,
                            root_dir,
                            output_dir)

        self.__regex_client = re.compile(r'\b(^[A-ZÀÂÇÉÈÊËÎÏÔÛÙÜŸÑÆŒa-zàâçéèêëîïôûùüÿñæœ\s-]+)(\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4})?\b')
        self.__regex_email  = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.__doc_count    = 0
        self.__filenames    = []
        self.__clients      = []
        self.__emails       = []


    def printHeader(self):
        print("*******************************************************")
        print("*                                                     *")
        print("*               EXTRACTING FROM PDF                   *")
        print("*                                                     *")
        print("*******************************************************\n")
        print("***  Extracting data from PDF files in '{}' ***".format(self._root_dir))
        print("")

    def doExtraction(self):

        # loop through current dir and all subdirs
        for dirpath, dirnames, files in os.walk(self._root_dir):
            # look through all files in current directory
            for filename in [f for f in files if f.endswith(".pdf")]:
               
                filepath = os.path.join(dirpath, filename)

                if filepath.endswith(".pdf"):

                    print("Processing file: {}".format(filename))
                    self.__doc_count += 1

                    pdf  = fitz.open(filepath)
                    page = pdf[0]
                    text = page.get_text()

                    if not text:
                        OUTPUT_LOGGER.log( logging.WARNING, "The PDF is empty.")
                        continue
                    
                    client = ""
                    email  = ""
                    client_next_line = False

                    lines  = text.split('\n')

                    for line in lines:
                        line = line.strip()

                        if not client:
                            if "Sold To" in line or "Vendu à" in line or "Deliver To" in line or "Livrer à" in line:
                                client_next_line = True
                                continue

                            if client_next_line:
                                result = self.__regex_client.search(line)
                                if result:
                                    client = result.group(1).strip().lower().title()
                                client_next_line = False
                                continue

                        if not email:
                            result = self.__regex_email.search(line)
                            if result:
                                email = result.group().strip().lower()

                        if client and email:
                            break

                    pdf.close()

                    valid_invoice = True

                    # support potential typos in client names
                    if not client:
                        OUTPUT_LOGGER.log( logging.WARNING, "Failed to extract client full name.")

                    if not email:
                        OUTPUT_LOGGER.log( logging.WARNING, "Failed to extract client email.")
                        valid_invoice = False

                    if valid_invoice:
                        if email in self.__emails:
                            OUTPUT_LOGGER.log( logging.WARNING, "Duplicate email found --- Client: {}, Email: {}".format(client, email))
                        else:
                            self.__filenames.append( filename)
                            self.__clients.append( client)
                            self.__emails.append( email)
                            print("Extracted data --- Client: {}, Email: {}".format(client, email))
                    print("")
     
    def printFooter(self):
        print("")
        print("*** {} PDF files found ***".format(self.__doc_count))

        if self.__doc_count != len( self.__filenames):
            OUTPUT_LOGGER.log( logging.WARNING, "*** {} PDF files extracted unsuccessfully ***".format(self.__doc_count - len(self.__filenames)))

        print("*** {} PDF files extracted successfully ***".format(len(self.__filenames)))
        print("*** {} client full names extracted ***".format(len(self.__clients)))
        print("*** {} client emails extracted ***".format(len( self.__emails)))
        print("")

    def postProcessResults(self):
        if self.__filenames:
            workbook = Workbook()
            worksheet = workbook.active
            worksheet.title = "Invoice Extraction"
            headers = ["File", "First Name", "Last Name", "Email"]
            worksheet.append( headers)

            for idx in range(len(self.__filenames)):
                firstname, *lastname = self.__clients[ idx].split()
                lastname = " ".join(lastname)
                worksheet.append( [self.__filenames[ idx], firstname, lastname, self.__emails[ idx]])

            for col in worksheet.columns:
                max_length = 0
                col[0].font = Font(bold=True, underline="single")
                column = col[0].column_letter # Get the column name
                for cell in col:
                    try: # Necessary to avoid error on empty cells
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2) * 1.2
                worksheet.column_dimensions[column].width = adjusted_width

            workbook.save(self._output_file)

            print("*** Output of extraction: {} ***".format(self._output_file))
            print("")

            # open the excel sheet
            os.startfile(self._output_file)