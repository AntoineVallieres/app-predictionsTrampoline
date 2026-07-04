import streamlit as st
import pandas as pd
import json
import gspread
import math
from google.oauth2.service_account import Credentials

# --- ÉTAPE A : LE DICTIONNAIRE DE TRADUCTIONS ---
TEXTS = {
    'Français': {
        'APP_TITLE': "🤸 Prédictions de l'équipe",
        'SIDEBAR_LANG_LABEL': "🌐 Langue / Language :",
        'NAVI_LABEL': "Navigation",
        'NAVI_PREDICT': "Faire une prédiction",
        'NAVI_VIEW_PREDICTS': "Voir les prédictions",
        'NAVI_GLOBAL_RANKING': "🏆 Classement Général",
        'NAVI_COACH': "Zone Admin",
        'WELCOME_MSG_TITLE': "👋 Bienvenue !",
        'WELCOME_MSG_COACH_ACTION': "Veuillez aller dans la 'Zone Admin' pour créer votre premier événement.",
        'CHOOSE_EVENT_LABEL': "Choisir l'épreuve :",
        'CHOOSE_COMPETITION_LABEL': "Sélectionnez la compétition (6 premiers caractères) :",
        'NAVI_SUB_GO': "Aller à :",
        'SUB_PREDICT_TITLE': "Fais tes choix",
        'INPUT_NAME_LABEL': "Quel est ton nom?",
        'INPUT_FIN_RANK_LABEL': "Rang pour",
        'BTN_LOAD_DRAFT': "📂 Charger mes choix précédents",
        'BTN_SAVE_DRAFT': "💾 Sauvegarder comme brouillon",
        'SUCCESS_DRAFT_RECORDED': "✅ Brouillon sauvegardé pour {0} ! (Invisible aux autres)",
        'ERR_PREDICT_INVALID_FINALE': "Prédiction invalide (tous les rangs doivent être remplis sans doublons).",
        'BTN_CONFIRM_PREDICT': "SOUMETTRE VERSION FINALE",
        'ERR_NO_NAME': "N'oublie pas d'inscrire ton nom!",
        'ERR_PREDICT_INCOMPLETE': "Tu dois assigner une position à TOUS les athlètes.",
        'ERR_PREDICT_DUPLICATE_RANK': "Tu as donné la même position à plus d'un athlète.",
        'SUCCESS_PREDICT_RECORDED': "✅ Tes prédictions finales sont enregistrées, {0}!",
        'MULTISELECT_QUALIF_LABEL': "Sélectionne tes {0} qualifiés en cochant les noms :",
        'ERR_NOT_N_SELECTED': "Tu dois sélectionner EXACTEMENT {0} athlètes.",
        'LABEL_SELECTED': "Sélectionnés",
        'SUB_VIEW_TITLE': "📊 Tableau des prédictions",
        'INFO_RESULTS_ENTERED': "Les résultats officiels sont entrés ! Compare les choix avec la première colonne.",
        'TABLE_PREDICTS_COL_TRUE_RESULT': "🏆 RÉSULTAT",
        'TABLE_PREDICTS_COL_RANK': "Rang / Choix",
        'INFO_NO_PREDICTS': "Aucune prédiction finale pour le moment.",
        'LEGEND_RESULTS': "**Légende des couleurs :**\n* 🟢 Vert : Position exacte (Finale) ou Qualifié trouvé (Qualif)\n* 🟡 Jaune : Dans le vrai Top 3 mais mauvaise position (Finale)\n* 🔴 Rouge : Mauvais choix / Mauvaise position",
        'LEGEND_UNANIMOUS': "⚪ **Légende :** Les cases grises indiquent les athlètes choisis par *absolument tous* les participants du groupe.",
        'SUB_COACH_TITLE': "🔒 Zone d'administration",
        'COACH_LOGIN_TEXT': "Cette zone est réservée à l'administrateur.",
        'INPUT_PWD_LABEL': "Mot de passe :",
        'BTN_UNLOCK': "Déverrouiller",
        'ERR_WRONG_PWD': "Mot de passe incorrect.",
        'BTN_LOGOUT': "Se déconnecter (Verrouiller)",
        'COACH_ACTION_LABEL': "Action :",
        'ACTION_CREATE_EVENT': "Créer une nouvelle épreuve",
        'ACTION_RENAME_EVENT': "Renommer l'épreuve",
        'ACTION_EDIT_FIN': "Modifier la liste de départ",
        'ACTION_REPLACE_ATHLETE': "Remplacer un athlète",
        'ACTION_EDIT_PARTICIPANT_NAME': "Modifier le nom d'un participant",
        'ACTION_MODIF_PREDICT': "Modifier une prédiction",
        'ACTION_DEL_PREDICT': "Supprimer une prédiction",
        'ACTION_MODIF_NB_QUALIF': "Modifier le nombre de qualifiés",
        'ACTION_ENTER_RESULTS': "Entrer les résultats et calculer",
        'ACTION_MANAGE_ARCHIVES': "Gérer / Archiver les épreuves",
        'SUB_CREATE_EVENT': "➕ Ajouter une compétition",
        'INPUT_NEW_EVENT_NAME': "Nom de l'épreuve",
        'EVENT_TYPE_LABEL': "Type d'épreuve :",
        'TYPE_FINALE': "Finale (Classer de 1 à 8)",
        'TYPE_QUALIF': "Ronde de qualification (Trouver les qualifiés)",
        'INPUT_NB_QUALIFIES': "Nombre d'athlètes qui passent à la ronde suivante :",
        'BTN_CREATE_EVENT': "Créer l'épreuve",
        'SUCCESS_EVENT_CREATED': "L'épreuve a été créée ! Rends-toi dans 'Modifier la liste de départ'.",
        'ERR_EVENT_EXISTS': "Une épreuve porte déjà ce nom.",
        'SUB_RENAME_EVENT': "✏️ Renommer l'épreuve",
        'INPUT_NEW_NAME_EV': "Nouveau nom :",
        'BTN_CONFIRM_RENAME': "Confirmer le nouveau nom",
        'SUCCESS_RENAMED': "L'épreuve a été renommée avec succès !",
        'SUB_EDIT_FIN': "📝 Liste de départ pour",
        'INPUT_ATHLETES_AREA': "Copie/Colle les noms des athlètes ici (UN ATHLÈTE PAR LIGNE) :",
        'BTN_SAVE_FIN_NAMES': "Sauvegarder la liste",
        'ERR_FIN_NAMES_DUPLICATE': "Assure-toi que tous les noms sont différents.",
        'ERR_NOT_EXACTLY_8': "Pour une finale, tu dois inscrire EXACTEMENT 8 athlètes.",
        'ERR_NOT_ENOUGH_QUALIF': "Pour cette ronde, tu dois inscrire plus de {0} athlètes au total.",
        'SUCCESS_FIN_NAMES_UPDATED': "La liste a été mise à jour !",
        'SUB_EDIT_PART': "👤 Corriger le nom d'un participant",
        'INPUT_SELECT_PART_LABEL': "Sélectionner le participant :",
        'INPUT_NEW_NAME_PART_LABEL': "Nouveau nom :",
        'BTN_MODIFY_PART': "Modifier le nom du participant",
        'SUCCESS_PART_NAME_UPDATED': "Le nom du participant a été corrigé !",
        'ERR_PART_NAME_EXISTS': "Ce nom existe déjà.",
        'INFO_NO_PART_YET': "Aucun participant pour cette épreuve.",
        'SUB_ENTER_RESULTS': "🏆 Résultats officiels pour l'épreuve",
        'INFO_RESULTS_ORDER': "Cochez les athlètes dans leur ordre d'arrivée (du 1er au dernier). **L'ordre de vos clics détermine le classement !**",
        'BTN_CALC_RESULTS': "CALCULER ET APPLIQUER LES COULEURS",
        'ERR_INCOMPLETE_RESULTS': "Remplis les {0} positions.",
        'SUCCESS_RESULTS_SAVED': "Résultats sauvegardés !",
        'CALC_LEADERBOARD_TITLE': "Classement de l'épreuve",
        'CALC_COL_PART': "Participant",
        'CALC_COL_POINTS': "Points de l'épreuve",
        'CALC_COL_WINS': "Victoires (1re position)",
        'BTN_CREATE_NEXT_ROUND': "🔗 Créer la RONDE SUIVANTE avec ces {0} athlètes",
        'SUCCESS_LINKED_FINAL': "La ronde suivante a été créée avec succès !",
        'SUB_MANAGE_ARCHIVES': "🗑️ Nettoyage des événements",
        'INFO_NO_EVENTS_TO_MANAGE': "Aucun événement à gérer.",
        'ARCHIVE_STATUS_LABEL': "Statut actuel :",
        'ARCHIVE_STATUS_ACTIF': "ACTIF",
        'ARCHIVE_STATUS_ARCHIVE': "ARCHIVÉ",
        'COL1_BTN_ARCHIVE': "Dossier jaune : Archiver",
        'COL1_BTN_UNARCHIVE': "Dossier vert : Désarchiver (Réactiver)",
        'SUCCESS_ARCHIVED': "Épreuve archivée !",
        'SUCCESS_UNARCHIVED': "Épreuve réactivée !",
        'COL2_BTN_DELETE_FOREVER': "Dossier rouge : Supprimer DÉFINITIVEMENT",
        'SUCCESS_DELETED': "L'épreuve a été supprimée."
    },
    'English': {
        'APP_TITLE': "🤸 Team Predictions",
        'SIDEBAR_LANG_LABEL': "🌐 Language / Langue :",
        'NAVI_LABEL': "Navigation",
        'NAVI_PREDICT': "Make a prediction",
        'NAVI_VIEW_PREDICTS': "View predictions",
        'NAVI_GLOBAL_RANKING': "🏆 Global Leaderboard",
        'NAVI_COACH': "Admin Zone",
        'WELCOME_MSG_TITLE': "👋 Welcome!",
        'WELCOME_MSG_COACH_ACTION': "Please go to the 'Admin Zone' to create your first event.",
        'CHOOSE_EVENT_LABEL': "Choose the event:",
        'CHOOSE_COMPETITION_LABEL': "Select competition (first 6 chars):",
        'NAVI_SUB_GO': "Go to:",
        'SUB_PREDICT_TITLE': "Make your choices",
        'INPUT_NAME_LABEL': "What is your name?",
        'INPUT_FIN_RANK_LABEL': "Rank for",
        'BTN_LOAD_DRAFT': "📂 Load my previous choices",
        'BTN_SAVE_DRAFT': "💾 Save as draft",
        'SUCCESS_DRAFT_RECORDED': "✅ Draft saved for {0}! (Hidden from others)",
        'ERR_PREDICT_INVALID_FINALE': "Invalid prediction (must fill all ranks uniquely).",
        'BTN_CONFIRM_PREDICT': "SUBMIT FINAL VERSION",
        'ERR_NO_NAME': "Don't forget to enter your name!",
        'ERR_PREDICT_INCOMPLETE': "You must assign a position to ALL athletes.",
        'ERR_PREDICT_DUPLICATE_RANK': "You have given the same position to more than one athlete.",
        'SUCCESS_PREDICT_RECORDED': "✅ Your final predictions are recorded, {0}!",
        'MULTISELECT_QUALIF_LABEL': "Select your {0} qualifiers by checking the names:",
        'ERR_NOT_N_SELECTED': "You must select EXACTLY {0} athletes.",
        'LABEL_SELECTED': "Selected",
        'SUB_VIEW_TITLE': "📊 Prediction Leaderboard",
        'INFO_RESULTS_ENTERED': "Official results are in! Compare choices with the first column.",
        'TABLE_PREDICTS_COL_TRUE_RESULT': "🏆 RESULTS",
        'TABLE_PREDICTS_COL_RANK': "Rank / Choice",
        'INFO_NO_PREDICTS': "No final predictions have been made yet.",
        'LEGEND_RESULTS': "**Color Legend:**\n* 🟢 Green: Exact position (Final) or Qualifier found (Qualif)\n* 🟡 Yellow: In the real Top 3 but wrong position (Final)\n* 🔴 Red: Wrong choice / Wrong position",
        'LEGEND_UNANIMOUS': "⚪ **Legend:** Gray cells indicate athletes chosen by *absolutely everyone* in the group.",
        'SUB_COACH_TITLE': "🔒 Admin Area",
        'COACH_LOGIN_TEXT': "This zone is for the admin only.",
        'INPUT_PWD_LABEL': "Password:",
        'BTN_UNLOCK': "Unlock",
        'ERR_WRONG_PWD': "Incorrect password.",
        'BTN_LOGOUT': "Log out (Lock)",
        'COACH_ACTION_LABEL': "Action:",
        'ACTION_CREATE_EVENT': "Create a new event",
        'ACTION_RENAME_EVENT': "Rename event",
        'ACTION_EDIT_FIN': "Edit start list",
        'ACTION_REPLACE_ATHLETE': "Replace an athlete",
        'ACTION_EDIT_PARTICIPANT_NAME': "Edit a participant's name",
        'ACTION_MODIF_PREDICT': "Modify a prediction",
        'ACTION_DEL_PREDICT': "Delete a prediction",
        'ACTION_MODIF_NB_QUALIF': "Modify the number of qualifiers",
        'ACTION_ENTER_RESULTS': "Enter results and calculate",
        'ACTION_MANAGE_ARCHIVES': "Manage / Archive events",
        'SUB_CREATE_EVENT': "➕ Add an event",
        'INPUT_NEW_EVENT_NAME': "Event name",
        'EVENT_TYPE_LABEL': "Event Type:",
        'TYPE_FINALE': "Final (Rank 1 to 8)",
        'TYPE_QUALIF': "Qualification round (Find the qualifiers)",
        'INPUT_NB_QUALIFIES': "Number of athletes advancing to the next round:",
        'BTN_CREATE_EVENT': "Create event",
        'SUCCESS_EVENT_CREATED': "Event created! Go to 'Edit start list'.",
        'ERR_EVENT_EXISTS': "An event already has this name.",
        'SUB_RENAME_EVENT': "✏️ Rename event",
        'INPUT_NEW_NAME_EV': "New name:",
        'BTN_CONFIRM_RENAME': "Confirm new name",
        'SUCCESS_RENAMED': "Event renamed successfully!",
        'SUB_EDIT_FIN': "📝 Start list for",
        'INPUT_ATHLETES_AREA': "Copy/Paste athlete names here (ONE ATHLETE PER LINE):",
        'BTN_SAVE_FIN_NAMES': "Save list",
        'ERR_FIN_NAMES_DUPLICATE': "Ensure all names are different.",
        'ERR_NOT_EXACTLY_8': "For a final, you must enter EXACTLY 8 athletes.",
        'ERR_NOT_ENOUGH_QUALIF': "For this round, you must enter more than {0} athletes in total.",
        'SUCCESS_FIN_NAMES_UPDATED': "List has been updated!",
        'SUB_EDIT_PART': "👤 Correct participant name",
        'INPUT_SELECT_PART_LABEL': "Select participant:",
        'INPUT_NEW_NAME_PART_LABEL': "New name:",
        'BTN_MODIFY_PART': "Modify name",
        'SUCCESS_PART_NAME_UPDATED': "Participant name corrected!",
        'ERR_PART_NAME_EXISTS': "Name already exists.",
        'INFO_NO_PART_YET': "No participant yet.",
        'SUB_ENTER_RESULTS': "🏆 Official results for",
        'INFO_RESULTS_ORDER': "Check the athletes in their exact finishing order (from 1st to last). **The order of your clicks determines the ranking!**",
        'BTN_CALC_RESULTS': "CALCULATE AND APPLY COLORS",
        'ERR_INCOMPLETE_RESULTS': "Fill all {0} positions.",
        'SUCCESS_RESULTS_SAVED': "Results saved!",
        'CALC_LEADERBOARD_TITLE': "Event Leaderboard",
        'CALC_COL_PART': "Participant",
        'CALC_COL_POINTS': "Event Points",
        'CALC_COL_WINS': "Wins (1st Place finishes)",
        'BTN_CREATE_NEXT_ROUND': "🔗 Create NEXT ROUND with these {0} athletes",
        'SUCCESS_LINKED_FINAL': "Next round successfully created!",
        'SUB_MANAGE_ARCHIVES': "🗑️ Event Management",
        'INFO_NO_EVENTS_TO_MANAGE': "No events to manage.",
        'ARCHIVE_STATUS_LABEL': "Current status:",
        'ARCHIVE_STATUS_ACTIF': "ACTIVE",
        'ARCHIVE_STATUS_ARCHIVE': "ARCHIVED",
        'COL1_BTN_ARCHIVE': "Yellow Folder: Archive",
        'COL1_BTN_UNARCHIVE': "Green Folder: Unarchive (Reactive)",
        'SUCCESS_ARCHIVED': "Event archived!",
        'SUCCESS_UNARCHIVED': "Event reactivated!",
        'COL2_BTN_DELETE_FOREVER': "Red Folder: Delete FOREVER",
        'SUCCESS_DELETED': "Event deleted forever."
    }
}

