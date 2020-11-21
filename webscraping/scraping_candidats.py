 """
cree un robot qui va se connecter a mon profil linkeding 
puis aller sur google faire une recherche de candidats 
aller sur leur page linkedin et extraire les info interressantes
puis les stocker dans un premier sous fichier csv. 

On pourra par la suite extraire aussi les info concernant les postes 
et les stocker aussi dans un fichier csv dans un premier temps. 


!apt-get update
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
!pip install selenium
# set options to be headless, ..
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# open it, go to a website, and get results
wd = webdriver.Chrome('chromedriver',options=options)
wd.get("https://www.website.com")
print(wd.page_source)  # results

"""
from selenium import  webdriver
#inporter la librairy pour le delai
from time import sleep
#importer la librairie qui permettra d'imiter les touches 'keys'
from selenium.webdriver.common.keys import Keys
#importer mes parametres de recherches
import parameters
#importer le selector
from parsel import Selector
#on va sauvegarder les données dans un csv pour l'instant
import csv
#pour prendre des valeurs au hasard
import random
#remplacer des valeurs
import re

# fonction pour verifier que les champs ont des valeurs
def validate_field(field):
    if field:
        pass
    else:
        field = 'pas de resultat'
    return field

print("hello")
#fonction qui supprime les espaces dans les listes
def espace(liste):
    try: 
        for i in range(len(liste)-1):
            if liste[i]=="":
                del liste[i]
    except: 
        print("espaces enlevées")
    return liste 

#enlever les espaces dans l'object
def clean(liste):
    if liste:
        if liste != "pas de resulat":
            liste = liste.strip()
        else: 
            pass
    return liste

def clean_liste(liste):  
    if liste != "pas de resultat":
        liste1 = []
        for k in liste: 
            liste1.append(clean(k))
    else:
        liste1 = "pas de resultat"
    return liste1

#je crée mon fichier csv dans lequel sera sauvegarder les fiches des candidats

f = open(parameters.file_name, 'w', newline ='')
z = csv.writer(f, delimiter=';')
z.writerow(['nom','lieu','poste','entreprise','duree','universite','domaine','description','hard-skills','soft-skills','url'])
f.close()


#utiliser le driver correspondant Ã  mon navigateur et ouvrir le navigateur
driver = webdriver.Chrome('C:/Users/moi/Desktop/projet finder/webscraping/chromedriver')
#attendre 5 secondes
sleep(5)
#charger la page d'acceuil linkedin
driver.get('https://www.linkedin.com')
#attendre 5 secondes
sleep(5)
#selecionner la zone de saisie de l'username et entrer l'username
driver.find_element_by_name('session_key').send_keys(parameters.linkedin_username)
#attendre 2secondes
sleep(2)

#â»selectionner la zone de saisie du mot de passe et entrer le mot de passe
driver.find_element_by_name('session_password').send_keys(parameters.linkedin_password)
#attendre 2 secondes
sleep(4)

#reperer le button login et appuyer
try: 
    driver.find_element_by_class_name('sign-in-form__submit-button').click()
except:
    driver.find_element_by_class_name('sign-in-form__submit-btn').click()


#aller sur google pour faire sa recherche
driver.get('https://www.google.com')
#chercher la barre de recherche google
search_query= driver.find_element_by_name('q')
#saisir ma recherche
search_query.send_keys(parameters.search_query)
#attendre 3 secondes
sleep(3)
#appuer sur la touche valider
search_query.send_keys(Keys.RETURN)

