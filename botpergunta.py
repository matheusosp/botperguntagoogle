from selenium import webdriver #line:11
import PySimpleGUI as sg
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class Perguntagoogle:
    def _init_ (self):
        sg .theme ('DarkBlack1')
        layout=[
            [sg .Text ('Qual a pergunta? ')],
            [sg .Input (key ='pergunta')],
            [sg .Button ('Perguntar',size =(10 ,2 )),sg .Exit ('Fechar',size =(10 ,2 ))]
        ]
        window =sg .Window ('Pergunta Google',layout,size =(500 ,100),element_justification ='center')
        event, values = window.read()
        while True :
            self.inputpergunta =values['pergunta']
            if event == sg .WIN_CLOSED or event =='Fechar':
                break 
            if event == 'Perguntar':
                with open ('pergunta.txt','w')as pergunta:
                    pergunta.write('Pergunta: \n'+self.inputpergunta+'\n')                
                pergunta.close()    
            break    

    def Start(self):
        if(self.inputpergunta!=''):
            options = webdriver.ChromeOptions()      
            options.add_argument('lang=pt-br')   
            self.driver= webdriver.Chrome(
                executable_path='./chromedriver.exe', chrome_options=options)#line:102    
            self.driver.get('https://www.google.com') 
            wait=WebDriverWait(self.driver,10) 
            googleinput=wait.until(EC.element_to_be_clickable((
                By.XPATH,f'/html/body/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input')))    
            googleinput.click() 
            googleinput.send_keys(self.inputpergunta) 
            googleinput.submit()
            wait.until(EC.presence_of_element_located((
                By.XPATH,'//span[@class="hgKElc"]')))                  
            resposta=self.driver.find_element_by_xpath('//span[@class="hgKElc"]').get_attribute('innerHTML')           
            arquivo = open('pergunta.txt', 'r') 
            conteudo = arquivo.readlines()
            conteudo.append('Resposta:\n')  
            resposta.encode("latin1").decode("unicode_escape")          
            if(resposta!=''):
                conteudo.append(resposta)
                arquivo = open('pergunta.txt', 'w') 
                arquivo.writelines(conteudo)   
                arquivo.close() 
            self.driver.quit()
            arquivoo = open('pergunta.txt', 'r') 
            conteudo = arquivoo.readlines()
            arquivoo.close()
            sg.popup(conteudo)   
            bot = Perguntagoogle()
            bot.Start()               
if _name_ == '_main_':
    bot = Perguntagoogle()
    bot.Start()