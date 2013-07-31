from mako.template import Template
from datetime import datetime


_template = Template("""<!doctype html>
<html>
    <head>
        <title>Error report</title>

        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
        <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0-rc1/js/bootstrap.min.js"></script>

        <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0-rc1/css/bootstrap.min.css" rel="stylesheet">
        <link href="http://netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.min.css" rel="stylesheet">
        <style>
            a {
                cursor: pointer;
            }

            .codebox {
                font-family: monospace;
            }

            .codebox .line.current {
                background: rgba(0,0,255,.1);
            }

            .codebox .lineno {
                text-align: right;
                display: inline-block;
                width: 100px;
                opacity: .5;
            }

            .codebox .code {
                white-space: pre;
            }

            .object-link {
                font-family: monospace;
                white-space: pre;
            }
        </style>
    </head>

    <%
        def id():
            id._last_id += 1
            return id._last_id

        id._last_id = 0

        def extract_attrs(object):
            r = {}
            for k in dir(object):
                if not k.startswith('__') and hasattr(object, k):
                    v = getattr(object, k)
                    if not type(v).__name__.endswith('method'):
                        r[k] = v
            return r
    %>

    <%def name="object(x, depth=0)" buffered="True">
        % if depth > maxdepth:
            <% return "[too deep]" %>
        % endif
        <% objid = id() %>
        % if type(x) in [str, int, long, float, set] or x in [None]:
            <code>${repr(x) | h}</code>
        % elif type(x) == dict:
            <table class="table">
                % for key, value in x.items():
                    <tr>
                        <td><code>${key | h}</code></td>
                        <td><span class="badge">${type(value).__name__ | h}</span></td>
                        <td width="100%">${object(value, depth + 1)}</td>
                    </tr>
                % endfor
            </table>
        % elif type(x) == list:
            <span class="badge">${len(x)} items</span>
            <table class="table">
                % for value in x:
                    <tr>
                        <td><span class="badge">${type(value).__name__ | h}</span></td>
                        <td>${object(value, depth + 1)}</td>
                    </tr>
                % endfor
            </table>
        % else:
            % if hasattr(x, '__dict__'):
                <a class="object-link" data-toggle="collapse" data-target="#${objid}-content">${repr(x) | h}</a>
                <div id="${objid}-content" class="collapse">
                    ${object(extract_attrs(x), depth + 1)}
                </div>
            % else:
                <code> ${repr(x) | h} </code>
            % endif
        % endif
    </%def>

    <body>
        <div class="container">
            <h3>Error report</h3>
            <dl>
                <dt>Timestamp</dt>
                <dd>${ datetime.fromtimestamp(report.timestamp) }</dd>
            </dl>

            <h3>Exception</h3>
            ${object(report.exception)}

            <h3>Traceback</h3>
            % for frame in report.traceback:
                <% frameid = id() %>
                <p>
                    <i class="icon-file"></i> <code>${ frame.file } : ${ frame.line }</code>


                    <div class="row">
                        <div class="col-lg-10">

                            <div class="codebox">
                                % for index, line in enumerate(frame.code[0]):
                                    <div class="line ${'current' if frame.code[1] + index == frame.line else ''}">
                                        <span class="lineno">
                                            ${ frame.code[1] + index }
                                        </span>
                                        <span class="code">${ line }</span>
                                    </div>
                                % endfor
                            </div>

                        </div>
                        <div class="col-lg-2">
                            <a class="btn btn-default" data-toggle="collapse" data-target="#${frameid}-locals">
                                <i class="icon-list-ul"></i> Locals
                            </a>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-lg-1">
                        </div>
                        <div>
                            <div id="${frameid}-locals" class="collapse">
                                <h4>Locals</h4>
                                ${object(frame.locals)}
                            </div>
                        </div>
                    </div>
                </p>
            % endfor
        </div>
    </body>
</html>
""")


class HTMLFormatter:
    def format(self, report, maxdepth=5):
        return _template.render(maxdepth=maxdepth, report=report, datetime=datetime)
