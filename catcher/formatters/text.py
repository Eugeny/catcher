from datetime import datetime


class TextFormatter:
    maxDepth = 5
    framesQty = 0
    framesWithoutLocals = []
    localsFormatted = False


    @staticmethod
    def isValidToRepresent(varname: str, object):
        if not (varname  in ('self', 'e')     or
                varname.startswith('__')      or
                'method' in varname           or
                'function' in varname         or
                'module' in str(type(object)) or
                'Report' in str(type(object))):
            return True


    @staticmethod
    def extractAttrs(object):
        result = {}
        for k in dir(object):
            if (hasattr(object, k)
                and not k.startswith('__')
                and not k.endswith('__')
                and not hasattr(k, 'hidden')
                and not type(getattr(object, k)).__name__.endswith('method')):
                    result[k] = getattr(object, k)

        return result


    def formatTracebackFrame(self, frame):
        if self.localsFormatted:
            self.framesQty += 1
            self.localsFormatted = False

        lines, current_line = frame.code
        code = '‖   |'
        code += '‖   |'.join((('>>> ' if lines.index(line) == frame.line - current_line else '    ') + line)
            for line in lines
        )

        return '''@ %(file)s, line %(line)s (frame #%(frameNo)s):
%(code)s‖
''' % {
            'file': frame.file,
            'line': frame.line,
            'frameNo': self.framesQty,
            'code': code,
        }


    def formatLocals(self, frame):
        i = int()
        localsText = f'@ frame #{self.framesQty}:\n'

        for varname, value in frame.locals.items():
            if self.isValidToRepresent(varname, value):
                if type(value) == dict:
                    localsText += f'''‖   |    {varname} ({type(value).__name__}):\n‖   |   |'''
                    for k, v in value.items():
                        if self.isValidToRepresent(k, v): localsText += f'''"{k}": {v}\n‖   |   |'''
                    localsText += '‖   |\n'
                    i += 1


                elif hasattr(value, '__dict__') and ('class' in str(type(value))):
                    localsText += f'''‖   |   {varname} (object of type {str(type(value))[7:-1]}):\n'''

                    d = self.extractAttrs(value)
                    for k, v in d.items(): 
                        localsText += f'''‖   |   |   attribute '{k}' ({type(v).__name__}): {v}\n'''
                    localsText += '‖   |\n'
                    i += 1


                else:
                    localsText += f'''‖   |   {varname} ({type(value).__name__}): {repr(value)}\n'''
                    i += 1


        self.localsFormatted = True
        if i: return localsText
        else: return ''


    def format(self, report):
        tracebackAsList, localsAsList = [], []
        emptyLocalsMessage = ''

        for frame in report.traceback:
            tracebackAsList.append(self.formatTracebackFrame(frame))

            localsForFrame = self.formatLocals(frame)
            if localsForFrame: localsAsList.append(localsForFrame)
            else: self.framesWithoutLocals.append(frame)

        if self.framesWithoutLocals:
            messagePart = ''
            for frameNo in range(len(self.framesWithoutLocals)):
                messagePart += f'{frameNo}, '
            messagePart = messagePart[:-2]
            emptyLocalsMessage = f'\n‖   Frames {messagePart} don`t have locals'

        return '''Error report
~~~~~~~~~~~~
Report generated using python-catcher

Exception has been ocurred at %(timestamp)s and indices the following:
‖   %(exceptionName)s: %(exceptionDesc)s

Traceback:
‖   %(traceback)s

Locals:%(emptyLocals)s
‖   %(locals)s
        ''' % {
            'timestamp': datetime.fromtimestamp(int(report.timestamp)),
            'traceback': '‖   '.join(tracebackAsList),
            'locals': '‖   '.join(localsAsList),
            'emptyLocals': emptyLocalsMessage,
            'exceptionName': type(report.exception).__name__,
            'exceptionDesc': str(report.exception)
        }
