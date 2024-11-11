from bs4 import BeautifulSoup
import requests
import pandas
import glob
from collections import OrderedDict
pages_csv='characters_pages.csv'
characters_csv='characters_dataset.csv'
# Получение ссылок и их обработка для передачи в csv файл
def get_all_links():
    # Запрос данных с сайта
    page=requests.get('https://www.marvel.com/characters')
    # вызов конвертера данных HTML структуры сайта
    soup=BeautifulSoup(page.content,'html.parser')
    pages=[]
    #Поиск данных из файла по структуре HTML
    mvl_cards=soup.find('div',{'class':'grid-base grid__6'}).find_all('div',{'class':'mvl-card mvl-card--explore'})
    for i in range(len(mvl_cards)-1):
        link=mvl_cards[i]
        #Каждая карточка содержит ссылку на стр героя
        page=link.find('a',{'class':'explore__link'})
        # Достает атрибут href
        print(i,page['href'],page.text)
        #добавляем все ссылки в список
        pages.append(page['href'])
    df=pandas.DataFrame({'Link':pages})
    write_csv_file(df,pages_csv)
# Запись файла в csv формат
def write_csv_file(df,name):
    df.to_csv(name,index=False)
    print("Sucsessefull \n")
# Обратимся к полученному файлу чтение

def read_csv_file(name):
    df=pandas.read_csv(name)
    return df
#Создание файла для записи даннызх из каждой карточки персонажа
def create_characters_df():
    base_url='https://www.marvel.com'
    pages=pandas.read_csv(pages_csv)
    links=pages['Link']
    columns=[]
    marvel_list=[]
    #Проход по всем ссылкам, записанным в csv файл
    for link in links:
        # Данные из карточки
        marvel_characters=OrderedDict()
        # Получение данных из карточки каждого персонажа с сайта
        request=requests.get(base_url+str(link))
        content=request.content
        soup=BeautifulSoup(content,'html.parser')
        marvel_characters['Name']=soup.find('h1').text.replace('\n','').strip()
        marvel_characters['Link']=link
        print(soup.find('h1').text.replace('\n','').strip(),base_url+str(link))
        # Поиск описания персонажа
        label=soup.findAll('p',{'class':'bioheader__label'})
        stat=soup.findAll('p',{'class':'bioheader__stat'})
        for i in range(len(label)):
            column=label[i].text.title()
            if column not in columns:
                columns.append(column)
            try:
                marvel_characters[column]=stat[i].text.replace('\n','').strip()
            except:
                marvel_characters[column]=''
        marvel_list.append(marvel_characters)
    df=pandas.DataFrame(marvel_list)
    write_csv_file(df,characters_csv)
def main():
    files=glob.glob('*.csv')
    if characters_csv not in files:
        if pages_csv not in files:
            print('Создание файла characters_pages.csv')
            get_all_links()
        print('Создание файла characters_dataset.csv')
        create_characters_df()
    df=read_csv_file(characters_csv)
    df=df.fillna('')
    print('Колонки:',df.columns.values)
    print(df[['Link','Eyes']])
    #Чтение данных из файла и отображение
    df=pandas.read_csv('characters_dataset.csv')
    print(df.shape) # размеры файла
if __name__=='__main__':
    main()