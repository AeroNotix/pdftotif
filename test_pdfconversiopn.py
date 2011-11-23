
import os
import subprocess
from pyPdf import PdfFileWriter, PdfFileReader



class Conversion(object):

    def __init__(self, gscriptpath):
        self.gscriptpath = gscriptpath


    def pdf_to_tif(self, ifname, ofname):

        subprocess.Popen(' '.join([
                           self.gscriptpath + '\gswin32c.exe"',
                           '-q',
                           '-dNOPAUSE',
                           '-dBATCH',
                           '-r300x300',
                           '-sDEVICE=tiffpack',
                           '-dJPEGQ=50',
                           '-sPAPERSIZE=a4',
                           '-sOutputFile=%s %s' % (str(ofname), str(ifname)),
                           ]), shell=True)


PDFWrapper = Conversion(r'"C:\Program Files\gs\gs8.53\bin')

PDFWrapper.pdf_to_tif(r'"C:\Documents and Settings\francea\Desktop\IMG.pdf"',
                      r'"C:\Temp\123.jpg"')



inputPDFdir = r"C:\Documents and Settings\francea\Desktop"

inputpdf = PdfFileReader(open(inputPDFdir + r'\IMG.pdf', 'rb'))

for i in xrange(inputpdf.numPages):
 output = PdfFileWriter()
 output.addPage(inputpdf.getPage(i))
 outputStream = open(r"C:\Documents and Settings\francea\Desktop\outputdir\IMG%s.pdf" % i, "wb")
 output.write(outputStream)
 outputStream.close()


path = r'C:\Documents and Settings\francea\Desktop\outputdir'

dirList = os.listdir(path)

for i, fname in enumerate(dirList):

    PDFWrapper.pdf_to_tif('"' + path + '\\' + fname + '"',
                          '"' + path + '\\' + fname[:-4] + '.tiff' + '"')