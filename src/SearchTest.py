'''
Author: Nicholas Bright
Created Date: 2019-12-03
Last Updated: 2019-12-03
Version: 1.0.0
Purpose:
Tests that SearchListPage can successfully search a list and get the correct results returned
'''
from CheeseModel import CheeseModel
import unittest
from ViewBasics import SearchListPage

print("Nicholas Bright - Unit Test - SearchListPage")

class TestSearchListPage(unittest.TestCase):
  """A test object that tests the SearchListPage object"""
  def testSearchResults(self):
    """Ensures that SearchListPage filters cheese objects correctly"""
    cheeseList = [
      CheeseModel(CheeseId = 1, CheeseNameEN="Cheese"),
      CheeseModel(CheeseId = 2, CheeseNameEN="heese"),
      CheeseModel(CheeseId = 3, CheeseNameEN="Ceese"),
      CheeseModel(CheeseId = 4, CheeseNameEN="Chse"),
      CheeseModel(CheeseId = 5, CheeseNameFR="Cheese"),
      CheeseModel(CheeseId = 6, CheeseNameFR="eese"),
      CheeseModel(CheeseId = 7, CheeseNameEN="Fromage"),
      CheeseModel(CheeseId = 8, CheeseNameEN="Homage"),
      CheeseModel(CheeseId = 9, CheeseNameEN="Cheese"),
      CheeseModel(CheeseId = 10, ManufacturerNameEN="Cheese")
    ]
    firstSearchLine = "CheeseNameEN:Cheese"
    secondSearchLine = "CheeseNameEN:eese"
    thirdSearchLine = "CheeseNameEN:z"
    searchPage = SearchListPage(cheeseList)

    #Test that only the Cheeses with ID 1 and 9 have a CheeseNameEN containing "Cheese"
    searchPage.searchLine = firstSearchLine
    searchPage.filterList()
    for cheese in searchPage.displayList:
      self.assertIn(cheese.CheeseId, [1, 9])
    
    #Test that only the Cheeses with ID 1, 2, 3 and 9 have a CheeseNameEN containing "eese"
    searchPage.searchLine = secondSearchLine
    searchPage.filterList()
    for cheese in searchPage.displayList:
      self.assertIn(cheese.CheeseId, [1, 2, 3, 9])
    
    #Test that no cheeses are found with CheeseNameEN containing "z"
    searchPage.searchLine = thirdSearchLine
    searchPage.filterList()
    for cheese in searchPage.displayList:
      self.assertTrue(False, "List should be empty")

if __name__ == '__main__':
    unittest.main()