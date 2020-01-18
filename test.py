import unittest
import time
from pathlib import Path
from calendar import monthrange
from zmedia import Journal

#For journal entry creation
#---
METADATA='''\
Content-Type: text/x-zim-wiki
Wiki-Format: zim 0.4
Creation-Date: Not Relevant
'''
HEADER='''\
====== {month} {year} ======

'''
CONTENT='''\
==== {year}/{month}/{day} ====

Log:
    * Generic event
    * Generic event
    * Generic event
    * Generic event
    
Comments:
    * Generic Comment

'''
JOURNALDIR = './test-environment/Journal/'
MINYEAR, MAXYEAR = 2013, 2021
#---

class TestJournalMediaClass(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        '''Set up the files we need for testing'''
        
        for year in range(MINYEAR, MAXYEAR):
            year = str(year)                # convert to str for .joinpath()
            year_dir = Path(JOURNALDIR + year)
            year_dir.mkdir(parents=True)
            
            for month in range(1,13):
                entry = ''                  # reset here or it accumulates
                month = str(month)          # same deal as above
                month_path = year_dir.joinpath(month + '.txt')
                entry += METADATA + HEADER.format(year=year, month=month)
                
                for day in range(1, monthrange(int(year), int(month))[1] + 1):
                    # Populate the entries by day
                    entry += CONTENT.format(year=year, month=month, day=day)
                month_path.write_text(entry)

    @classmethod
    def tearDownClass(cls):
        '''Delete the actual files then rmdir recursively in reverse'''
        journal_dir = Path(JOURNALDIR)
        
        for year_dir in journal_dir.iterdir():
            for f in year_dir.iterdir():
                f.unlink()
            year_dir.rmdir()
        journal_dir.rmdir()                #rmdir "Journal"
        Path(journal_dir.parent).rmdir()   #rmdir "test-environment"

    def test_journal_init(self):
        '''Test that we can create journals and retrieve their contents
        -Verify headings & contents
        -Add a heading for media links
        Search a directory for media to add to entries'''
        
        #load and verify journal contents
        journal = Journal(JOURNALDIR)
        for log in journal.logs:
            self.assertEqual(METADATA, log.metadata)
        
        #ensure each journal entry has: date, header, contents 
        #TEST STILL IN PROGRESS
        for entry in journal.entries:
            self.assertNotEqual('', entry.contents)
    
    def test_media_referencing(self):
        pass
    
if __name__ == "__main__":
    unittest.main()
