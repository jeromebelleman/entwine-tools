import os
import subprocess

def photos(params, start=0, stop=None, size=64):
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
    def mkentry(entry):
        path = 'thumbnails/' + entry
        try:
            if os.stat(entry).st_mtime > os.stat(path).st_mtime:
                raise OSError
        except OSError:
            subprocess.call(['gm', 'convert', '-resize', 'x' + str(size),
                             entry, path])
        print '[![%s](thumbnails/%s)](%s)' % ((entry,) * 3)

    entries = [entry for entry in os.listdir('.')
               if entry.lower().endswith('.jpg') or
               entry.lower().endswith('.png')]
    for entry in entries[start:stop]:
        mkentry(entry)

