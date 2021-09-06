from extractor_pdf import ExtractorPDF

class ExtractorFactory(object):

    @staticmethod
    def createExtractor(filetype, root_dir="", output_file=""):

        if filetype.lower() == "pdf":
            return ExtractorPDF(root_dir, output_file)
        
        return None
            

    