st.set_page_config(page_title="Team Predictions", page_icon="🤸", layout="wide")

st.sidebar.markdown(f"**{TEXTS['Français']['SIDEBAR_LANG_LABEL']}**")
selected_lang = st.sidebar.selectbox("", options=['Français', 'English'], label_visibility="collapsed")
t = TEXTS[selected_lang]
st.markdown(f"<script>document.title = '{t['APP_TITLE']}'</script>", unsafe_allow_html=True)


# --- CONNEXION À GOOGLE SHEETS ---
def get_sheet():
    creds_json = st.secrets["google_json"]
    creds_dict = json.loads(creds_json)
    credentials = Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    gc = gspread.authorize(credentials)
    sh = gc.open("BaseDeDonnees_Trampoline")
    return sh.sheet1

def charger_donnees():
    try:
        sheet = get_sheet()
        valeur = sheet.acell('A1').value
        if valeur:
            donnees = json.loads(valeur)
            for ev_nom, ev_data in donnees.items():
                if "statut" not in ev_data: ev_data["statut"] = "actif"
                if "vrais_resultats" not in ev_data: ev_data["vrais_resultats"] = None
                if "type" not in ev_data: ev_data["type"] = "finale"
                if ev_data["type"] == "demi-finale": ev_data["type"] = "qualif"
                if "nb_qualifies" not in ev_data: ev_data["nb_qualifies"] = 8
                if "predictions" in ev_data:
                    for p_nom, p_val in ev_data["predictions"].items():
                        if not isinstance(p_val, dict) or "choix" not in p_val:
                            ev_data["predictions"][p_nom] = {"choix": p_val, "brouillon": False}
            return donnees
    except Exception as e:
        pass
    return {}

