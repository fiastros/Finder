"""
cree un robot qui va se connecter a mon profil linkeding 
puis aller sur google faire une recherche de candidats 
aller sur leur page linkedin et extraire les info interressantes
puis les stocker dans un premier sous fichier csv. 

On pourra par la suite extraire aussi les info concernant les postes 
et les stocker aussi dans un fichier csv dans un premier temps. 
"""
from selenium import  webdriver
#inporter la librairy pour le delai
from time import sleep
#travailler avec les directory
import os
os.chdir("C:/Users/moi/Desktop/projet finder/webscraping")
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
#charger la page d'acceuil linkedin
driver.get('https://www.linkedin.com')
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

# driver.get('https://www.linkedin.com') #parfois ca me demande d'enregistrer un numero du coup je saute cette etape

#aller sur google pour faire sa recherche
# driver.get('https://www.google.com')
offre = "data scientist"
lieu = "France"
offre = offre.split(" ")
poste =""
if len(offre) > 1:
    poste = "%20".join(offre)
    # poste = poste +'%20'+str(offre[i])
else:
    poste = offre[0]

#requête ou on va avoir tous les offres d'entreprise selon le poste et le lieu.
offre_query = 'https://www.linkedin.com/jobs/search/?geoId=105015875&keywords='+str(poste)+'&location='+str(lieu)
driver.get(offre_query)

liste_offre_id =[]
quota_offre = False
quota = 10
page = 0
offre_page = 1
#on repete récupère les informations tant qu'on a pas le nombre d'offres requis
new =True
while quota_offre == False:
    #reinitialise la next page
    next_page = False
    
    #si on change de page, alors on réinitialise le nom du premier link
    if new == True:
        #TODO apparement linkedin change le nom des balises assez frequement dont il faut changer le name !!
        # name= "job-card-container relative job-card-list job-card-container--clickable job-card-list--underline-title-on-hover jobs-search-two-pane__job-card-container--active jobs-search-two-pane__job-card-container--viewport-tracking-0"
        name="job-card-container relative job-card-list job-card-container--clickable job-card-list--underline-title-on-hover jobs-search-results-list__list-item--active jobs-search-two-pane__job-card-container--viewport-tracking-0"
        new = False
    else: 
        name= "job-card-container relative job-card-list job-card-container--clickable job-card-list--underline-title-on-hover  jobs-search-two-pane__job-card-container--viewport-tracking-"+str(offre_page)
   
    #on preleve l'id de chaque offre
    try: 
        offre_id = driver.find_elements_by_xpath(".//div[@class='"+str(name)+"']")[0]
        offre_id = offre_id.get_attribute("data-job-id")
        offre_id = offre_id.split(":")[-1]
        liste_offre_id.append(offre_id)   #on append l'id de l'offre dans la liste des offres
    except:  #sion peut plus prendre id sur la même page
        next_page = True

    #on doit aller sur la prochaine ou non. 
    if next_page == True:
        #incrémenter le numero de la page
        page = page +1
        #attendre 3 secondes avant de selectionner la page suivante
        sleep(3)
        #prendre le numero de la page actuelle
        try:
            driver.find_element_by_xpath('/html/body/div[8]/div[3]/div[3]/div/div/div/section/div/div/section/div/ul/li['+str(page)+']/button').click()
        except:  #si on a plus de page suivante, on sort de la boucle
            pass
            #break
        
        #on reinitialise le numero de l'offre
        offre_page = 1
        #changement de page effectuer
        new = True
    else:
        #on pass à la prochaine offre
        offre_page = offre_page +1
        #on est sur la même page
        new = False
    
    
    #on verifie si on a atteint le quota d'offre requis. 
    if len(liste_offre_id) < quota :
        quota_offre = False
    else: #on a atteint le quota
        quota_offre = True
    
#pour chaque id d'offre on ira a la page
for num in liste_offre_id:
    # num = liste_offre_id[1]
    offre_query ='https://www.linkedin.com/jobs/search/?currentJobId='+str(num)+'&geoId=105015875&keywords='+str(poste)+'&location='+str(lieu)
    # driver.get(offre_query)
    driver.get("https://www.linkedin.com/jobs/view/"+str(num)+"/?alternateChannel=search&refId=a7fc9158-4a59-44c6-8830-307ba7c2e335&trk=flagship3_search_srp_jobs")    
    
    #prendre le code source de la page
    sel = Selector(text=driver.page_source)
    
    ###########prendre le titre du poste
    titre = sel.xpath('//*[starts-with(@class, "jobs-top-card__job-title t-24")]/text()').extract_first()
    titre = validate_field(titre)
    #enlever les espaces et /n indÃ©sirables
    titre=clean(titre)
    print(titre)

    ###############extraire le nom de l'entreprise
    
    entreprise = sel.xpath('//*[starts-with(@class, "jobs-top-card__company-url t-black ember-view")]/text()').extract_first()
    entreprise  = validate_field(entreprise )
    #enlever les espaces et /n indÃ©sirables
    entreprise =clean(entreprise )
    print(entreprise )
    
    #########extraire le lieu de l'offre
    
    lieu = sel.xpath('//*[starts-with(@class, "jobs-top-card__exact-location t-black--light link-without-visited-state")]/text()').extract_first()
    lieu  = validate_field(lieu)
    if lieu == "pas de resultat": #parfois le texte du lieu est un lien et donc cela change le nom de l'attribut de la balise
        lieu = sel.xpath('//*[starts-with(@class, "jobs-top-card__bullet")]/text()').extract_first()
        lieu = validate_field(lieu) #verifie qu'on a bien une valeur à l'interieur
    #enlever les espaces et /n indÃ©sirables
    lieu =clean(lieu) 
    print(lieu)

    ###########extraire les compétences necessaire de l'offre
    #TODO verifier que cette formule marche aussi avec d'autre offres. 
    liste ="""jobs-ppc-criteria__value t-14 t-black t-normal ml2 block"""
    competences = sel.xpath('//*[starts-with(@class, "'+liste+'")]/text()').extract()
    competences = validate_field(competences)
    
    if isinstance(competences,list): #si c'est une liste alors on nettoie ce qu'on obtient. 
        for position,competence in enumerate(competences):
            competence = clean(competence)
            competences[position] = competence
    
    print(competences)
    
    
    ######### niveau requis pour le poste
    #TODO verifie pourqoui ca ne marche pas ici
    niveau = sel.xpath('//*[starts-with(@class, "jobs-description-details__list-item t-14")]/text()').extract()
    for record in niveau: 
        print(record.xpath('//p').extract())
    
    niveau  = validate_field(niveau)
    #enlever les espaces et /n indÃ©sirables
    niveau =clean(niveau)
    print(niveau)

    #TODO extraire aussi le secteur, le type d'emploi et la fonction. 
    
    #extraire le texte concernant les informations de l'offre
    #TODO regarder si on peut aussi extraire les informations de cette entreprise
    liste ="jobs-box__html-content jobs-description-content__text t-14 t-normal"
    titre = sel.xpath('//*[starts-with(@class, "'+liste+'")]/text()').extract()
    titre = validate_field(titre)
    #enlever les espaces et /n indÃ©sirables
    titre=clean(titre)
    print(titre)

driver.get('https://www.google.com')
driver.find_element_by_name('q')
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
