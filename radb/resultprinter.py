import io
from typing import override

class ResultPrinter():

    @classmethod
    def create(cls, outputformat):
        if outputformat == 'radb':
            return RADBResultPrinter()
        if outputformat == 'markdown':
            return MarkdownResultPrinter()
        if outputformat == 'org':
            return OrgResultPrinter()
        raise Exception(f"no result printer for {outputformat} exists!")

    @classmethod
    def getcolsizes(cls, r, attrs):
        colsizes = [0] * len(r[0])
        for i, v in enumerate(attrs):
            colsizes[i] = max(colsizes[i], len(v))
        for row in r:
            for i, v in enumerate(row):
                colsizes[i] = max(colsizes[i], len(v))
        return colsizes

    @classmethod
    def result_as_list(cls, r):
        return [ x for x in r ]

    def print(self, r, attrs):
        pass



class RADBResultPrinter(ResultPrinter):

    @override
    def print(self,r,attrs):
        r = ResultPrinter.result_as_list(r)
        colsizes = ResultPrinter.getcolsizes(r, attrs)
        totallen = sum(colsizes) + (len(colsizes) - 1) * 2
        output = io.StringIO()
        output.write('-'*totallen + '\n')
        output.write(', '.join(str(val).ljust(colsizes[i]) for i,val in enumerate(attrs)) + '\n')
        output.write('-'*totallen + '\n')
        count = 0
        for row in r:
            output.write(', '.join(str(val).ljust(colsizes[i]) for i,val in enumerate(row)) + '\n')
            count += 1
        output.write('-'*totallen)
        output.write('\n{} tuple{} returned'.format('no' if count == 0 else count,
                                               '' if count == 1 else 's'))
        return output.getvalue()



class MarkdownResultPrinter(ResultPrinter):

    def formatonerow(self,row,colsizes):
        return '| ' + ' | '.join(str(val).ljust(colsizes[i]) for i,val in enumerate(row)) + ' |\n'

    def headersep(self,colsizes):
        return '|-' + '-|-'.join("".ljust(size, '-') for i,size in enumerate(colsizes)) + '-|\n'

    @override
    def print(self,r, attrs):
        r = ResultPrinter.result_as_list(r)
        colsizes = ResultPrinter.getcolsizes(r, attrs)
        output = io.StringIO()
        # write header
        output.write(self.formatonerow(attrs, colsizes))
        output.write(self.headersep(colsizes))
        count = 0
        for row in r:
            output.write(self.formatonerow(row, colsizes))
            count += 1
        return output.getvalue()

class OrgResultPrinter(ResultPrinter):

    def formatonerow(self,row,colsizes):
        return '| ' + ' | '.join(str(val).ljust(colsizes[i]) for i,val in enumerate(row)) + ' |\n'

    def headersep(self,colsizes):
        return '|-' + '-+-'.join("".ljust(size, '-') for i,size in enumerate(colsizes)) + '-|\n'

    @override
    def print(self,r,attrs):
        r = ResultPrinter.result_as_list(r)
        colsizes = ResultPrinter.getcolsizes(r,attrs)
        output = io.StringIO()
        # write header
        output.write(self.formatonerow(attrs, colsizes))
        output.write(self.headersep(colsizes))
        count = 0
        for row in r:
            output.write(self.formatonerow(row, colsizes))
            count += 1
        return output.getvalue()