def sauvegarder_donnees():
    try:
        sheet = get_sheet()
        donnees_json = json.dumps(st.session_state.evenements, ensure_ascii=False)
        sheet.update_acell('A1', donnees_json)
    except Exception as e:
        st.error(f"Erreur de sauvegarde Cloud : {e}")

if 'evenements' not in st.session_state:
    st.session_state.evenements = charger_donnees()
if 'coach_authentifie' not in st.session_state:
    st.session_state.coach_authentifie = False

st.title(t['APP_TITLE'])

st.sidebar.markdown("---")
st.sidebar.header(t['NAVI_LABEL'])
liste_evenements_actifs = sorted([ev for ev, data in st.session_state.evenements.items() if data.get("statut", "actif") == "actif"])

if not liste_evenements_actifs:
    st.sidebar.info(t['WELCOME_MSG_COACH_ACTION'])
    evenement_actif = None
    choix = t['NAVI_COACH']
else:
    # On ajoute le classement global au menu
    choix = st.sidebar.radio(t['NAVI_SUB_GO'], [t['NAVI_PREDICT'], t['NAVI_VIEW_PREDICTS'], t['NAVI_GLOBAL_RANKING'], t['NAVI_COACH']])
    if choix != t['NAVI_GLOBAL_RANKING']:
        evenement_actif = st.sidebar.selectbox(t['CHOOSE_EVENT_LABEL'], liste_evenements_actifs)
    else:
        evenement_actif = None

