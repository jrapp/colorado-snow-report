
from pyvirtualdisplay import Display
from selenium import webdriver
from datetime import date
import time
import boto3
import logging
import sys
import re

class ColoradoSnowReport:
    def __init__(self):
        #initialize the logger
        logging.basicConfig(filename='snow-report.log',level=logging.INFO)

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
        except Exception as e:
            logging.error(date.today().isoformat())
            logging.error('Error obtaining Breckenridge data')
            logging.error(str(e))
            snowfall = 'error'
        try:
            self.post_to_table('Breckenridge', snowfall)
        except Exception as e:
            logging.error(date.today().isoformat())
            logging.error(str(e))
            logging.error('could not post data to dynamodb')

        logging.debug('Posted Breckenridge data to Snow Report Table')

    def Keystone(self):
        snowfall = 'nr'
        try:
            self.driver.get('http://www.keystoneresort.com/ski-and-snowboard/snow-report.aspx')
            temp = self.driver.find_element_by_class_name('snowReportPage')
            temp = temp.find_element_by_class_name('snowBorder')
            temp = temp.find_element_by_id('snowReport')
            temp = temp.find_element_by_class_name('snowReportData')
            temp = temp.find_element_by_class_name('snowReportDataColumn1')
            temp = temp.find_element_by_class_name('snowfallData')
            temp = temp.text.split(' ')
            logging.debug('Keystone reported ' + temp[0]);
            snowfall = temp[0]
        except Exception as e:
            logging.error('Error obtaining Keystone data')
            snowfall = 'error'
            logging.error(str(e))
        try:
            self.post_to_table('Keystone', snowfall)
        except Exception as e:
            logging.error(date.today().isoformat())
            logging.error('could not post keystone data to dynamodb')
            logging.error(str(e))
        logging.debug('Success posting keystone to dynamodb')

    def Vail(self):
        snowfall = 'nr'
        try:
            self.driver.get('http://www.vail.com/mountain/current-conditions/snow-and-weather-report.aspx')
            temp = self.driver.find_element_by_class_name('snowReportPage')
            temp = temp.find_element_by_class_name('snowBorder')
            temp = temp.find_element_by_id('snowReport')
            temp = temp.find_element_by_class_name('snowReportData')
            temp = temp.find_element_by_class_name('snowReportDataColumn1')
            temp = temp.find_element_by_class_name('snowfallData')
            temp = temp.text.split(' ')
            logging.debug('Vail reported ' + temp[0]);
            snowfall = temp[0]
        except Exception as e:
            logging.error(date.today().isoformat())
            logging.error('Error obtaining Vail data')
            logging.error(str(e))
            snowfall = 'error'
        try:
            self.post_to_table('Vail', snowfall)
        except Exception as e:
            logging.error('could not post vail data to dynamodb')
            logging.error(str(e))
        logging.debug('Success posting vail to dynamodb')


    def A_Basin(self):
        snowfall = 'nr'
        try:
            self.driver.get('http://arapahoebasin.com/ABasin/snow-conditions/')
            temp = self.driver.find_element_by_class_name('page')
            temp = temp.find_element_by_class_name('clearfix')
            temp = temp.find_element_by_tag_name('article')
            temp = temp.find_element_by_id('mountain-conditions')
            temp = temp.find_element_by_class_name('nine')
            temp = temp.find_elements_by_tag_name('li')
            temp = re.search(r'\d+',temp[0].text).group()
            logging.debug('A-Basin reported ' + temp[0])
            snowfall = temp[0]
        except Exception as e:
            logging.error(date.today().isoformat())
            logging.error('Error getting A-Basin data')
            logging.error(str(e))
            snowfall = 'error'
        try:
            self.post_to_table('A-Basin', snowfall)
        except Exception as e:
            logging.error(date.today().isoformat())
            logging.error('Error posting to dynamodb')
            logging.error(str(e))
        logging.debug('Success posting a-basin to dynamodb')

    def Copper(self):
        snowfall = 'nr'
        try:
            self.driver.get('http://www.coppercolorado.com/winter/the_mountain/dom/snow.html')
            temp = self.driver.find_element_by_id('report-page-conditions-snow')
            temp = temp.find_elements_by_tag_name('tr')
            temp = temp[2].find_elements_by_tag_name('td')
            temp = temp[0].text.split('.')
            snowfall = temp[0]
            logging.debug('Copper reported ' + snowfall)
        except Exception as e:
            logging.error(date.today().isoformat())
            logging.error('Error getting Copper data')
            logging.error(str(e))
            snowfall = 'error'
        try:
            self.post_to_table('Copper',snowfall)
            logging.debug('Success posting copper to dynamodb')
        except Exception as e:
            logging.error(date.today().isoformat())
            logging.error('Error posting to dynamodb')
            logging.error(str(e))


    def WinterPark(self):
        snowfall = 'nr'
        try:
            self.driver.get('https://www.winterparkresort.com/the-mountain/weather-dashboard')
            temp = self.driver.find_element_by_class_name('recent-snowfall')
            temp = temp.find_elements_by_class_name('data-point')
            temp = re.search(r'\d+',temp[1].text).group()
            snowfall = temp
        except Exception as e:
            logging.error(date.today().isoformat())
            logging.error('Error getting Winter Park data')
            logging.error(str(e))
            snowfall = 'error'
        try:
            self.post_to_table('Winter Park',snowfall)
            logging.debug('Success posting Winter Park to DynamoDB')
        except Exception as e:
            logging.error(date.today().isoformat())
            logging.error('Error posting to DynamoDB')
            logging.error(str(e))


    def Steamboat(self):
        snowfall = 'nr'
        try:
            self.driver.get('https://www.steamboat.com/the-mountain/conditions-report')
            temp = self.driver.find_element_by_class_name('recent-snowfall')
            temp = temp.find_elements_by_class_name('data-point')
            temp = re.search(r'\d+',temp[1].text).group()
            snowfall = temp
        except Exception as e:
            logging.error(date.today().isoformat())
            logging.error('Error getting Steamboat data')
            logging.error(str(e))
            snowfall = 'error'
        try:
            self.post_to_table('Steamboat',snowfall)
            logging.debug('Success posting Steamboat to DynamoDB')
        except Exception as e:
            logging.error(date.today().isoformat())
            logging.error('Error posting Steamboat data to DynamoDB')
            logging.error(str(e))

    def Eldora(self):
        snowfall = 'nr'
        try:
            self.driver.get('https://www.eldora.com/the-mountain/snow-grooming-report/')
            temp = self.driver.find_element_by_id('h-snowfall-data-24')
            temp = temp.find_element_by_class_name('h-weather-small-text')
            temp = re.search(r'\d+',temp.text).group()
            snowfall = temp
        except Exception as e:
            logging.error(date.today().isoformat())
            logging.error('Error getting Eldora data')
            logging.error(str(e))
            snowfall = 'error'
        try:
            self.post_to_table('Eldora',snowfall)
            logging.debug('Sucess posting Eldora to DynamoDB')
        except Exception as e:
            logging.error(date.today().isoformat())
            logging.error('Error posting Eldora data to DynamoDB')
            logging.error(str(e))




if __name__ == "__main__":
    #Call the constructor
    csr = ColoradoSnowReport()
    #Call the functions for the individual resorts
    csr.Breckenridge()
    csr.A_Basin()
    csr.Keystone()
    csr.Vail()
    csr.Copper()
    csr.WinterPark()
    csr.Steamboat()
    csr.Eldora()
    #Close the chrome driver
    csr.driver.close()


