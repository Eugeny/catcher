Catcher - Beautiful tracebacks
==============================

**python-catcher** module generates rich HTML tracebacks (including source code and locals), submits it to the web and generates a permalink.

Quick use::

    import catcher

    try:
        launch_important_stuff()
    except Exception, e:
        report = catcher.collect(e)
        html = catcher.formatters.HTMLFormatter().format(report, maxdepth=4)
        url = catcher.uploaders.AjentiOrgUploader().upload(html)

        print 'Application has crashed. Please submit this link along with the bug report:'
        print url


Example report: http://ajenti.org/catcher/view/10

Report overview:

.. image:: http://habrastorage.org/storage2/f05/ea4/779/f05ea4779fccf0087fa24a380bd92b45.png

One stack frame with locals:

.. image:: http://habrastorage.org/storage2/4b8/188/5fe/4b81885fe8582d835c557af1d71884b9.png

