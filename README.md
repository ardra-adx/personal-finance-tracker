# personal-finance-tracker

this is a basic tool to track your personal expenses using csv file.Is saves the data in a local database and gives a montly report.

packages:
 pip install pandas tabulate
 datetime

 SQLite3 is used to give us a local database that's portable

 need to setuo a database first
  primary key -used to store the data

  then categorize 
  converts the transaction description to lowercase and checks for key words
  return a category string used later for reporting

  CSV import 
  into pandas dataframe
  add category column
  date,description,amount

  Montly report
  use sqlite strftime to filter rows by month and year

  main content 
  csv imported successfully
  month,year should be given 
  output displayed

  
