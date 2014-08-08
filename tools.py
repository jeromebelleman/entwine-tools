import os
import subprocess

def photos(params, start=0, stop=None, size=64, details=False):
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
        path = 'thumbnails/' + entry
        try:
            if os.stat(entry).st_mtime > os.stat(path).st_mtime:
                raise OSError
        except OSError:
            subprocess.call(['gm', 'convert', '-resize', 'x' + str(size),
                             entry, path])
        if details:
            filesize = os.stat(entry).st_size / 1024
            proc = subprocess.Popen(['file', entry], stdout=subprocess.PIPE)
            filetype, _ = proc.communicate()
            row = '<tr><td>[![%s](thumbnails/%s)](%s)</td>'
            row += '<td>%s, %s kB</td></tr>'
            print row % ((entry,) * 3 + (filetype.strip(), filesize))
        else:
            print '[![%s](thumbnails/%s)](%s)' % ((entry,) * 3)

    entries = [entry for entry in os.listdir('.')
               if entry.lower().endswith('.jpg') or
               entry.lower().endswith('.png')]

    if details:
        print '<table>'

    for entry in entries[start:stop]:
        mkentry(entry, details)

    if details:
        print '</table>'

