from html_pdf import HtmlPdf
from html_txt import HtmlTxt
from pdf_html import PdfHtml
from txt_html import TxtHtml
from odt_html import OdtHtml
import re
import magic
import mimetypes

AVAILABLE_FORMATS = ['pdf', 'html', 'txt', 'odt']

AVAILABLE_CONVERTERS = [(HtmlPdf, 'htmlpdf'), (HtmlTxt, 'htmltxt'), (PdfHtml, 'pdfhtml'), (TxtHtml, 'txthtml'), (OdtHtml, 'odthtml')]

FORMAT_RE = [re.compile('.*%s'%fmt) for fmt in AVAILABLE_FORMATS]

def convert(input_file, output_format):
    """
    This is the main function that does the actual conversion.
    It takes as input the file to be converted and the required
    output format. If conversion is successful, it returns the 
    name of resultant file. Otherwise, it will return the name
    of original file.

    Example
    ========
    >>> from compound import convert
    >>>
    >>> convert('test.html', 'txt')
    'test.txt'

    Also See
    ========
    _class_selector
    general.GeneralConverter

    Open Problem
    ========
    The current organisation returns the name of the file and
    achieves conversion as a side-effect. I am afraid the side-effect
    thing may cause some bugs in future.
    """
    input_format = get_extension(input_file)
    converter = _class_selector(input_format, output_format)
    intermediate_file = input_file
    for converter, expression in converter:
        obj = converter()
        intermediate_file = obj.convert(intermediate_file)
    return intermediate_file

def _class_selector(input_format, output_format):
    """
    It takes as input input and output formats and returns the module
    or sequence of modules that will acheive the desired conversion.

    Example
    =======
    >>> from compound import _class_selector
    >>>
    >>> _class_selector('html', 'txt')
    [(<class html_txt.HtmlTxt at 0x10798e598>, 'htmltxt')]
    >>>
    >>> _class_selector('pdf', 'html')
    [(<class pdf_html.PdfHtml at 0x107e54050>, 'pdfhtml'),
    (<class html_txt.HtmlTxt at 0x10798e598>, 'htmltxt')]

    Note
    =======
    The second element of each returned list are expressions are
    required for regular expression matching.
    """
    input_format_re = re.compile('%s.*'%input_format)
    output_format_re =  re.compile('.*%s'%output_format)
    result = [(converter, expression) for converter, expression in AVAILABLE_CONVERTERS
              if input_format_re.match(expression) and output_format_re.match(expression)]
    if not result:
        result1 = [(converter, expression) for converter, expression in AVAILABLE_CONVERTERS
                   if input_format_re.match(expression)]
        result2 = [(converter, expression) for converter, expression in AVAILABLE_CONVERTERS
                   if output_format_re.match(expression)]
        for converter, expression in result1:
            result.append((converter, expression))
            input_format_c = expression[len(input_format):]
            input_format_c_re = re.compile('%s.*'%input_format_c)
            if not _class_selector(input_format_c, output_format):
                result = result[:-1]
            else:
                result.append(_class_selector(input_format_c, output_format)[0])
    return result
