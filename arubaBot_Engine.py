# coding: utf-8


##################################################
#       Serigne Saliou Khadim LEYE
#       HPE Aruba France SE Apprentice
##################################################


##################
import myFunctions
##################


import json
from flask import Flask, request
from random import randint


monAPP = Flask(__name__)
monAPP.debug = True

@monAPP.route('/dialogflow_webhook', methods=["GET", "POST"])
def traitement():
    if request.method == "POST":
        ############################################
        #
        #   Traitement données issues de dialogflow
        #
        ############################################
        dialogflow_data = request.get_json()
        #Extraction des paramètres qui nous intérressent (saisis du user depuis dialogflow) pour créer le compte guest
        parameters = myFunctions.extract_DialogFlow_Parameters(dialogflow_data)
        #
        ############################################
        #
        #   Use Cas 1 : Création d'un compte guest
        #
        ############################################
        if parameters['operation']=="create_guest_account":
            #
            guest_parameters = myFunctions.extract_DialogFlow_GuestUser_Parameters(parameters)
            #préparation des paramètres de création du compte guest
            visitorAccount_data = myFunctions.Build_GuestUser_Data(guest_parameters)
            #
            base_url = "https://app1-apigw.central.arubanetworks.com"
            atoken = myFunctions.get_Token(base_url)
            guestPortalName = "Central-Captive-Portal"
            #
            temp1 = myFunctions.get_GuestPortals(base_url, atoken)
            temp1 = myFunctions.extract_GuestPortals_AuthType_UsrPwd(temp1)
            temp1 = myFunctions.filter_GuestPortal_By_Name(temp1, guestPortalName)
            #
            portal_id = myFunctions.extract_Id_GuestPortal(temp1)
            #
            myFunctions.post_visitor(base_url, atoken, portal_id, visitorAccount_data)
            #
        ############################################
        #
        #   Use Cas 2 : Allumer le WIFI
        #
        ############################################
        if parameters['operation']=="enable_wifi":
            #
            base_url = "https://app1-apigw.central.arubanetworks.com"
            atoken = myFunctions.get_Token(base_url)
            device_serial = "BX0126370"
            device_mac = "18:64:72:c6:e7:52"
            #
            myFunctions.allumer_wifi (base_url, atoken, device_serial, device_mac)
            #
        ############################################
        #
        #   Use Cas 3 : Eteindre le WIFI
        #
        ############################################
        if parameters['operation']=="disable_wifi":
            #
            base_url = "https://app1-apigw.central.arubanetworks.com"
            atoken = myFunctions.get_Token(base_url)
            device_serial = "BX0126370"
            device_mac = "18:64:72:c6:e7:52"
            #
            myFunctions.eteindre_wifi (base_url, atoken, device_serial, device_mac)
            #
        #############################
        #
        #   La réponse à la requête
        #
        #############################
        response = {}
        response['msg'] = "Opération réussie ;)"
        response['path'] = request.path
        response['request_type'] = request.method
        return json.dumps(response)


if __name__ == '__main__' :
    monAPP.run(host='0.0.0.0', port=1994)