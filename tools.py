import os
import subprocess
import datetime
import entwine

DATEFMT = '%d %b %Y'

def photos(params, start=0, stop=None, size=64, details=False):
    '''
    Write photo gallery
    '''

    params['styles'] = '''
       img {
           border: thin solid;
           padding: 2px;
       }
    '''

    # Create thumbnails directory
    try:
        os.mkdir('thumbnails')
    except OSError:
        pass

    # Make entries
    def mkentry(entry, details):
        '''
        Make an entry for a photo
        '''

        path = 'thumbnails/' + entry
        try:
            if entwine.getmtime(entry) > entwine.getmtime(path):
                raise OSError
        except OSError:
            subprocess.call(['gm', 'convert', '-resize', 'x' + str(size),
                             entry, path])
        if details:
            mtime = datetime.datetime.fromtimestamp(entwine.getmtime(entry))
            proc = subprocess.Popen(['identify', entry], stdout=subprocess.PIPE)
            filetype, _ = proc.communicate()
            filetype = filetype.strip().replace(' ', '<br />', 1)

            row = '<tr><td>[![%s](thumbnails/%s)](%s)</td>'
            row += '<td>%s<br />%s</td></tr>'
            print row % ((entry,) * 3 + \
                (filetype, mtime.strftime(DATEFMT)))
        else:
            print '[![%s](thumbnails/%s)](%s)' % ((entry,) * 3)

    entries = sorted([entry for entry in os.listdir('.')
                      if entry.lower().endswith('.jpg') or
                      entry.lower().endswith('.png')])

    if details:
        print '<table>'

    for entry in entries[start:stop]:
        mkentry(entry, details)

    if details:
        print '</table>'