#le nombre de candidat retenus
nombre_candidat =0
breaker = False
next_page= False
page = 3
while True :

    if next_page == True:      
        #aller sur google pour faire sa recherche
        driver.get('https://www.google.com')
        #chercher la barre de recherche google
        search_query= driver.find_element_by_name('q')
        #saisir ma recherche
        search_query.send_keys(parameters.search_query)
        #attendre 3 secondes
        sleep(3)
        #appuer sur la touche valider
        search_query.send_keys(Keys.RETURN)
        
        #presser la prochaine page
        driver.find_element_by_xpath('//*[@id="xjs"]/div/table/tbody/tr/td['+str(page)+']/a').click()
        #je reinitialise la boucle
        next_page = False
        #j'incrémente page
        page = page+1
    
    #selectionner seuls les elements ayant les parametres de recherches sans prendre les pubs
    linkedin_names= driver.find_elements_by_class_name('iUh30')
    
    #inserer dans une liste ces personnes
    
    linkedin_names = [url.text for url in linkedin_names]
    
    # supprimer les espaces presents entres chaque personnes
    espace(linkedin_names)
    
    #nombre de personnes selectionnée
    len(linkedin_names)
    
    #enlever les liens qui ont des 3 points car elles ne fonctionnent pas. 
    linkedin_names_good_to_use =[]
    for p_ in linkedin_names:
        _3_points= False
        for k in range(len(p_)):
            if p_[k:k +3] == "...":
                _3_points=True
                break   
        if _3_points == False: 
           linkedin_names_good_to_use.append(p_)
    
    len(linkedin_names_good_to_use)
          
    #creer les urls Ã  partir des good names to use  
    linkedin_urls =[]
    for p in linkedin_names_good_to_use:
        url ="https://"
        for  x_ in  range(len(p)): 
            if p[x_:x_+3] == "...":
                name = "true"
            if p[x_] != " " and p[x_] != "›":
                url= str(url) + str(p[x_])
            elif p[x_] == " ":
                url=str(url) + str("/")
            elif p[x_] == "›":
                url=str(url) + str("in")
        linkedin_urls.append(url)
    
    linkedin_urls1= ["https://www.linkedin.com/in/vianney-njock-491aab11b/"]
    linkedin_url = linkedin_urls1[0]
    #for loop pour recuperer les codes sources de chaque candidats
    for linkedin_url in linkedin_urls:
        #si on attend la de la liste on passe a la prochaine page google
        if linkedin_url == linkedin_urls[-1]:
            next_page = True
        #prendre le profil de la personne
        driver.get(linkedin_url)
        # attendre 10 seconde le temps de chargement de la page
        sleep(10)
        #prendre le code source de la page
        sel = Selector(text=driver.page_source)
        
        #selectionner et extraire l'info qu'on veut recuperer
        #=========================================extraire le nom==================================#
        name = sel.xpath('//*[starts-with(@class, "inline t-24 t-black t-normal break-words")]/text()').extract_first()
        #verifier que le field name contient quelque chose
        name= validate_field(name)
        #enlever les espaces et /n indÃ©sirables
        name=clean(name)
        print(name)
        
        #=========================================extraire le lieu==================================#
        lieu = sel.xpath('//*[starts-with(@class, "t-16 t-black t-normal inline-block")]/text()').extract_first()
        #verifier que le field name contient quelque chose
        lieu= validate_field(lieu) 
        #enlever les espaces et /n indÃ©sirables
         
        lieu= clean(lieu)
        print(lieu)
    
        #=========================================experience==================================#    
        
        #==========poste
        poste_ = sel.xpath("//*[starts-with(@class,'t-16 t-black t-bold')]/text()").extract() 
        #verifier que le field name contient quelque chose t-16 t-black t-bold
        poste_= validate_field(poste_)  
        #enlever les espaces et /n indÃ©sirables    
        poste = clean_liste(poste_)
        #supprimer les espaces entre les elements de la liste
        poste = espace(poste)
        print(poste)
        if poste =="pas de resultat":
            pass
        
        #=========entreprise
        entreprises_ = sel.xpath('//*[starts-with(@class, "pv-entity__secondary-title t-14 t-black t-normal")]/text()').extract()
        #verifier que le field name contient quelque chose
        entreprises_= validate_field(entreprises_)
        #enlever les espaces et /n indÃ©sirables
        entreprises= clean_liste(entreprises_)
        #supprimer les espaces dans la liste
        entreprises= espace(entreprises)
        
        print(entreprises)
    
        #===================duree1
        duree1 = sel.xpath('//*[starts-with(@class, "pv-entity__bullet-item-v2")]/text()').extract()
        #verifier que le field name contient quelque chose
        duree1= validate_field(duree1)
        duree = clean_liste(duree1)
        duree = espace(duree)
        #replacer les yrs et yr et mos par years et mois 
        if duree != "pas de resultat":
            dureee =[]
            for k in duree:
                mois = False
                for o in range(len(k)):
                    try:
                        if mois != True:
                            dureee.append(float(k[o]))
                        else:
                            dureee.append(0.1*float(k[o]))
                    except:
                        mois = True
                        pass
                duree  =int(sum(dureee))
                '''
                #duree[k] = duree[k].replace('yr','an')
                duree[k]=  re.sub('yrs|yr','.',duree[k])              
                duree[k]=  re.sub('mos|mo','',duree[k])
                duree[k]=   re.sub(' ','',duree[k])
                '''
        print(duree)
        #=========================================education==================================#    
  
        #===============universite
        education_universite_ = sel.xpath('//*[starts-with(@class, "pv-entity__school-name t-16 t-black t-bold")]/text()').extract()
        #verifier que le field name contient quelque chose
        education_universite_= validate_field(education_universite_)
         
        education_universite = clean_liste(education_universite_)
        education_universite = espace(education_universite)
        print(education_universite)
        #===============specialisation
        specialisation_ = sel.xpath('//*[starts-with(@class, "pv-entity__comma-item")]/text()').extract()
        #verifier que le field name contient quelque chose
        specialisation_= validate_field(specialisation_)
        specialisation = clean_liste(specialisation_)
        specialisation = espace(specialisation)
    
        print(specialisation)
        #==================================description
        description_ = sel.xpath('//*[starts-with(@class,"pv-entity__description t-14 t-normal mt4")]/text()').extract()   
        description  = validate_field(description_ )
        description  = espace(clean_liste(description))
       
        print(description)
    
        #====================licences et certification
        certif_ = sel.xpath('//*[starts-with(@class,"t-16 t-bold")]/text()').extract()
        #verifier que le field name contient quelque chose
        certif_ = validate_field(certif_ )
        certif = clean_liste(certif_)
        certif = espace(certif)
    
        print(certif)
        #==================================hard skills 
        skills_ = sel.xpath("//*[starts-with(@class,'pv-skill-category-entity__name-text t-16 t-black t-bold')]/text()").extract()   
        #attribue des hard_skills si le candidats n'en a pas 
        if skills_:
            pass
        else:
            skills_ = parameters.hard_skills(random.randint(1,5)) #prendre une valeur au hasard pour l'hardskills
        skills = validate_field(skills_ )
        skills = clean_liste(skills)
        skills = espace(skills)
    
        print(skills)
        #--------------------------------------------------------------soft skills----------------------------
        #genere des soft skills au hasard
        soft_skills = parameters.soft_skills(random.randint(1,5))
        
        print(soft_skills)
        #==================================interests
        interests_ = sel.xpath('//*[starts-with(@class,"pv-entity__summary-title-text")]/text()').extract()   
    
        interests = validate_field(interests_)
        interests = clean_liste(interests)
        interests = espace(interests)
        
        print(interests)
        
        print("\n #----------------ecriture des données dans le fichier csv ----------------# ")

        if poste != "pas de resultat":
            poste= " , ".join(poste)
        else: 
            poste = poste
        if entreprises != "pas de resutat":
            entreprises = " , ".join(entreprises)
        else:
            entreprises = entreprises
        if education_universite != "pas de resultat":
            education_universite = " , ".join(education_universite)
        else:
            education_universite = education_universite
        if specialisation != "pas de resultat":
            specialisation = " , ".join(specialisation)
        else:
            specialisation = specialisation
        if description != "pas de resultat":
            description = " , ".join(description)
        else:
            description = description
        if duree == "pas de resultat":
            duree = 0
        else:
            duree = duree
        try:
            f = open(parameters.file_name, 'a', newline ='')
            z = csv.writer(f, delimiter=';')
            z.writerow([name,lieu,poste,entreprises,str(duree)+"année",education_universite,specialisation,
                        description," , ".join(skills)," , ".join(soft_skills),linkedin_url])
            f.close()
        except:
            pass
        
        print("\n #-----------------------profil suivant --------------------------# \n")
        
        #sortir de la loop si on a atteint notre quota de candidats
        if nombre_candidat > 20: 
            breaker = True
            break
        nombre_candidat = nombre_candidat +1
   
    if breaker:
        break
 
    
#arreter le driver et fermer le navigateur
driver.quit()