st.write("---")

# =========================================================
# SECTION 1 : FAIRE UNE PRÉDICTION
# =========================================================
if evenement_actif and choix == t['NAVI_PREDICT']:
    st.header(f"{t['SUB_PREDICT_TITLE']} : {evenement_actif}")
    nom_athlete = st.text_input(t['INPUT_NAME_LABEL'])
    
    ev_type = st.session_state.evenements[evenement_actif].get("type", "finale")
    finalistes_actuels = sorted(st.session_state.evenements[evenement_actif]["finalistes"])
    predictions_actuelles = st.session_state.evenements[evenement_actif]["predictions"]
    
    if nom_athlete and nom_athlete in predictions_actuelles:
        if st.button(t['BTN_LOAD_DRAFT']):
            choix_existants = predictions_actuelles[nom_athlete]["choix"]
            if ev_type == "qualif":
                for ath in finalistes_actuels:
                    st.session_state[f"chk_{evenement_actif}_{ath}"] = (ath in choix_existants)
            elif ev_type == "finale":
                for ath in finalistes_actuels:
                    if ath in choix_existants:
                        st.session_state[f"sel_{evenement_actif}_{ath}"] = choix_existants[ath]
    
    st.write("---")
    dict_choix = {}
    is_valid = False
    nb_q = 8

    if ev_type == "finale":
        for i in range(0, len(finalistes_actuels), 2):
            cols = st.columns(2)
            with cols[0]:
                ath1 = finalistes_actuels[i]
                dict_choix[ath1] = st.selectbox(f"{t['INPUT_FIN_RANK_LABEL']} {ath1}", options=[None, 1, 2, 3, 4, 5, 6, 7, 8], key=f"sel_{evenement_actif}_{ath1}")
            if i + 1 < len(finalistes_actuels):
                with cols[1]:
                    ath2 = finalistes_actuels[i+1]
                    dict_choix[ath2] = st.selectbox(f"{t['INPUT_FIN_RANK_LABEL']} {ath2}", options=[None, 1, 2, 3, 4, 5, 6, 7, 8], key=f"sel_{evenement_actif}_{ath2}")
        
        valeurs = list(dict_choix.values())
        is_valid = (None not in valeurs) and (len(set(valeurs)) == 8)

    elif ev_type == "qualif":
        nb_q = st.session_state.evenements[evenement_actif].get("nb_qualifies", 8)
        st.write(f"**{t['MULTISELECT_QUALIF_LABEL'].format(nb_q)}**")
        
        checked_count = sum([1 for ath in finalistes_actuels if st.session_state.get(f"chk_{evenement_actif}_{ath}", False)])
        
        choix_utilisateur = []
        for i in range(0, len(finalistes_actuels), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(finalistes_actuels):
                    ath = finalistes_actuels[i + j]
                    with cols[j]:
                        is_checked = st.session_state.get(f"chk_{evenement_actif}_{ath}", False)
                        disabled = (checked_count >= nb_q) and not is_checked
                        if st.checkbox(ath, key=f"chk_{evenement_actif}_{ath}", disabled=disabled):
                            choix_utilisateur.append(ath)
                    
        couleur_compteur = "green" if len(choix_utilisateur) == nb_q else "red"
        st.markdown(f"**{t['LABEL_SELECTED']} : <span style='color:{couleur_compteur}'>{len(choix_utilisateur)} / {nb_q}</span>**", unsafe_allow_html=True)
        st.write("") 
        
        dict_choix = {athlete: (i+1) for i, athlete in enumerate(choix_utilisateur)}
        is_valid = (len(choix_utilisateur) == nb_q)

    colA, colB = st.columns(2)
    with colA:
        if st.button(t['BTN_SAVE_DRAFT']):
            if not nom_athlete: st.error(t['ERR_NO_NAME'])
            else:
                st.session_state.evenements[evenement_actif]["predictions"][nom_athlete] = {"choix": dict_choix, "brouillon": True}
                sauvegarder_donnees()
                st.success(t['SUCCESS_DRAFT_RECORDED'].format(nom_athlete))
    
    with colB:
        if st.button(t['BTN_CONFIRM_PREDICT'], type="primary"):
            if not nom_athlete: st.error(t['ERR_NO_NAME'])
            elif not is_valid:
                if ev_type == "finale": st.error(t['ERR_PREDICT_INVALID_FINALE'])
                else: st.error(t['ERR_NOT_N_SELECTED'].format(nb_q))
            else:
                st.session_state.evenements[evenement_actif]["predictions"][nom_athlete] = {"choix": dict_choix, "brouillon": False}
                sauvegarder_donnees()
                st.success(t['SUCCESS_PREDICT_RECORDED'].format(nom_athlete))

# =========================================================
# SECTION 2 : VOIR LES PRÉDICTIONS
# =========================================================
elif evenement_actif and choix == t['NAVI_VIEW_PREDICTS']:
    st.header(f"{t['SUB_VIEW_TITLE']} : {evenement_actif}")
    ev_type = st.session_state.evenements[evenement_actif].get("type", "finale")
    predictions_brutes = st.session_state.evenements[evenement_actif]["predictions"]
    vrais_resultats = st.session_state.evenements[evenement_actif].get("vrais_resultats")
    
    valid_preds = {nom: data["choix"] for nom, data in predictions_brutes.items() if not data.get("brouillon", False)}
    
    if valid_preds:
        affichage_predictions = {}
        for nom, preds in valid_preds.items():
            if ev_type == "finale":
                affichage_predictions[nom] = {rang: athlete for athlete, rang in preds.items()}
            else:
                sorted_preds = sorted(preds.keys())
                affichage_predictions[nom] = {f"Choix {i+1}": athlete for i, athlete in enumerate(sorted_preds)}
            
        df = pd.DataFrame(affichage_predictions)
        df.index.name = t['TABLE_PREDICTS_COL_RANK']
        if ev_type == "finale": df = df.sort_index()

        if vrais_resultats:
            st.info(t['INFO_RESULTS_ENTERED'])
            vrais_resultats_propres = {int(k): v for k, v in vrais_resultats.items()}
            
            if ev_type == "finale":
                colonne_resultats = [vrais_resultats_propres.get(i) for i in df.index]
            else:
                colonne_resultats = sorted(vrais_resultats_propres.values())
                while len(colonne_resultats) < len(df.index): colonne_resultats.append("")
                
            col_true_name = t['TABLE_PREDICTS_COL_TRUE_RESULT']
            df.insert(0, col_true_name, colonne_resultats[:len(df.index)])

            def coloriser_cellules(colonne):
                if colonne.name == col_true_name:
                    return ['font-weight: bold; background-color: #e6e6e6; color: black;'] * len(colonne)
                
                vrais_athletes = {athlete: int(rang) for rang, athlete in vrais_resultats.items()}
                styles = []
                for rang_predit, athlete in colonne.items():
                    if ev_type == "finale":
                        rang_vrai = vrais_athletes.get(athlete)
                        if rang_vrai == int(rang_predit): styles.append('background-color: rgba(76, 175, 80, 0.4); color: black;')
                        elif int(rang_predit) <= 3 and rang_vrai and rang_vrai <= 3: styles.append('background-color: rgba(255, 235, 59, 0.4); color: black;')
                        else: styles.append('background-color: rgba(244, 67, 54, 0.4); color: black;')
                    elif ev_type == "qualif":
                        if athlete in vrais_athletes: styles.append('background-color: rgba(76, 175, 80, 0.4); color: black;')
                        else: styles.append('background-color: rgba(244, 67, 54, 0.4); color: black;')
                return styles

            st.dataframe(df.style.apply(coloriser_cellules, axis=0), use_container_width=True)
            st.markdown(t['LEGEND_RESULTS'])
            
        else:
            if ev_type == "qualif":
                all_sets = [set(choix.keys()) for choix in valid_preds.values()]
                unanimous = set.intersection(*all_sets) if all_sets else set()
                
                def color_unanimous(colonne):
                    styles = []
                    for val in colonne:
                        if val in unanimous: styles.append('background-color: lightgray; color: black;')
                        else: styles.append('')
                    return styles
                
                st.dataframe(df.style.apply(color_unanimous, axis=0), use_container_width=True)
                if unanimous:
                    st.caption(t['LEGEND_UNANIMOUS'])
            else:
                st.dataframe(df, use_container_width=True)
    else:
        st.info(t['INFO_NO_PREDICTS'])

# =========================================================
# SECTION 3 : CLASSEMENT GÉNÉRAL (COMPÉTITION)
# =========================================================
elif choix == t['NAVI_GLOBAL_RANKING']:
    st.header(t['NAVI_GLOBAL_RANKING'])
    
    # Extraire les préfixes (6 premiers caractères) des épreuves actives
    prefixes = sorted(list(set([ev[:8] for ev in st.session_state.evenements.keys() if st.session_state.evenements[ev].get("statut", "actif") == "actif"])))
    
    if prefixes:
        selected_prefix = st.selectbox(t['CHOOSE_COMPETITION_LABEL'], prefixes)
        
        global_scores = {}
        events_counted = 0
        
        for ev_nom, ev_data in st.session_state.evenements.items():
            if ev_data.get("statut", "actif") == "actif" and ev_nom.startswith(selected_prefix) and ev_data.get("vrais_resultats"):
                events_counted += 1
                ev_type = ev_data.get("type", "finale")
                vrais_res = ev_data["vrais_resultats"]
                vrais_res_propres = {int(k): v for k, v in vrais_res.items()}
                vrais_resultats_athlete = {athlete: int(rang) for rang, athlete in vrais_res_propres.items()}
                vrai_top_3 = {vrais_res_propres.get(i) for i in [1, 2, 3] if vrais_res_propres.get(i)}
                vrai_premier = vrais_res_propres.get(1)
                
                scores_ev = {}
                valid_preds = {nom: data["choix"] for nom, data in ev_data["predictions"].items() if not data.get("brouillon", False)}
                
                for nom, choix_athlete in valid_preds.items():
                    score = 0
                    if ev_type == "finale":
                        pred_top_3 = {athl for athl, rang in choix_athlete.items() if rang <= 3}
                        for athl, rang in choix_athlete.items():
                            if vrais_resultats_athlete.get(athl) == rang: score += 1
                        score += len(vrai_top_3.intersection(pred_top_3))
                        if choix_athlete.get(vrai_premier) == 1: score += 1
                    elif ev_type == "qualif":
                        for athl in choix_athlete.keys():
                            if athl in vrais_resultats_athlete: score += 1
                    scores_ev[nom] = score
                
                if scores_ev:
                    max_score = max(scores_ev.values())
                    for nom, score in scores_ev.items():
                        if score == max_score:
                            global_scores[nom] = global_scores.get(nom, 0) + 1
                        else:
                            global_scores[nom] = global_scores.get(nom, 0)
                            
        if events_counted > 0:
            st.write(f"*(Épreuves comptabilisées pour {selected_prefix} : {events_counted})*")
            df_global = pd.DataFrame(list(global_scores.items()), columns=[t['CALC_COL_PART'], t['CALC_COL_WINS']])
            df_global = df_global.sort_values(by=t['CALC_COL_WINS'], ascending=False).reset_index(drop=True)
            df_global.index += 1
            st.dataframe(df_global, use_container_width=True)
        else:
            st.info("Aucun résultat officiel n'a été entré pour les épreuves de cette compétition.")
    else:
        st.info("Aucune compétition n'est disponible pour le moment.")

# =========================================================
# SECTION 4 : ZONE ADMIN
# =========================================================
elif choix == t['NAVI_COACH'] or choix == 'Zone Admin' or choix == "Admin Zone":
    st.header(t['SUB_COACH_TITLE'])
    
    if not st.session_state.coach_authentifie:
        st.write(t['COACH_LOGIN_TEXT'])
        mdp = st.text_input(t['INPUT_PWD_LABEL'], type="password")
        if st.button(t['BTN_UNLOCK']):
            if mdp == "Coach33":
                st.session_state.coach_authentifie = True
                st.rerun()
            else: st.error(t['ERR_WRONG_PWD'])
    else:
        if st.button(t['BTN_LOGOUT']):
            st.session_state.coach_authentifie = False
            st.rerun()
            
        st.write("---")
        action_map = {
            t['ACTION_CREATE_EVENT']: "CREATE", 
            t['ACTION_RENAME_EVENT']: "RENAME",
            t['ACTION_EDIT_FIN']: "EDIT_FIN", 
            t['ACTION_REPLACE_ATHLETE']: "REPLACE_ATHLETE", 
            t['ACTION_EDIT_PARTICIPANT_NAME']: "EDIT_PART",
            t['ACTION_MODIF_PREDICT']: "MODIF_PREDICT",
            t['ACTION_DEL_PREDICT']: "DEL_PREDICT", 
            t['ACTION_MODIF_NB_QUALIF']: "MODIF_NB_QUALIF", 
            t['ACTION_ENTER_RESULTS']: "ENTER_RESULTS", 
            t['ACTION_MANAGE_ARCHIVES']: "MANAGE_ARCHIVES"
        }
        action_coach = action_map[st.selectbox(t['COACH_ACTION_LABEL'], list(action_map.keys()))]
        
        if action_coach == "CREATE":
            st.subheader(t['SUB_CREATE_EVENT'])
            nouvel_evenement = st.text_input(t['INPUT_NEW_EVENT_NAME'])
            type_ev_label = st.radio(t['EVENT_TYPE_LABEL'], [t['TYPE_FINALE'], t['TYPE_QUALIF']])
            type_ev_code = "finale" if type_ev_label == t['TYPE_FINALE'] else "qualif"
            
            nb_qualifies = 8
            if type_ev_code == "qualif":
                nb_qualifies = st.selectbox(t['INPUT_NB_QUALIFIES'], [8, 16, 24])
            
            if st.button(t['BTN_CREATE_EVENT']):
                if nouvel_evenement and nouvel_evenement not in st.session_state.evenements:
                    st.session_state.evenements[nouvel_evenement] = {
                        "type": type_ev_code,
                        "nb_qualifies": nb_qualifies if type_ev_code == "qualif" else 8,
                        "finalistes": ["Athlète 1", "Athlète 2", "Athlète 3", "Athlète 4", "Athlète 5", "Athlète 6", "Athlète 7", "Athlète 8"] if type_ev_code == "finale" else [f"Athlète {i+1}" for i in range(nb_qualifies + 4)],
                        "predictions": {}, "vrais_resultats": None, "statut": "actif"
                    }
                    sauvegarder_donnees()
                    st.success(t['SUCCESS_EVENT_CREATED'])
                    st.rerun()
                elif nouvel_evenement in st.session_state.evenements: st.error(t['ERR_EVENT_EXISTS'])

        elif evenement_actif and action_coach == "RENAME":
            st.subheader(f"{t['SUB_RENAME_EVENT']} : {evenement_actif}")
            nouveau_nom_ev = st.text_input(t['INPUT_NEW_NAME_EV'], value=evenement_actif)
            if st.button(t['BTN_CONFIRM_RENAME']):
                if nouveau_nom_ev != evenement_actif and nouveau_nom_ev not in st.session_state.evenements:
                    st.session_state.evenements[nouveau_nom_ev] = st.session_state.evenements.pop(evenement_actif)
                    sauvegarder_donnees()
                    st.success(t['SUCCESS_RENAMED'])
                    st.rerun()
                elif nouveau_nom_ev in st.session_state.evenements and nouveau_nom_ev != evenement_actif: st.error(t['ERR_EVENT_EXISTS'])

        elif evenement_actif and action_coach == "EDIT_FIN":
            st.subheader(f"{t['SUB_EDIT_FIN']} : {evenement_actif}")
            ev_type = st.session_state.evenements[evenement_actif].get("type", "finale")
            nb_q = st.session_state.evenements[evenement_actif].get("nb_qualifies", 8)
            finalistes_actuels = st.session_state.evenements[evenement_actif]["finalistes"]
            
            texte_noms_defaut = "\n".join(finalistes_actuels)
            noms_entres = st.text_area(t['INPUT_ATHLETES_AREA'], value=texte_noms_defaut, height=300)
            
            if st.button(t['BTN_SAVE_FIN_NAMES']):
                nouveaux_noms = [nom.strip() for nom in noms_entres.split('\n') if nom.strip()]
                if len(set(nouveaux_noms)) != len(nouveaux_noms): st.error(t['ERR_FIN_NAMES_DUPLICATE'])
                elif ev_type == "finale" and len(nouveaux_noms) != 8: st.error(t['ERR_NOT_EXACTLY_8'])
                elif ev_type == "qualif" and len(nouveaux_noms) <= nb_q: st.error(t['ERR_NOT_ENOUGH_QUALIF'].format(nb_q))
                else:
                    st.session_state.evenements[evenement_actif]["finalistes"] = nouveaux_noms
                    sauvegarder_donnees()
                    st.success(t['SUCCESS_FIN_NAMES_UPDATED'])

        elif evenement_actif and action_coach == "REPLACE_ATHLETE":
            st.subheader(t['ACTION_REPLACE_ATHLETE'])
            finalistes_actuels = st.session_state.evenements[evenement_actif]["finalistes"]
            ancien = st.selectbox("Sélectionnez l'athlète à retirer :", finalistes_actuels)
            nouveau = st.text_input("Nom complet du nouvel athlète :")
            
            if st.button("Confirmer le remplacement"):
                if nouveau and nouveau not in finalistes_actuels:
                    idx = finalistes_actuels.index(ancien)
                    st.session_state.evenements[evenement_actif]["finalistes"][idx] = nouveau
                    for p_data in st.session_state.evenements[evenement_actif]["predictions"].values():
                        choix = p_data["choix"]
                        if ancien in choix:
                            val = choix.pop(ancien)
                            choix[nouveau] = val
                    vrais = st.session_state.evenements[evenement_actif].get("vrais_resultats")
                    if vrais:
                        for k, v in vrais.items():
                            if v == ancien: vrais[k] = nouveau
                    sauvegarder_donnees()
                    st.success(f"{ancien} a été retiré et remplacé par {nouveau} partout !")
                    st.rerun()
                else:
                    st.error("Le nouveau nom est invalide ou figure déjà dans la liste.")

        elif evenement_actif and action_coach == "EDIT_PART":
            st.subheader(t['SUB_EDIT_PART'])
            predictions_actuelles = st.session_state.evenements[evenement_actif]["predictions"]
            if predictions_actuelles:
                ancien_nom = st.selectbox(t['INPUT_SELECT_PART_LABEL'], list(predictions_actuelles.keys()))
                nouveau_nom_part = st.text_input(t['INPUT_NEW_NAME_PART_LABEL'], value=ancien_nom)
                if st.button(t['BTN_MODIFY_PART']):
                    if nouveau_nom_part != ancien_nom and nouveau_nom_part not in predictions_actuelles:
                        st.session_state.evenements[evenement_actif]["predictions"][nouveau_nom_part] = st.session_state.evenements[evenement_actif]["predictions"].pop(ancien_nom)
                        sauvegarder_donnees()
                        st.success(t['SUCCESS_PART_NAME_UPDATED'])
                        st.rerun()
                    elif nouveau_nom_part in predictions_actuelles and nouveau_nom_part != ancien_nom: st.error(t['ERR_PART_NAME_EXISTS'])
            else: st.info(t['INFO_NO_PART_YET'])

        elif evenement_actif and action_coach == "MODIF_PREDICT":
            st.subheader("Modifier manuellement les choix d'un participant")
            predictions_brutes = st.session_state.evenements[evenement_actif]["predictions"]
            if predictions_brutes:
                nom_a_modifier = st.selectbox(t['INPUT_SELECT_PART_LABEL'], list(predictions_brutes.keys()))
                ev_type = st.session_state.evenements[evenement_actif].get("type", "finale")
                finalistes_actuels = sorted(st.session_state.evenements[evenement_actif]["finalistes"])
                choix_existants = predictions_brutes[nom_a_modifier]["choix"]
                est_brouillon = predictions_brutes[nom_a_modifier].get("brouillon", False)
                
                st.write(f"**Édition pour {nom_a_modifier}** (Brouillon: {'Oui' if est_brouillon else 'Non'})")
                
                if ev_type == "finale":
                    dict_choix_admin = {}
                    for i in range(0, len(finalistes_actuels), 2):
                        cols = st.columns(2)
                        for j in range(2):
                            if i + j < len(finalistes_actuels):
                                ath = finalistes_actuels[i+j]
                                with cols[j]:
                                    default_val = choix_existants.get(ath, None)
                                    default_idx = [None, 1, 2, 3, 4, 5, 6, 7, 8].index(default_val) if default_val in [None, 1, 2, 3, 4, 5, 6, 7, 8] else 0
                                    dict_choix_admin[ath] = st.selectbox(f"Rang pour {ath}", options=[None, 1, 2, 3, 4, 5, 6, 7, 8], index=default_idx, key=f"adm_sel_{ath}")
                    
                    if st.button("Enregistrer les modifications", type="primary"):
                        valeurs = list(dict_choix_admin.values())
                        if None in valeurs or len(set(valeurs)) != 8:
                            st.error(t['ERR_PREDICT_INVALID_FINALE'])
                        else:
                            st.session_state.evenements[evenement_actif]["predictions"][nom_a_modifier]["choix"] = dict_choix_admin
                            sauvegarder_donnees()
                            st.success("Prédiction modifiée avec succès !")
                            
                elif ev_type == "qualif":
                    nb_q = st.session_state.evenements[evenement_actif].get("nb_qualifies", 8)
                    choix_utilisateur = []
                    for i in range(0, len(finalistes_actuels), 3):
                        cols = st.columns(3)
                        for j in range(3):
                            if i + j < len(finalistes_actuels):
                                ath = finalistes_actuels[i+j]
                                with cols[j]:
                                    if st.checkbox(ath, value=(ath in choix_existants), key=f"adm_chk_{ath}"):
                                        choix_utilisateur.append(ath)
                    
                    st.write(f"Sélectionnés : {len(choix_utilisateur)} / {nb_q}")
                    if st.button("Enregistrer les modifications", type="primary"):
                        if len(choix_utilisateur) != nb_q:
                            st.error(t['ERR_NOT_N_SELECTED'].format(nb_q))
                        else:
                            dict_choix = {ath: (idx+1) for idx, ath in enumerate(choix_utilisateur)}
                            st.session_state.evenements[evenement_actif]["predictions"][nom_a_modifier]["choix"] = dict_choix
                            sauvegarder_donnees()
                            st.success("Prédiction modifiée avec succès !")
            else: st.info(t['INFO_NO_PREDICTS'])

        elif evenement_actif and action_coach == "DEL_PREDICT":
            st.subheader(t['ACTION_DEL_PREDICT'])
            predictions_actuelles = st.session_state.evenements[evenement_actif]["predictions"]
            if predictions_actuelles:
                nom_a_supprimer = st.selectbox("Sélectionner la prédiction à supprimer :", list(predictions_actuelles.keys()))
                if st.button("Supprimer définitivement"):
                    del st.session_state.evenements[evenement_actif]["predictions"][nom_a_supprimer]
                    sauvegarder_donnees()
                    st.success(f"La prédiction de {nom_a_supprimer} a été effacée.")
                    st.rerun()
            else:
                st.info("Aucune prédiction à supprimer.")

        elif evenement_actif and action_coach == "MODIF_NB_QUALIF":
            st.subheader(t['ACTION_MODIF_NB_QUALIF'])
            ev_type = st.session_state.evenements[evenement_actif].get("type", "finale")
            if ev_type == "qualif":
                current_nb = st.session_state.evenements[evenement_actif].get("nb_qualifies", 8)
                nouveau_nb = st.selectbox(t['INPUT_NB_QUALIFIES'], [8, 16, 24], index=[8,16,24].index(current_nb))
                if st.button("Appliquer la modification"):
                    st.session_state.evenements[evenement_actif]["nb_qualifies"] = nouveau_nb
                    sauvegarder_donnees()
                    st.success(f"Limite mise à jour ! La ronde se jouera sur {nouveau_nb} athlètes.")
            else:
                st.warning("Cette option n'est disponible que pour les Rondes de qualification.")

        elif evenement_actif and action_coach == "ENTER_RESULTS":
            st.subheader(f"{t['SUB_ENTER_RESULTS']} : {evenement_actif}")
            ev_type = st.session_state.evenements[evenement_actif].get("type", "finale")
            nb_q = st.session_state.evenements[evenement_actif].get("nb_qualifies", 8)
            finalistes_actuels = sorted(st.session_state.evenements[evenement_actif]["finalistes"])
            
            limite_resultats = 8 if ev_type == "finale" else nb_q
            vrais_resultats_rang = {}
            
            st.markdown(t['INFO_RESULTS_ORDER'])
            
            # --- SYSTÈME DE CASES À COCHER PAR ORDRE ---
            state_key = f"ordre_res_{evenement_actif}"
            
            # Initialisation de la mémoire pour l'ordre
            if state_key not in st.session_state:
                st.session_state[state_key] = []
                # Si des résultats existent déjà, on les charge pour afficher l'ordre
                vrais_res = st.session_state.evenements[evenement_actif].get("vrais_resultats")
                if vrais_res:
                    vrais_res_propres = {int(k): v for k, v in vrais_res.items()}
                    ordered_athls = [vrais_res_propres[k] for k in sorted(vrais_res_propres.keys())]
                    st.session_state[state_key] = ordered_athls
                    for ath in ordered_athls:
                        st.session_state[f"chk_res_{evenement_actif}_{ath}"] = True
            
            # Fonction qui gère l'ordre des clics
            def update_res_order(athl, chk_key, s_key):
                if st.session_state[chk_key] and athl not in st.session_state[s_key]:
                    st.session_state[s_key].append(athl)
                elif not st.session_state[chk_key] and athl in st.session_state[s_key]:
                    st.session_state[s_key].remove(athl)

            # Affichage de la grille de 3 colonnes (comme les prédictions)
            for i in range(0, len(finalistes_actuels), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(finalistes_actuels):
                        ath = finalistes_actuels[i + j]
                        chk_key = f"chk_res_{evenement_actif}_{ath}"
                        with cols[j]:
                            disabled = len(st.session_state[state_key]) >= limite_resultats and ath not in st.session_state[state_key]
                            st.checkbox(ath, key=chk_key, on_change=update_res_order, args=(ath, chk_key, state_key), disabled=disabled)
            
            st.write(f"**Sélectionnés ({len(st.session_state[state_key])} / {limite_resultats}) :**")
            if st.session_state[state_key]:
                st.caption(" ➔ ".join(st.session_state[state_key]))
            
            if st.button(t['BTN_CALC_RESULTS'], type="primary"):
                if len(st.session_state[state_key]) != limite_resultats: 
                    st.error(t['ERR_INCOMPLETE_RESULTS'].format(limite_resultats))
                else:
                    for idx, ath in enumerate(st.session_state[state_key]):
                        vrais_resultats_rang[idx + 1] = ath
                        
                    st.session_state.evenements[evenement_actif]["vrais_resultats"] = vrais_resultats_rang
                    sauvegarder_donnees()
                    st.success(t['SUCCESS_RESULTS_SAVED'])
            
            if st.session_state.evenements[evenement_actif].get("vrais_resultats"):
                vrais_res = st.session_state.evenements[evenement_actif]["vrais_resultats"]
                vrais_res_propres = {int(k): v for k, v in vrais_res.items()}
                vrais_resultats_athlete = {athlete: int(rang) for rang, athlete in vrais_res_propres.items()}
                
                vrai_top_3 = {vrais_res_propres.get(i) for i in [1, 2, 3] if vrais_res_propres.get(i)}
                vrai_premier = vrais_res_propres.get(1)
                
                scores = {}
                predictions_brutes = st.session_state.evenements[evenement_actif]["predictions"]
                valid_preds = {nom: data["choix"] for nom, data in predictions_brutes.items() if not data.get("brouillon", False)}
                
                for nom, choix_athlete in valid_preds.items():
                    score = 0
                    if ev_type == "finale":
                        pred_top_3 = {athl for athl, rang in choix_athlete.items() if rang <= 3}
                        for athl, rang in choix_athlete.items():
                            if vrais_resultats_athlete.get(athl) == rang: score += 1
                        score += len(vrai_top_3.intersection(pred_top_3))
                        if choix_athlete.get(vrai_premier) == 1: score += 1
                    
                    elif ev_type == "qualif":
                        for athl in choix_athlete.keys():
                            if athl in vrais_resultats_athlete: score += 1
                            
                    scores[nom] = score
                    
                st.subheader(t['CALC_LEADERBOARD_TITLE'])
                df_scores = pd.DataFrame(list(scores.items()), columns=[t['CALC_COL_PART'], t['CALC_COL_POINTS']])
                df_scores = df_scores.sort_values(by=t['CALC_COL_POINTS'], ascending=False).reset_index(drop=True)
                df_scores.index += 1
                st.dataframe(df_scores, use_container_width=True)

                if ev_type == "qualif":
                    st.write("---")
                    nom_nouvelle_ronde = f"{evenement_actif} - RONDE SUIVANTE"
                    if st.button(t['BTN_CREATE_NEXT_ROUND'].format(nb_q)):
                        if nom_nouvelle_ronde not in st.session_state.evenements:
                            nouveau_type = "finale" if nb_q == 8 else "qualif"
                            nouv_nb_q = 8
                            st.session_state.evenements[nom_nouvelle_ronde] = {
                                "type": nouveau_type,
                                "nb_qualifies": nouv_nb_q,
                                "finalistes": list(vrais_res_propres.values()),
                                "predictions": {}, "vrais_resultats": None, "statut": "actif"
                            }
                            sauvegarder_donnees()
                            st.success(t['SUCCESS_LINKED_FINAL'])
                        else:
                            st.info("Cette ronde a déjà été générée.")

        elif action_coach == "MANAGE_ARCHIVES":
            st.subheader(t['SUB_MANAGE_ARCHIVES'])
            tous_les_evenements = list(st.session_state.evenements.keys())
            if tous_les_evenements:
                ev_a_gerer = st.selectbox(t['CHOOSE_EVENT_LABEL'], tous_les_evenements)
                statut_actuel = t['ARCHIVE_STATUS_ACTIF'] if st.session_state.evenements[ev_a_gerer].get("statut", "actif") == "actif" else t['ARCHIVE_STATUS_ARCHIVE']
                st.write(f"{t['ARCHIVE_STATUS_LABEL']} **{statut_actuel}**")
                col1, col2 = st.columns(2)
                with col1:
                    if st.session_state.evenements[ev_a_gerer].get("statut", "actif") == "actif":
                        if st.button(t['COL1_BTN_ARCHIVE']):
                            st.session_state.evenements[ev_a_gerer]["statut"] = "archivé"
                            sauvegarder_donnees()
                            st.success(t['SUCCESS_ARCHIVED']); st.rerun()
                    else:
                        if st.button(t['COL1_BTN_UNARCHIVE']):
                            st.session_state.evenements[ev_a_gerer]["statut"] = "actif"
                            sauvegarder_donnees()
                            st.success(t['SUCCESS_UNARCHIVED']); st.rerun()
                with col2:
                    if st.button(t['COL2_BTN_DELETE_FOREVER']):
                        del st.session_state.evenements[ev_a_gerer]
                        sauvegarder_donnees()
                        st.error(t['SUCCESS_DELETED']); st.rerun()
            else: st.info(t['INFO_NO_EVENTS_TO_MANAGE'])