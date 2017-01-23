
from pyvirtualdisplay import Display
from selenium import webdriver
from datetime import date
import time
import boto3
import logging
import sys

class ColoradoSnowReport:
    def __init__(self):
        #initialize the logger
        logging.basicConfig(filename='snow-report.log',level=logging.DEBUG)

        #Initialize the web driver
        self.display = Display(visible=0, size=(800,600))
        self.display.start()
        self.driver = webdriver.Chrome()
        logging.debug('Initialized Chrome Webdriver')

        #Set up boto3 to work with the SnowReport table
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('SnowReport')
        logging.debug('Sucessfully initialized SnowReport table resource')

    def post_to_table(self, resort, reporting):
        self.table.put_item(
            Item={
                'Date':date.today().isoformat(),
                'Resort':resort,
                'Reporting': reporting,
            }
        )
        logging.debug('Posted item: ' + date.today().isoformat() + ', ' + resort + ', ' + reporting) 

    def Breckenridge(self):
        snowfall = 'nr'
        try:
            self.driver.get('http://www.breckenridge.com/mountain/snow-and-weather-report.aspx')
            temp = self.driver.find_element_by_class_name('snowReportPage')
            temp = temp.find_element_by_class_name('snowBorder')
            temp = temp.find_element_by_id('snowReport')
            temp = temp.find_element_by_class_name('snowReportData')
            temp = temp.find_element_by_class_name('snowReportDataColumn1')
            temp = temp.find_element_by_class_name('snowfallData')
            temp = temp.text.split(' ')
            logging.debug('Breck reported' + temp[0])
            snowfall = temp[0]
        except:
            logging.error('Error obtaining Breckenridge data')
            snowfall = 'error'
        try:
            self.post_to_table('Breckenridge', snowfall)
        except:
            logging.error('could not post data to dynamodb')

        logging.debug('Posted Breckenridge data to Snow Report Table')

    def A_Basin(self):
        snowfall = 'nr'
        try:
            self.driver.get('http://arapahoebasin.com/ABasin/snow-conditions/')
            temp = self.driver.find_element_by_class_name('columns')
            print(temp)
            temp = temp.find_element_by_class_name('page-image')
            print('2')
            temp = temp.find_element_by_id('mountain-conditions')
            print('3')
            temp = temp.find_element_by_class_name('nine')
            print('4')
            temp = temp.find_elements_by_tag_name('li')
            print('5')
            temp = temp[0]
            print(temp)
        except:
            print(sys.exc_info())

if __name__ == "__main__":
    #Call the constructor
    csr = ColoradoSnowReport()
    #Call the functions for the individual resorts
    #csr.Breckenridge()
    csr.A_Basin()
    csr.driver.close()


