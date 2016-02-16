import unittest
import RegexFinder as reg
class RegexFinderTests(unittest.TestCase):

    def testOne(self):
        self.assertEqual("String","String")

    def testHashTags(self):
    	regexFinder = reg.RegexFinder()
    	line = "#blossom"
    	self.assertEqual(regexFinder.subHashtags(line),"0h_tag0")

   	def testAccountTags(self):
   		regexFinder = reg.RegexFinder()
   		line = "@jeremy"
   		self.assertEqual(regexFinder.subAccountTags(line),"0a_tag0")

    def testURLTags(self):
      regexFinder = reg.RegexFinder()
      line = "www.testURLTags.com"
      self.assertEqual(regexFinder.subURLTags(line),"0url_tag0")

    def testJWTags(self):
      regexFinder = reg.RegexFinder()
      line = "To.night"
      self.assertEqual(regexFinder.subJoinedWordTags(line),"0jw_tag0")

    def testExcessLetterTags(self):
      regexFinder = reg.RegexFinder()
      line = "Helloooo"
      self.assertEqual(regexFinder.subExcessLetterTags(line),"0el_tag0")


def main():
    unittest.main()

if __name__ == '__main__':
    main()