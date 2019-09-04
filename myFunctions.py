# coding: utf-8

#Serigne Saliou Khadim LEYE
#HPE Aruba SE Apprentice

#####################################################################################
#
#Script regroupant un ensemble de fonctions pour les appels API vers Aruba Central
#
#####################################################################################


import json
import requests
from flask import Flask, request
from random import randint


def main():
    base_url = "https://app1-apigw.central.arubanetworks.com"


######################################################################################
#
#Fonction permettant de s'authentifier et de récupérer une paire access/refresh Token
#
######################################################################################
def get_Token(base_url):
    #définition des paramètres
    customerid = "8012831"
    clientid = "gsUo6zGitTjdIbT70cYWu6zbKY3EsWTo"
    clientsecret = "6Q35IOGSGB7NwLUh2XBGpneVMerUFiDn"
    username = "showroomhpe.lesulis@gmail.com"
    password = "HPEAruba2019$"
    #définition des différents url utilisés dans les différentes étapes de l'authentification
    url1 = "/oauth2/authorize/central/api/login"
    url2 = "/oauth2/authorize/central/api"
    url3 = "/oauth2/token"
    #construction des urls utilisés dans les requettes
    authurl = base_url + url1
    authcodeurl = base_url + url2
    #les paramètres de la requette
    params = {"client_id": clientid}
    headers = {'Content-type': 'application/json'}
    payload = {"username": username, "password": password}
    #authentification en 3 phases
    resp = requests.post(authurl, params=params, data=json.dumps(payload), headers=headers)
    csrf = resp.cookies['csrftoken']
    ses = resp.cookies['session']
    #
    if resp.status_code != 200:
        print("Failure! The code is: {}".format(resp.status_code))
    else:
        print("\n")
    #
    sesk = "session=" + ses
    #
    headers2 = {}
    headers2 = {
        'X-CSRF-TOKEN': csrf,
        'Content-type': 'application/json',
        'Cookie': sesk
    }
    #
    payload2 = {"customer_id": customerid}
    params2 = {"client_id": clientid, "response_type": "code", "scope": "all"}
    resp = requests.post(authcodeurl, params=params2, data=json.dumps(payload2), headers=headers2)
    authcode = resp.json()['auth_code']
    #
    swapurl = base_url + url3
    params3 = {"client_id": clientid, "grant_type": "authorization_code", "client_secret": clientsecret, "code": authcode}
    resp = requests.post(swapurl, params=params3)
    #récupération des Tokens access & refresh
    rtoken = resp.json()['refresh_token']
    atoken = resp.json()['access_token']
    print("\nCongrats!\nAccess Token is:{}\nRefresh Token is:{}\nThese are valid for 2 hours only!".format(atoken, rtoken))
    #
    return atoken



#####################################################################################################
#
#Fonction permettant de retourner la liste de l'ensemble des portails guests crées dans Aruba Central
#
#####################################################################################################
def get_GuestPortals(base_url, atoken):
    #construction de l'url utilisé dans les requettes
    url1 = "/guest/v1/portals"
    url2 = base_url + url1
    #les paramètres de la requette
    params = {"access_token": atoken, "sort": "+name", "offset": "0", "limit": "20"}
    # Récupération de la reponse de la requette
    resp = requests.get(url2, params=params)
    # Vérification si la requette s'est correctement effectuée
    if resp.status_code != 200:
        print("Something went bad {} {}".format(resp.status_code, resp.text))
    else:
        print("\n")
    # Formatage de la réponse en un dictionnaire appelé "jsonobj"
    jsonobj = resp.json()
    # Extraction de la liste des portails dans une variable de type liste appelée "list_guestPortals"
    list_GuestPortals = jsonobj['portals']
    return list_GuestPortals



####################################################################################################################################
#
#Fonction permettant d'extraire parmis une liste de guestPortals, ceux qui sont en "auth_type": "Username/Password" et les retourner
#
####################################################################################################################################
def extract_GuestPortals_AuthType_UsrPwd(list_GuestPortals):
    #Variable de récupération des portals dans une liste appelée "guestPortals"
    guestPortals = []
    #Vérification si le portail est en "auth_type": "Username/Password" et si oui, alors l'ajouter à la liste
    for element in list_GuestPortals:
        if element['auth_type']=="Username/Password":
            guestPortals.append(element)
    #print(guestPortals)
    return guestPortals



