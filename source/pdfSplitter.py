from PyPDF2 import PdfFileWriter, PdfFileReader
import argparse
import os 
parser = argparse.ArgumentParser(
    description='Split PDF file into several PDFs. This version supports splitting into ranges', formatter_class=argparse.HelpFormatter)
parser.add_argument("-i", "--inputPDF",
                    help="input file [REQUIRED]", type=str,
                    required=True)
parser.add_argument("-o", "--outputDirectory",
                    help="output directory to move the output pdfs [REQUIRED]", type=str,
                    default='.', required=True)
parser.add_argument("-p", "--pageRange",
                    help="output pdfs in rages [OPTIONAL]", type=str,
                    default='all', required=False)
parser.add_argument("-v", "--verbose",
                    help="verbose output [OPTIONAL]", type=bool,
                    default=False, required=False)

args = vars(parser.parse_args())

filename = args['inputPDF']
outputDir = args['outputDirectory']
pageRange = args['pageRange']
verbose = args['verbose']
pageRanges = pageRange.split(',')

outputDir = os.path.abspath(outputDir)

if verbose:
    print '\n\nSplit PDF {} into {}'.format(filename, outputDir)

inputpdf = PdfFileReader(open(filename, "rb"))
numPages = inputpdf.getNumPages()

if verbose:
    print 'number of pages: {}'.format(numPages)

if 'all' in pageRange:
    pageRanges = [str(i) + '-' + str(i) for i in range(1, numPages+1)]

for i, pageRange in enumerate(pageRanges):
    rangeParts = pageRange.split('-')
    rangeStart = int(rangeParts[0])-1
    rangeEnd = int(rangeParts[1])
    output = PdfFileWriter()

    for page in range(rangeStart, rangeEnd):
        currentPage = inputpdf.getPage(page)
        currentPage.compressContentStreams()
        output.addPage(currentPage)
        if verbose:
            print '\nadding page {}'.format(page+1)
        outputPDFFilename = outputDir + os.sep + \
            'document-page {}.pdf'.format(i+1)
    with open(outputPDFFilename, 'wb') as outputStream:
        if verbose:
            print 'writing to file', outputPDFFilename + ':'
        output.write(outputStream)
