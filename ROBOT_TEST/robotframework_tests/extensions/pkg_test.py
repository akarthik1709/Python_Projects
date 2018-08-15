#!/usr/bin/python
import os
import sys
import struct
import subprocess
import xml.etree.ElementTree
from hashlib import sha512

class pkgfile:
    def __init__(self,fname,hdrStart,hdrStop,dataStart,dataStop,checksumString):
        self.info = {'fname':fname, 'hdrStart':hdrStart, 'hdrStop':hdrStop,
                     'dataStart':dataStart, 'dataStop':dataStop, 'checksumString':checksumString}
    def adjustDataOffset( self, amount ):
        self.info['dataStart'] = self.info['dataStart'] + amount
        self.info['dataStop']  = self.info['dataStop'] + amount

class pkgtool:
    def __init__(self, data=None):
        self.pkg = None
        self.header = None
        if data:
            _ = self.getHeader( data )
    def createCSString(self,buffer):
        return struct.pack('H',(65535 - self.calcCS( buffer )))
    def calcCS(self,buffer,seed=0):
        lenth = len(buffer)
        sum = seed
        i=0
        while lenth > 1:
            j = i+2
            sum = sum + struct.unpack('H',buffer[i:j])[0]
            if sum > 0x0000FFFF: sum = (sum >> 16) + (sum & 0x0000FFFF)
            lenth = lenth -2
            i=j
        if lenth == 1:
            trailer = buffer[-1] + '\0'
            sum = sum + struct.unpack('H',trailer[0:2])[0]
        if sum > 0x0000FFFF: sum = (sum >> 16) + (sum & 0x0000FFFF)
        if sum > 0x0000FFFF: sum = (sum >> 16) + (sum & 0x0000FFFF)
        return sum
    def readHeaderFromFile(self,pkgName):
        pkg = open(pkgName,'r').read()
        return self.getHeader( pkg )
    def getHeader( self, pkg ):
        self.pkg=pkg[:]
        nfiles = ord(pkg[1])
        nfilecksumstr = pkg[2:4]
        header = []
        self.filemap = {}
        ptr = 4
        data_offset=0
        for i in range(nfiles):
            a = ptr
            b = a + 4
            one_file_data_len = struct.unpack('>I',pkg[a:b])[0]
            ptr = b + 4 + 4 + 4 # repeat length + 8 byte zero padding
            c = ptr
            d = c + 2
            ptr = d
            one_file_cksumstr = pkg[c:d]
            e = ptr
            f = ptr + 1
            ptr = f + 1 # 1 byte zero padding
            one_file_fname_len = struct.unpack('B',pkg[e:f])[0]
            g = ptr
            h = ptr + one_file_fname_len
            one_file_fname = pkg[g:h]
            ptr = h
            m = data_offset
            n = data_offset + one_file_data_len
            data_offset = n
            header.append( pkgfile( one_file_fname, a,h,m,n,one_file_cksumstr ) )
            self.filemap[one_file_fname] = i
        # update the data offsets
        for i in range(nfiles):
            header[i].adjustDataOffset( ptr )
        self.header = header[:]
        return len(header)
    def extractFile(self, file_num=-1):
        if file_num < 0:
            return ''
        a = self.header[file_num].info['dataStart']
        b = self.header[file_num].info['dataStop']
        return self.pkg[ a:b ]

class Carton:
    def __init__(self):
        self.carton = None
        self.userid = 10 ### admin user
        self.errors = []
    def psql(self,txt):
        cmd = ['psql','configuration','-Uroot','-Atc',txt]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pipeout, pipeerr = p.communicate()
        piperc = p.returncode
        if piperc is not 0:
            self.errors.append(pipeerr)
            return -1
        else:
            return pipeout
    def loadCarton(self, cartonName,tmpfile):
        self.tmpfile=tmpfile
        self.carton = pkgtool()
        filecount = self.carton.readHeaderFromFile( cartonName )
        self.cartonheader = self.carton.header[:]
        self.cartondata = self.carton.pkg[:]
        returnedid=None
        for pkg_idx in range(filecount):
            self.addPkgToDB( pkg_idx )
        totalerrors = len(self.errors)
        if totalerrors:
            for e in self.errors:
                print '   ',e
            print 'Loaded carton with %d errors out of %d pkgs'%(totalerrors,filecount)
        else:
            print 'Loaded carton with no errors, %d pkgs'%filecount
    def addPkgToDB(self, idx):
        savedname = self.carton.header[idx].info['fname']
        pkgbytes = self.carton.extractFile( idx )
        onepkg = pkgtool(pkgbytes)
        indexToSummary = onepkg.filemap['package_summary.xml']
        summary = onepkg.extractFile(indexToSummary)
        tree = xml.etree.ElementTree.fromstring( summary )
        open(self.tmpfile,'w').write(pkgbytes)
        chmodcmd = ('chmod 644 %s'%self.tmpfile).split()
        subprocess.call(chmodcmd)
        print '--> running add_config ',tree.find('creation_info').find('filename').text
        #
        # 616 = Package object type
        # 65  = Update Manager service
        #
        sqladd = """SELECT obj_id,kv->'pkg_blob_id' FROM 
            add_config({userid},(
            SELECT get_objecttypeid('Package')
            ),'{pkgname}',(
            SELECT obj_id FROM service s 
            JOIN object o USING(obj_id) 
            WHERE obj_name='Update Manager'
            ),'',
            hstore('filename','{pkgname}')     ||
            hstore('footprint','{pkgsize}')    ||
            hstore('hash','{hashstring}')      ||
            hstore('package_type','{content}') ||
            hstore('pkg_blob_id',null)         ||
            hstore('pkgactivate','false')      ||
            hstore('version','{pkgversion}')   ||
            hstore('summary','{pkgsummary}') )""".format(
            userid = self.userid,
            pkgsize=len(pkgbytes),
            hashstring = sha512(pkgbytes).hexdigest(),
            pkgname = tree.find('creation_info').find('filename').text,
            content = tree.find('content_type').text,
            pkgversion = tree.find('code_version').text,
            pkgsummary=summary.replace("'","''" ) 
            )
        returnvalue = self.psql( sqladd )
        if returnvalue == -1:
            print 'add_config not successful for pkg',savedname,' continuing with rest of carton'
            return
        returned_obj_id,returned_blob_id = returnvalue.split('|')
        sqlmodify = """SELECT modify_blobContent({userid}, {blobid})""".format(
            userid = self.userid,
            blobid = returned_blob_id
            )
        _ = self.psql( sqlmodify )
        sqlimport = """SELECT importfile( {userid}, {objid}, {blobid}, '{tmpfilename}' )""".format(
            userid = self.userid,
            objid=returned_obj_id,
            blobid=returned_blob_id,
            tmpfilename=self.tmpfile
            )
        _ = self.psql( sqlimport )
        totalpkgcount = len(self.carton.header)
        print '    %d/%d added obj_id %s, blob_id %s'%(idx+1,totalpkgcount,returned_obj_id,returned_blob_id)
        os.unlink(self.tmpfile)


if __name__=='__main__':
    argc = len(sys.argv)
    if argc < 2:
        print 'usage: {scriptname} /path/to/carton/file/to/be/uploaded'.format(sys.argv[0])
    else:
        cartonname = sys.argv[1]
        tmpfile = '/var/idirect/cache/carton.tmpfile'
        if argc==3:
            tmpfile = sys.argv[2]
        carton = Carton()
        carton.loadCarton(cartonname,tmpfile)
