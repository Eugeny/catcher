from datetime import datetime


class TextFormatter:
    def __format_frame(self, frame):
        lines, current_line = frame.code
        code = ''.join(
            '    ' +
            ('>>' if lines.index(line) == frame.line - current_line else '  ') +
            ' ' + line
            for line in lines
        )

        return """
    %(file)s:%(line)s
%(code)s
        """ % {
            'file': frame.file,
            'line': frame.line,
            'code': code,
        }

    def format(self, report):
        traceback = '\n'.join(self.__format_frame(frame) for frame in report.traceback)
        return """
Error report at %(timestamp)s

Traceback:
%(traceback)s
        """ % {
            'timestamp': datetime.fromtimestamp(int(report.timestamp)),
            'traceback': traceback,
        }
