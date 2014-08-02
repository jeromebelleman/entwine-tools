import os

def photos(params):
    params['styles'] = '''
       img {
           height: 64px;
           border: thin solid;
           padding: 2px;
       }
    '''

    for entry in os.listdir('.'):
        if entry.endswith('.jpg'):
            print '[![%s](%s)](%s)' % ((entry,) * 3)

