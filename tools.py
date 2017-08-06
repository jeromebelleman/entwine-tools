import os
import subprocess
import datetime
import socket
import entwinelib

DATEFMT = '%d %b %Y'

def photos(outdir, start=0, stop=None, size=64, details=False):
    '''
    Write photo gallery
    '''

    # Create thumbnails directory
    try:
        os.mkdir(outdir + '/thumbnails')
    except OSError:
        pass

    # Make entries
    def mkentry(filename, details):
        '''
        Make an entry for a photo
        '''

        outfile = outdir + '/thumbnails/' + filename
        try:
            if entwinelib.getmtime(filename) > entwinelib.getmtime(outfile):
                raise OSError
        except OSError:
            subprocess.call(['gm', 'convert', '-resize', 'x' + str(size),
                             filename, outfile])
        if details:
            mtime = \
                datetime.datetime.fromtimestamp(entwinelib.getmtime(filename))
            proc = subprocess.Popen(['identify', filename],
                                    stdout=subprocess.PIPE)
            filetype, _ = proc.communicate()
            filetype = filetype.strip().replace(' ', '<br />', 1)

            row = '<tr><td>[![%s](thumbnails/%s)](%s)</td>'
            row += '<td>%s<br />%s</td></tr>'
            print row % ((filename,) * 3 + \
                (filetype, mtime.strftime(DATEFMT)))
        else:
            print '[![%s](thumbnails/%s)](%s)' % ((filename,) * 3)

    filenames = sorted([entry for entry in os.listdir('.')
                        if entry.lower().endswith('.jpg') or
                        entry.lower().endswith('.png')])

    if details:
        print '<table>'
    else:
        print '<div class="photos">'

    for filename in filenames[start:stop]:
        mkentry(filename, details)

    if details:
        print '</table>'
    else:
        print '</div>'

def include(path):
    '''
    Include file contents
    '''

    with open(path) as fhl:
        print fhl.read()

def indexposts():
    '''
    Print index of posts
    '''

    for doc in os.listdir('.'):
        if os.path.isdir(doc):
            meta, _ = entwinelib.loadmd(doc + '/index.md')
            print '<div>'
            print '<a href="%s">%s</a><br>' % (doc, meta['title'])
            print '<span class="date">%s</span><br>' % \
              meta['date'].strftime('%-d %b %Y')
            print meta['description']
            print '</div>'

def ganalytics(dev, trackingid):
    '''
    Insert Google Analytics
    '''

    if socket.gethostname() != dev:
        print '''\
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', '%s', 'auto');
  ga('send', 'pageview');
  </script>''' % trackingid
