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
            subprocess.call(['gm', 'convert', '-resize', 'x64', entry,
                             'thumbnails/' + entry])
            print '[![%s](thumbnails/%s)](%s)' % ((entry,) * 3)

