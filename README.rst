Catcher - Beautiful tracebacks
==============================

**python-catcher** module generates highly informative crash reports (including source code and locals) in two possible forms:

  * generates a text file report, which you can save it where it is needed to;
  * generates HTML-page-like report, submits it to the web and generates a permalink.

Quick use for HTML-page-like report::

    import catcher

    try:
        launch_important_stuff()
    except Exception as e:
        report = catcher.collect(e)
        html = catcher.formatters.HTMLFormatter().format(report, maxdepth=4)
        url = catcher.uploaders.AjentiOrgUploader().upload(html)

        print('Application has crashed. Please submit this link along with the bug report:')
        print(url)

Quick use for text file report::

    import catcher

    try:
        print('you cannot' / 'divide this')
    except Exception as e:
        report = catcher.collect(e)
        text = catcher.formatters.TextFormatter().format(report)
        with open(f'crash_{report.timestamp}.txt', 'w') as f: f.write(text)


Example text file report::

    Error report
    ~~~~~~~~~~~~
    Report generated using python-catcher
    
    Exception has been ocurred at 2021-01-12 20:09:53 and indices the following:
    ‖   TypeError: unsupported operand type(s) for /: 'str' and 'str'
    
    Traceback:
    ‖   @ mytest.py, line 6 (frame #0):
    ‖   |    import catcher
    ‖   |    
    ‖   |    try:
    ‖   |        print('you cannot' / 'divide this')
    ‖   |    except Exception as e:
    ‖   |        report = catcher.collect(e)
    ‖   |>>>     text = catcher.formatters.TextFormatter().format(report)
    ‖   |        with open(f'crash_{report.timestamp}.txt', 'w', encoding = 'utf-8') as f: f.write(text)
    ‖
    
    
    Locals:
    ‖   Frames 0 don`t have locals
    ‖   
        


Report overview:

.. image:: http://habrastorage.org/storage2/f05/ea4/779/f05ea4779fccf0087fa24a380bd92b45.png

One stack frame with locals:

.. image:: http://habrastorage.org/storage2/4b8/188/5fe/4b81885fe8582d835c557af1d71884b9.png

