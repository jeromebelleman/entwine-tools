import os
import subprocess
import datetime
import entwine

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
            if entwine.getmtime(filename) > entwine.getmtime(outfile):
                raise OSError
        except OSError:
            subprocess.call(['gm', 'convert', '-resize', 'x' + str(size),
                             filename, outfile])
        if details:
            mtime = datetime.datetime.fromtimestamp(entwine.getmtime(filename))
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

    for filename in filenames[start:stop]:
        mkentry(filename, details)

    if details:
        print '</table>'