#############################################################################################################
#
#Fonction permettant d'extraire et retourner les IDs des guestPortals présent dans une liste de guestPortals
#
#############################################################################################################
def extract_Ids_GuestPortals(list_GuestPortals):
    #Variable de récupération des portals ID dans une liste appelée "guestPortalsId"
    guestPortalsId = []
    for element in list_GuestPortals:
        guestPortalsId.append(element['id'])
    #print(guestPortalssId)
    return guestPortalsId


#########################################################################################
#
#Fonction permettant d'extraire et de retourner l'id d'un guestPortal donné en paramètre
#
#########################################################################################
def extract_Id_GuestPortal(guestPortal):
    #récupération de l'id du portail guest
    guestPortalId = guestPortal['id']
    #print(guestPortalId)
    return guestPortalId



###############################################################
#
#Fonction permettant de filtrer un guestPortal grâce à son nom
#
###############################################################
def filter_GuestPortal_By_Name(list_GuestPortals, guestPortalName):
    #Variable de récupération du portail guest recherché
    guestPortal = {}
    #Parcourir la liste des portails (donner en paramètre pour matcher le name rentré en paramètre de la fonction
    for element in list_GuestPortals:
        if element['name']==guestPortalName:
            guestPortal = element
    #print(guestPortal)
    return guestPortal


############################################################################################
#
#Fonction permettant de retourner la liste des comptes visitors crées pour un portail donné
#
############################################################################################
def get_Visitors(base_url, atoken, portal_id):
    #construction de l'url utilisé dans les requettes
    url1 = "/guest/v1/portals/"+portal_id+"/visitors"
    url2 = base_url + url1
    #les paramètres de la requette
    params = {"access_token": atoken, "sort": "+name", "offset": "0", "limit": "20", "portal_id": portal_id}
    # Récupération reponse de la requette
    resp = requests.get(url2, params=params)
    # Vérification si la requette s'est correctement effectuée
    if resp.status_code != 200:
        print("Something went bad {} {}".format(resp.status_code, resp.text))
    else:
        print("\n")
    # Formatage de la réponse dans un dictionnaire appelé "jsonobj"
    jsonobj = resp.json()
    # Extraction de la liste des visitors dans une variable de type liste appelée "list_visitors"
    list_Visitors = jsonobj['visitors']
    #print(list_Visitors)
    return list_Visitors



#######################################################################################
#
#Fonction permettant de filtrer un visitor parmis une liste de visitor grace à son nom
#
#######################################################################################
def filter_Visitor_By_Name(list_Visitors, visitorName):
    #Variable de récupération du visitor
    visitor = {}
    #Parcourir la liste des visitors (donner en paramètre pour matcher le name rentré en paramètre de la fonction
    for element in list_Visitors:
        if element['name']==visitorName:
            visitor = element
    #print(visitor)
    return visitor



#########################################################################################
#
#Fonction permettant de retourner une liste des noms de visitors d'une liste de visitors
#
#########################################################################################
def extract_Name_Visitors(list_Visitors):
    #Variable de récupération des noms des visitors dans une liste appelée "visitorsName"
    visitorsName = []
    for element in list_Visitors:
        visitorsName.append(element['name'])
    #print(visitorsName)
    return visitorsName



##############################################################################
#
#Fonction permettant de créer un compte guest visitor pour un portal id donné
#
##############################################################################
def post_visitor(base_url, atoken, portal_id, data):
    #IL Faut vérifier que le portail ayant pour id "portal_id" soit en "auth_type": "Username/Password"
    #data est la donnée à envoyer dans la requette post. Aller dans le swagger tool pour en savoir plus
    #construction de l'url utilisé dans les requettes
    url1 = "/guest/v1/portals/"+portal_id+"/visitors"
    url2 = base_url + url1
    #les paramètres de la requette
    params = {"access_token": atoken, "portal_id": portal_id}
    #la donnée à envoyer dans le post
    #formatage de la donnée en format json
    data = json.dumps(data)
    #récapitulation de la donnée à envoyer
    print("Sending..", type(data), data)
    #L'entête de la requete post
    headers = {'content-type': 'application/json'}
    # Envoie de la requette et stockage de la réponse dans la variable "resp"
    resp = requests.post(url2, params=params, data=data, headers=headers)
    # Vérification si la requette s'est correctement effectuée
    if (resp.status_code == 200) or (resp.status_code == 201):
        #print("Success! The code is: {}".format(resp.status_code))
        print("\n")
    else:
        print("Failure! The code is: {}".format(resp.status_code))

    return



############################################################
#
#Fonction permettant d'extraire depuis les paramètres de la requête dialogflow
#
############################################################
def extract_DialogFlow_Parameters(dialogflow_data):
    #Créer un dictionnaire pour récupérer les données
    parameters = dialogflow_data['queryResult']['parameters']

    return parameters




