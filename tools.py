import os
import subprocess

def photos(params):
    params['styles'] = '''
       img {
           border: thin solid;
           padding: 2px;
       }
    '''

    try:
        os.mkdir('thumbnails')
    except OSError:
        pass
    for entry in os.listdir('.'):
        if entry.lower().endswith('.jpg'):
            path = 'thumbnails/' + entry
            if os.stat(entry).st_mtime > os.stat(path).st_mtime:
                subprocess.call(['gm', 'convert', '-resize', 'x64',
                                 entry, path])
            print '[![%s](thumbnails/%s)](%s)' % ((entry,) * 3)

