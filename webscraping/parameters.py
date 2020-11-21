""" filename: parameters.py """

# requete de recherche 
search_query = 'site:linkedin.com/in/ AND "python developer" AND "London"'

# dossier où les resulats scrapés seront stockés 
file_name = 'liste_offres.csv'

# login et pasword
linkedin_username = 'loicyng@gmail.com'
linkedin_password = ')Yq^-9MFMQ2hb=A'
import random

def hard_skills(n):
    skills_liste= []
    liste= random.sample(range(0,len(skills_liste)), n)
    skills= []
    for k in liste: 
        skills.append(skills_liste[k])
    return skills


def soft_skills(n):
   skills_liste = ['confiance','empathie','communication','entrepreneur','audace','motivé',
                   'curieux','adaptabilité','assertivité','autonome','conscient','coopératif',
                   'créatif','profesionnel','négociateur','optimiste','perséverant','résilient','rigoureux'] 
   liste = random.sample(range(0,len(skills_liste)),n)
   skills= []
   for k in liste:
       skills.append(skills_liste[k])
   return skills