############################################################
#
#Fonction permettant d'extraire depuis les input de dialogflow les données du compte guest à créer
#
############################################################
def extract_DialogFlow_GuestUser_Parameters(data):
    #Créer un dictionnaire pour récupérer les données
    parameters = {}
    #Récupération du nom du portail guest
    #parameters['portal_name'] = enlever_prem_caract(dialogflow_data['queryResult']['parameters']['portal_name'])
    #Récupération du mot de passe du compte guest
    #parameters['password'] = enlever_prem_caract(dialogflow_data['queryResult']['parameters']['password'])
    #Réupération de l'e-mail du compte guest
    parameters['email'] = data['email']
    #Récupération du numéro de tél du compte guest
    parameters['phone-number'] = data['phone-number']

    return parameters



##############################################################
#
#Fonction permettant de retourner un dictionnaire avec les données du user à envoyer dans la requete de création du compte guest
#
##############################################################
def Build_GuestUser_Data(parameters):
    #Création d'un dictionnaire avec les données du user à envoyer dans la requete de création du compte guest
    visitorAccount_data = {
        "name": "guest"+str(randint(1000,9999)),
        "company_name": "HPE Aruba",
        "user": {
            "phone": parameters['phone-number'],
            "email": parameters['email']
        },
        "is_enabled": True,
        "valid_till_no_limit": False,
        "valid_till_days": 1,
        #Notify the user that his account has been created and give him the credentials
        "notify": True,
        #Notify to "phone" using phone number or "email" using email address
        "notify_to": "phone",
        "password": "aruba_"+str(randint(100000,999999))
    }
    return visitorAccount_data




##############################################################
#
#Fonction permettant d'enlever le premier caractère d'une chaine de caractère
#Car Dialogflow envoie des caractère du genre [mot de passe
#Donc il faut supprimer le "["
#
##############################################################
def enlever_prem_caract(chaine_caracteres):

    nouvelle_chaine = chaine_caracteres[1:len(chaine_caracteres)]

    return nouvelle_chaine






##############################################################
#
#Fonction permettant d'allumer le wifi internal
#
##############################################################
def allumer_wifi (base_url, atoken, device_serial, device_mac):
    #variables to be updated
    data = {
        "variables": {
            "_sys_lan_mac": ""+device_mac+"",
            "enable_ssid_internal": "yes"
        }
    }
    #Construction de l'URL de la requete
    url1 = "/configuration/v1/devices/"+device_serial+"/template_variables"
    url2 = base_url + url1
    #les paramètres de la requette
    params = {"access_token": atoken, "device_serial": device_serial}
    #la donnée à envoyer dans le post
    #formatage de la donnée en format json
    data = json.dumps(data)
    #récapitulation de la donnée à envoyer
    print("Sending..", type(data), data)
    #L'entête de la requete post
    headers = {'content-type': 'application/json'}
    #Envoie de la requette et stockage de la réponse dans la variable "resp"
    resp = requests.patch(url2, params=params, data=data, headers=headers)
    # Vérification si la requette s'est correctement effectuée
    if (resp.status_code == 200) or (resp.status_code == 201):
        #print("Success! The code is: {}".format(resp.status_code))
        print("\n")
    else:
        print("Failure! The code is: {}".format(resp.status_code))
    return





##############################################################
#
#Fonction permettant d'éteindre le wifi internal
#
##############################################################
def eteindre_wifi (base_url, atoken, device_serial, device_mac):
    #variables to be updated
    data = {
        "variables": {
            "_sys_lan_mac": ""+device_mac+"",
            "enable_ssid_internal": "no"
        }
    }
    #Construction de l'URL de la requete
    url1 = "/configuration/v1/devices/"+device_serial+"/template_variables"
    url2 = base_url + url1
    #les paramètres de la requette
    params = {"access_token": atoken, "device_serial": device_serial}
    #la donnée à envoyer dans le post
    #formatage de la donnée en format json
    data = json.dumps(data)
    #récapitulation de la donnée à envoyer
    print("Sending..", type(data), data)
    #L'entête de la requete post
    headers = {'content-type': 'application/json'}
    #Envoie de la requette et stockage de la réponse dans la variable "resp"
    resp = requests.patch(url2, params=params, data=data, headers=headers)
    # Vérification si la requette s'est correctement effectuée
    if (resp.status_code == 200) or (resp.status_code == 201):
        #print("Success! The code is: {}".format(resp.status_code))
        print("\n")
    else:
        print("Failure! The code is: {}".format(resp.status_code))
    return
