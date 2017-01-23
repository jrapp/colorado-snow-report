
from pyvirtualdisplay import Display
from selenium import webdriver
import boto3


#Initialize the web driver
display = Display(visible=0, size=(800,600))
display.start()
driver = webdriver.Chrome()

#Set up boto3 to work with the SnowReport table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SnowReport')
print(table.creation_date_time)

driver.get('http://christopher.su')
print(driver.title)


