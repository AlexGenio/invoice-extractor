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

        self.__regex_client  = re.compile(r'\b(^[A-ZÀÂÇÉÈÊËÎÏÔÛÙÜŸÑÆŒa-zàâçéèêëîïôûùüÿñæœ\s-]+)\b')
        self.__regex_phone   = re.compile(r'\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4}')
        self.__regex_address = re.compile(r'\b(^\d+.*?\s+.+$)\b')
        self.__regex_email   = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.__doc_count     = 0
        self.__filenames     = []
        self.__clients       = []
        self.__phone_numbers = []
        self.__addresses     = []
        self.__emails        = []


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

                    # parse the PDF
                    pdf  = fitz.open(filepath)
                    page = pdf[0]
                    text = page.get_text()

                    if not text:
                        OUTPUT_LOGGER.log( logging.WARNING, "The PDF is empty.")
                        continue
                    
                    client = ""
                    email  = ""
                    address = []
                    phone_numbers = []

                    process_sold = False
                    process_deliver = False
                    process_address = False
                    lines_to_skip = 0

                    lines  = text.split('\n')

                    # go through parsed PDF line per line
                    for line in lines:
                        line = line.strip()

                        # extract phone numbers, address, and email from "Sold To" section
                        if "Sold To" in line or "Vendu à" in line:
                            lines_to_skip = 1
                            process_sold = True
                            process_deliver = False
                            continue

                        if process_sold:

                            result = self.__regex_phone.findall( line)
                            for phone in result:
                                if phone not in phone_numbers:
                                    phone_numbers.append( phone)

                            # force skip the client (could look like an address)
                            if lines_to_skip > 0:
                                lines_to_skip -= 1
                                continue

                            if not email:
                                result = self.__regex_email.search( line)
                                if result:
                                    email = result.group().strip().lower()
                                else:
                                    # build address string (after client, before email)
                                    if process_address:
                                        address.append( line.lower().title())
                                    else:
                                        result = self.__regex_address.search( line)
                                        if result:
                                            address.append( result.group(1).strip().lower().title())
                                            process_address = True

                            if email:
                                process_sold = False
                                continue

                        # extract phone numbers, client name, and potentially address
                        # from "Deliver To" section
                        if "Deliver To" in line or "Livrer à" in line:
                            process_sold = False
                            process_deliver = True
                            continue

                        if process_deliver:

                            result = self.__regex_phone.findall( line)
                            for phone in result:
                                if phone not in phone_numbers:
                                    phone_numbers.append( phone)

                            if not client:
                                result = self.__regex_client.search( line)
                                if result:
                                    client = result.group(1).strip().lower().title()

                            if not address:
                                result = self.__regex_address.search( line)
                                if result:
                                    address.append( result.group(1).strip().lower().title())

                            if client and address:
                                process_deliver = False
                                continue

                        if client and address and email:
                            break

                    pdf.close()

                    valid_invoice = True

                    # support potential typos in client names
                    if not client:
                        OUTPUT_LOGGER.log( logging.WARNING, "Failed to extract client full name.")

                    if not phone_numbers:
                        OUTPUT_LOGGER.log( logging.WARNING, "Failed to extract client phone number(s).")

                    if not address:
                        OUTPUT_LOGGER.log( logging.WARNING, "Failed to extract client address.")

                    if not email:
                        OUTPUT_LOGGER.log( logging.WARNING, "Failed to extract client email.")
                        valid_invoice = False

                    # invoice should be processed if email is unique
                    if valid_invoice:
                        if email in self.__emails:
                            OUTPUT_LOGGER.log( logging.WARNING, "Duplicate email found --- Client: {}, Email: {}".format(client, email))
                        else:
                            self.__filenames.append( filename)
                            self.__clients.append( client)
                            self.__addresses.append( address)
                            self.__emails.append( email)
                            self.__phone_numbers.append( phone_numbers)
                            print("Extracted data --- Client: {}, Email: {}".format(client, email))
                    print("")
     
    def printFooter(self):
        print("")
        print("*** {} PDF files found ***".format(self.__doc_count))

        if self.__doc_count != len( self.__filenames):
            OUTPUT_LOGGER.log( logging.WARNING, "*** {} PDF files extracted unsuccessfully ***".format(self.__doc_count - len(self.__filenames)))

        print("*** {} PDF files extracted successfully ***".format(len(self.__filenames)))
        print("*** {} client full names extracted ***".format(len(self.__clients)))
        print("*** {} client phone numbers extracted ***".format(len(self.__phone_numbers)))
        print("*** {} client addresses extracted ***".format(len(self.__addresses)))
        print("*** {} client emails extracted ***".format(len( self.__emails)))
        print("")

    def postProcessResults(self):
        if self.__filenames:
            workbook = Workbook()
            worksheet = workbook.active
            worksheet.title = "Invoice Extraction"
            headers = ["File", "First Name", "Last Name", "Phone Number(s)", "Address", "Email"]
            worksheet.append( headers)

            # populate excel worksheet with parsed PDF data
            for idx in range(len(self.__filenames)):
                firstname = ""
                lastname  = ""
                if self.__clients[ idx]:
                    firstname, *lastname = self.__clients[ idx].split()
                    lastname             = " ".join(lastname)
                phone_numbers        = ", ".join(self.__phone_numbers[ idx])
                address              = ", ".join(self.__addresses[ idx])
                worksheet.append( [self.__filenames[ idx],
                                  firstname,
                                  lastname,
                                  phone_numbers,
                                  address,
                                  self.__emails[ idx]])

            # automatically adjust column width
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
                adjusted_width = max_length * 1.05
                worksheet.column_dimensions[column].width = adjusted_width

            workbook.save(self._output_file)

            print("*** Output of extraction: {} ***".format(self._output_file))
            print("")

            # open the excel sheet
            os.startfile(self._output_file)