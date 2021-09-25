from os import name
from tkinter.font import BOLD, Font
from typing import Text
from bs4 import BeautifulSoup
import requests 
from tkinter import * 
import webbrowser

#webpage info
link = 'https://e24.no/' #Website link
html = requests.get(link).text #html as text 
soup = BeautifulSoup(html, 'lxml')


#list that keeps the info that is displayed...
listTitle = []
listLink = []
listParagraph =[]
listDate = []


class displayNews:
    def findNews(printOutput): #scrapes the page for infor from differnt sections  
        mainContent = soup.find('main', class_ = 'wrapper')

        # all the containers that we want info from 
        topArticle1 = mainContent.find_all('article', class_ = 'article-teaser default grid-col-9 skin-vekt-4-tykk')
        displayNews.findInContainer(topArticle1, printOutput)

        topArticle2 = mainContent.find_all('article', class_ = 'article-teaser default grid-col-3 skin-vekt-4-tykk')
        displayNews.findInContainer(topArticle2, printOutput)

        topArticle3 = mainContent.find_all('article', class_ = 'article-teaser pancake grid-col-12 skin-default')
        displayNews.findInContainer(topArticle3, printOutput)

        midArticle1 =mainContent.find_all('article', 'article-teaser default grid-col-6 skin-default')
        displayNews.findInContainer(midArticle1, printOutput)

        midArticle2 = mainContent.find_all('article', 'article-teaser default grid-col-6 skin-default')
        displayNews.findInContainer(midArticle2, printOutput)




        
    def findInContainer(input, printOutput): # searches the container for articles and prints relavant info...
        for index, article in enumerate(input):
            titleCont = article.find('div', class_='title-container')#headline 
            title = titleCont.find('h3', class_="title").text
            listTitle.append(title)

            #article link
            articleLink = ""
            for link in article.find_all('a'):
                articleLink = (link.get('href'))
            listLink.append(articleLink)

            contentHTML = requests.get(articleLink).text
            content = BeautifulSoup(contentHTML,'lxml')

            # try to find if the article has a paragraf and a date....
            try:
                p = content.find('p', class_= "css-bc5wrv").text
                listParagraph.append(p)
            except:
                p = None

            try:
                date = content.find('time', class_="css-10rvbm3").text
                listDate.append(date)
            except:
                date = None 
            
            if(printOutput == True):
                print(f'''
                Title : {title}
                Link : {articleLink}
                Paragarf: {p}
                {date}
                ''')

class test: # DEBUG(KJETIL): not working
    def fixList(lt): #checks the list for duplicate
        for i in range(0,len(lt)):
            cur = lt[i]
            for k in range(0, len(lt)):
                if(k != i):
                    if(cur == lt[k]):
                        try:
                            test.removeArticle(k)
                        except:
                            None 
                        
                else:
                    continue



    def removeArticle(nr): #removes article from list 
        listTitle.remove(nr)
        listParagraph.remove(nr)
        listLink.remove(nr)
        listDate.remove(nr)
        


#Display by using tkinter 
height = 0
width = 0

class app:
    def mainWindow(h, w):
        window = Tk()
        dim = str(w) +"x"+str(h)
        window.geometry(dim)
        window.title("E4 News Overview")
        font = Font(family="Helvetica",size=10,weight="bold")

        e24font = Font(family="Times",size=30, weight="bold")
        e24title = Label(window, text="E24 - NEWS", font=e24font)
        e24title.grid(column=0, row=0)
        articleTitleFont= Font(family="Times", size =12)
        #puts input as labels and directly on the screen 
        test.fixList(listTitle) # fix the list
        
        for i in range(1,len(listTitle)): #for each column
            Label(
                window,text=listTitle[i-1],
                borderwidth=1,
                highlightbackground="red", 
                highlightcolor="red",
                border=True,
                font=articleTitleFont).grid(
                column=0, 
                    sticky=W, 
                    padx=20)

        
            Label(
                window,
                text=listDate[i-1],
                borderwidth=1,
                border=True,
                font=font).grid(
                    column=1, 
                    row=i, 
                    sticky=E, 
                    padx=5)
                
            def OpenUrl(url):
                webbrowser.open(url)
            url = listLink[i-1]
            Button(
                window,
                text="Go to article!", 
                command = lambda aurl=url:OpenUrl(aurl),
                background="blue",
                fg="white").grid(
                    column=2, 
                    row=i,)



        window.mainloop()



def main():
    displayNews.findNews(False)

if __name__ == "__main__":
    main()
    app.mainWindow(1080,1920)