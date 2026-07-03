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
        'NAVI_COACH': "Zone Admin",
        'WELCOME_MSG_TITLE': "👋 Bienvenue !",
        'WELCOME_MSG_COACH_ACTION': "Veuillez aller dans la 'Zone Admin' pour créer votre premier événement.",
        'CHOOSE_EVENT_LABEL': "Choisir l'épreuve :",
        'NAVI_SUB_GO': "Aller à :",
        'SUB_PREDICT_TITLE': "Fais tes choix",
        'INPUT_NAME_LABEL': "Quel est ton nom?",
        'INFO_INPUT_NAME_FIRST': "👆 Veuillez d'abord entrer votre nom ci-dessus pour charger vos prédictions ou en faire de nouvelles.",
        'INPUT_FIN_RANK_LABEL': "Rang pour",
        'BTN_SAVE_DRAFT': "Sauvegarder le brouillon",
        'BTN_SUBMIT_FINAL': "Soumettre la version finale",
        'ERR_NO_NAME': "N'oublie pas d'inscrire ton nom!",
        'ERR_PREDICT_INCOMPLETE': "Tu dois assigner une position à TOUS les athlètes.",
        'ERR_PREDICT_DUPLICATE_RANK': "Tu as donné la même position à plus d'un athlète.",
        'SUCCESS_PREDICT_RECORDED': "✅ Tes prédictions sont enregistrées, {0}!",
        'SUCCESS_DRAFT_RECORDED': "📝 Ton brouillon a été sauvegardé, {0}. Tu pourras revenir plus tard!",
        'MULTISELECT_QUALIF_LABEL': "Sélectionne tes {0} qualifiés en cochant les noms :",
        'ERR_NOT_N_SELECTED': "Tu dois sélectionner EXACTEMENT {0} athlètes pour la version finale.",
        'SUB_VIEW_TITLE': "📊 Tableau des prédictions",
        'INFO_RESULTS_ENTERED': "Les résultats officiels sont entrés ! Compare les choix avec la première colonne.",
        'TABLE_PREDICTS_COL_TRUE_RESULT': "🏆 RÉSULTAT",
        'TABLE_PREDICTS_COL_RANK': "Rang / Choix",
        'INFO_NO_PREDICTS': "Aucune prédiction pour le moment.",
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
        'ACTION_CHANGE_NB_Q': "Modifier le nombre de qualifiés",
        'ACTION_REPLACE_ATHLETE': "Remplacer un athlète",
        'ACTION_EDIT_PARTICIPANT_NAME': "Modifier le nom d'un participant",
        'ACTION_DELETE_PRED': "Supprimer une prédiction",
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
        'SUB_CHANGE_NB_Q': "🔢 Modifier le nombre de qualifiés",
        'INPUT_NEW_NB_LABEL': "Nouveau nombre :",
        'BTN_SAVE_NB': "Sauvegarder le nombre",
        'SUCCESS_NB_CHANGED': "Nombre de qualifiés mis à jour !",
        'WARN_ONLY_QUALIF': "Cette action n'est valide que pour les rondes de qualification.",
        'SUB_REPLACE_ATHLETE': "🔄 Remplacer un athlète",
        'OLD_ATHLETE_LABEL': "Ancien athlète :",
        'NEW_ATHLETE_LABEL': "Nouvel athlète :",
        'BTN_REPLACE': "Remplacer",
        'SUCCESS_REPLACED': "Athlète remplacé avec succès !",
        'SUB_EDIT_PART': "👤 Corriger le nom d'un participant",
        'INPUT_SELECT_PART_LABEL': "Sélectionner le participant :",
        'INPUT_NEW_NAME_PART_LABEL': "Nouveau nom :",
        'BTN_MODIFY_PART': "Modifier le nom du participant",
        'SUCCESS_PART_NAME_UPDATED': "Le nom du participant a été corrigé !",
        'ERR_PART_NAME_EXISTS': "Ce nom existe déjà.",
        'INFO_NO_PART_YET': "Aucun participant pour cette épreuve.",
        'SUB_DELETE_PRED': "🗑️ Supprimer une prédiction",
        'BTN_DELETE_PRED': "Supprimer la prédiction",
        'SUCCESS_PRED_DELETED': "Prédiction supprimée avec succès !",
        'SUB_ENTER_RESULTS': "🏆 Résultats officiels pour l'épreuve",
        'INPUT_TRUE_POS': "Vraie position {0}",
        'BTN_CALC_RESULTS': "CALCULER ET APPLIQUER LES COULEURS",
        'ERR_INCOMPLETE_RESULTS': "Remplis les {0} positions avec des athlètes différents.",
        'SUCCESS_RESULTS_SAVED': "Résultats sauvegardés !",
        'CALC_LEADERBOARD_TITLE': "Classement final des experts",
        'CALC_COL_PART': "Participant",
        'CALC_COL_POINTS': "Points Total",
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
        'SUCCESS_DELETED': "L'épreuve a été supprimée.",
        'LEGEND_UNANIMOUS': "⚪ Gris : Sélectionné à l'unanimité (n'influence pas le pointage).",
        'LEGEND_FINAL_RES_FINALE': "Légende : 🟢 Bonne position | 🟡 Top 3 mais mauvaise position | 🔴 Mauvaise position",
        'LEGEND_FINAL_RES_QUALIF': "Légende : 🟢 Qualifié trouvé | 🔴 Non qualifié"
    },
    'English': {
        'APP_TITLE': "🤸 Team Predictions",
        'SIDEBAR_LANG_LABEL': "🌐 Language / Langue :",
        'NAVI_LABEL': "Navigation",
        'NAVI_PREDICT': "Make a prediction",
        'NAVI_VIEW_PREDICTS': "View predictions",
        'NAVI_COACH': "Admin Zone",
        'WELCOME_MSG_TITLE': "👋 Welcome!",
        'WELCOME_MSG_COACH_ACTION': "Please go to the 'Admin Zone' to create your first event.",
        'CHOOSE_EVENT_LABEL': "Choose the event:",
        'NAVI_SUB_GO': "Go to:",
        'SUB_PREDICT_TITLE': "Make your choices",
        'INPUT_NAME_LABEL': "What is your name?",
        'INFO_INPUT_NAME_FIRST': "👆 Please enter your name above first to load your predictions or start new ones.",
        'INPUT_FIN_RANK_LABEL': "Rank for",
        'BTN_SAVE_DRAFT': "Save as draft",
        'BTN_SUBMIT_FINAL': "Submit final version",
        'ERR_NO_NAME': "Don't forget to enter your name!",
        'ERR_PREDICT_INCOMPLETE': "You must assign a position to ALL athletes.",
        'ERR_PREDICT_DUPLICATE_RANK': "You have given the same position to more than one athlete.",
        'SUCCESS_PREDICT_RECORDED': "✅ Your predictions are recorded, {0}!",
        'SUCCESS_DRAFT_RECORDED': "📝 Your draft is saved, {0}. You can come back later!",
        'MULTISELECT_QUALIF_LABEL': "Select your {0} qualifiers by checking the names:",
        'ERR_NOT_N_SELECTED': "You must select EXACTLY {0} athletes for the final version.",
        'SUB_VIEW_TITLE': "📊 Prediction Leaderboard",
        'INFO_RESULTS_ENTERED': "Official results are in! Compare choices with the first column.",
        'TABLE_PREDICTS_COL_TRUE_RESULT': "🏆 RESULTS",
        'TABLE_PREDICTS_COL_RANK': "Rank / Choice",
        'INFO_NO_PREDICTS': "No predictions have been made yet.",
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
        'ACTION_CHANGE_NB_Q': "Modify the number of qualifiers",
        'ACTION_REPLACE_ATHLETE': "Replace an athlete",
        'ACTION_EDIT_PARTICIPANT_NAME': "Edit a participant's name",
        'ACTION_DELETE_PRED': "Delete a prediction",
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
        'SUB_CHANGE_NB_Q': "🔢 Modify the number of qualifiers",
        'INPUT_NEW_NB_LABEL': "New number:",
        'BTN_SAVE_NB': "Save number",
        'SUCCESS_NB_CHANGED': "Number of qualifiers updated!",
        'WARN_ONLY_QUALIF': "This action is only valid for qualification rounds.",
        'SUB_REPLACE_ATHLETE': "🔄 Replace an athlete",
        'OLD_ATHLETE_LABEL': "Old athlete:",
        'NEW_ATHLETE_LABEL': "New athlete:",
        'BTN_REPLACE': "Replace",
        'SUCCESS_REPLACED': "Athlete successfully replaced!",
        'SUB_EDIT_PART': "👤 Correct participant name",
        'INPUT_SELECT_PART_LABEL': "Select participant:",
        'INPUT_NEW_NAME_PART_LABEL': "New name:",
        'BTN_MODIFY_PART': "Modify name",
        'SUCCESS_PART_NAME_UPDATED': "Participant name corrected!",
        'ERR_PART_NAME_EXISTS': "Name already exists.",
        'INFO_NO_PART_YET': "No participant yet.",
        'SUB_DELETE_PRED': "🗑️ Delete a prediction",
        'BTN_DELETE_PRED': "Delete prediction",
        'SUCCESS_PRED_DELETED': "Prediction successfully deleted!",
        'SUB_ENTER_RESULTS': "🏆 Official results for",
        'INPUT_TRUE_POS': "True position {0}",
        'BTN_CALC_RESULTS': "CALCULATE AND APPLY COLORS",
        'ERR_INCOMPLETE_RESULTS': "Fill all {0} positions with different athletes.",
        'SUCCESS_RESULTS_SAVED': "Results saved!",
        'CALC_LEADERBOARD_TITLE': "Final Leaderboard",
        'CALC_COL_PART': "Participant",
        'CALC_COL_POINTS': "Total Points",
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
        'SUCCESS_DELETED': "Event deleted forever.",
        'LEGEND_UNANIMOUS': "⚪ Grey: Unanimously selected (does not influence scoring).",
        'LEGEND_FINAL_RES_FINALE': "Legend: 🟢 Correct position | 🟡 Top 3 but wrong position | 🔴 Wrong position",
        'LEGEND_FINAL_RES_QUALIF': "Legend: 🟢 Qualifier found | 🔴 Not qualified"
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
                
                # PATCH : Conversion des anciennes prédictions vers le format Brouillon/Final
                for nom, preds in ev_data.get("predictions", {}).items():
                    if not isinstance(preds, dict) or "choix" not in preds:
                        ev_data["predictions"][nom] = {"choix": preds, "statut": "final"}
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

# Ordre alphabétique des événements dans le menu (#9)
liste_evenements_actifs = sorted([ev for ev, data in st.session_state.evenements.items() if data.get("statut", "actif") == "actif"])

if not liste_evenements_actifs:
    st.sidebar.info(t['WELCOME_MSG_COACH_ACTION'])
    evenement_actif = None
    choix = t['NAVI_COACH']
else:
    evenement_actif = st.sidebar.selectbox(t['CHOOSE_EVENT_LABEL'], liste_evenements_actifs)
    choix = st.sidebar.radio(t['NAVI_SUB_GO'], [t['NAVI_PREDICT'], t['NAVI_VIEW_PREDICTS'], t['NAVI_COACH']])

st.write("---")

# =========================================================
# SECTION 1 : FAIRE UNE PRÉDICTION
# =========================================================
if evenement_actif and choix == t['NAVI_PREDICT']:
    st.header(f"{t['SUB_PREDICT_TITLE']} : {evenement_actif}")
    nom_athlete = st.text_input(t['INPUT_NAME_LABEL'])
    
    if nom_athlete:
        ev_type = st.session_state.evenements[evenement_actif].get("type", "finale")
        finalistes_actuels = st.session_state.evenements[evenement_actif]["finalistes"]
        
        # Chargement des données existantes (brouillon ou final)
        saved_data = st.session_state.evenements[evenement_actif]["predictions"].get(nom_athlete, {"choix": {}, "statut": "brouillon"})
        saved_choix = saved_data["choix"]
        
        # LOGIQUE FINALE
        if ev_type == "finale":
            choix_utilisateur = {}
            colonnes = st.columns(2)
            for i, athlete in enumerate(finalistes_actuels):
                with colonnes[i % 2]:
                    val_defaut = saved_choix.get(athlete)
                    options = [None, 1, 2, 3, 4, 5, 6, 7, 8]
                    idx_defaut = options.index(val_defaut) if val_defaut in options else 0
                    position = st.selectbox(f"{t['INPUT_FIN_RANK_LABEL']} {athlete}", options=options, index=idx_defaut, key=f"pred_{evenement_actif}_{nom_athlete}_{athlete}")
                    choix_utilisateur[athlete] = position
            
            st.write("")
            c1, c2 = st.columns(2)
            with c1:
                if st.button(t['BTN_SAVE_DRAFT']):
                    st.session_state.evenements[evenement_actif]["predictions"][nom_athlete] = {"choix": choix_utilisateur, "statut": "brouillon"}
                    sauvegarder_donnees()
                    st.success(t['SUCCESS_DRAFT_RECORDED'].format(nom_athlete))
            with c2:
                if st.button(t['BTN_SUBMIT_FINAL'], type="primary"):
                    valeurs = list(choix_utilisateur.values())
                    if None in valeurs: st.error(t['ERR_PREDICT_INCOMPLETE'])
                    elif len(set(valeurs)) != 8: st.error(t['ERR_PREDICT_DUPLICATE_RANK'])
                    else:
                        st.session_state.evenements[evenement_actif]["predictions"][nom_athlete] = {"choix": choix_utilisateur, "statut": "final"}
                        sauvegarder_donnees()
                        st.success(t['SUCCESS_PREDICT_RECORDED'].format(nom_athlete))

        # LOGIQUE QUALIFICATION (#2, #7, #8)
        elif ev_type == "qualif":
            nb_q = st.session_state.evenements[evenement_actif].get("nb_qualifies", 8)
            st.write(f"**{t['MULTISELECT_QUALIF_LABEL'].format(nb_q)}**")
            
            # Calcul du nombre sélectionné ACTUELLEMENT avant l'affichage (#7)
            current_selections = []
            for a in finalistes_actuels:
                chk_key = f"chk_{evenement_actif}_{nom_athlete}_{a}"
                if chk_key not in st.session_state:
                    st.session_state[chk_key] = (a in saved_choix)
                if st.session_state[chk_key]:
                    current_selections.append(a)
            
            limit_reached = len(current_selections) >= nb_q
            
            # Tri alphabétique puis séparation mathématique pour affichage vertical sur mobile (#2)
            sorted_athletes = sorted(finalistes_actuels)
            n_ath = len(sorted_athletes)
            col1_len = math.ceil(n_ath / 3)
            col2_len = math.ceil((n_ath - col1_len) / 2)
            lists_vertical = [sorted_athletes[:col1_len], sorted_athletes[col1_len:col1_len+col2_len], sorted_athletes[col1_len+col2_len:]]
            
            colonnes_demi = st.columns(3)
            for i, chunk in enumerate(lists_vertical):
                with colonnes_demi[i]:
                    for a in chunk:
                        chk_key = f"chk_{evenement_actif}_{nom_athlete}_{a}"
                        is_checked = st.session_state[chk_key]
                        # Désactiver si on a atteint la limite ET que la case n'est pas cochée (#7)
                        st.checkbox(a, key=chk_key, disabled=(limit_reached and not is_checked))
                        
            # Recalcul final en direct pour le bouton
            final_selections = [a for a in finalistes_actuels if st.session_state.get(f"chk_{evenement_actif}_{nom_athlete}_{a}")]
            
            couleur_compteur = "green" if len(final_selections) == nb_q else "red"
            label_compteur = "Sélectionnés" if selected_lang == 'Français' else "Selected"
            st.markdown(f"**{label_compteur} : <span style='color:{couleur_compteur}'>{len(final_selections)} / {nb_q}</span>**", unsafe_allow_html=True)
            st.write("") 
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(t['BTN_SAVE_DRAFT']):
                    dict_choix = {athlete: (i+1) for i, athlete in enumerate(final_selections)}
                    st.session_state.evenements[evenement_actif]["predictions"][nom_athlete] = {"choix": dict_choix, "statut": "brouillon"}
                    sauvegarder_donnees()
                    st.success(t['SUCCESS_DRAFT_RECORDED'].format(nom_athlete))
            with c2:
                if st.button(t['BTN_SUBMIT_FINAL'], type="primary"):
                    if len(final_selections) != nb_q: st.error(t['ERR_NOT_N_SELECTED'].format(nb_q))
                    else:
                        dict_choix = {athlete: (i+1) for i, athlete in enumerate(final_selections)}
                        st.session_state.evenements[evenement_actif]["predictions"][nom_athlete] = {"choix": dict_choix, "statut": "final"}
                        sauvegarder_donnees()
                        st.success(t['SUCCESS_PREDICT_RECORDED'].format(nom_athlete))
    else:
        st.info(t['INFO_INPUT_NAME_FIRST'])

# =========================================================
# SECTION 2 : VOIR LES PRÉDICTIONS
# =========================================================
elif evenement_actif and choix == t['NAVI_VIEW_PREDICTS']:
    st.header(f"{t['SUB_VIEW_TITLE']} : {evenement_actif}")
    ev_type = st.session_state.evenements[evenement_actif].get("type", "finale")
    predictions_actuelles = st.session_state.evenements[evenement_actif]["predictions"]
    vrais_resultats = st.session_state.evenements[evenement_actif].get("vrais_resultats")
    
    # Calcul des choix unanimes (Gris) (#5)
    unanimous_athletes = set()
    if ev_type == "qualif" and predictions_actuelles:
        n_participants = len(predictions_actuelles)
        athlete_counts = {}
        for data in predictions_actuelles.values():
            for a in data["choix"].keys():
                athlete_counts[a] = athlete_counts.get(a, 0) + 1
        unanimous_athletes = {a for a, c in athlete_counts.items() if c == n_participants and n_participants > 0}
    
    if predictions_actuelles:
        affichage_predictions = {}
        for nom, data in predictions_actuelles.items():
            # Ajout du tag Brouillon (#8)
            col_name = f"{nom} (Brouillon)" if data.get("statut") == "brouillon" else nom
            if ev_type == "finale":
                affichage_predictions[col_name] = {rang: athlete for athlete, rang in data["choix"].items()}
            else:
                # Tri alphabétique des choix pour la qualification (#5)
                choix_list = sorted(data["choix"].keys())
                affichage_predictions[col_name] = {f"Choix {i+1}": athlete for i, athlete in enumerate(choix_list)}
            
        df = pd.DataFrame(affichage_predictions)
        df.index.name = t['TABLE_PREDICTS_COL_RANK']
        if ev_type == "finale": df = df.sort_index()

        if vrais_resultats:
            st.info(t['INFO_RESULTS_ENTERED'])
            vrais_resultats_propres = {int(k): v for k, v in vrais_resultats.items()}
            
            if ev_type == "finale":
                colonne_resultats = [vrais_resultats_propres.get(i) for i in df.index]
            else:
                colonne_resultats = list(vrais_resultats_propres.values())
                
            col_true_name = t['TABLE_PREDICTS_COL_TRUE_RESULT']
            df.insert(0, col_true_name, colonne_resultats)

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
            
            # Légende (#6)
            if ev_type == "finale": st.caption(t['LEGEND_FINAL_RES_FINALE'])
            else: st.caption(t['LEGEND_FINAL_RES_QUALIF'])
            
        else:
            # S'il n'y a pas de résultats mais qu'on a des choix unanimes (Grise) (#5)
            def coloriser_brouillon(colonne):
                styles = []
                for rang_predit, athlete in colonne.items():
                    if ev_type == "qualif" and athlete in unanimous_athletes:
                        styles.append('background-color: #d3d3d3; color: black;')
                    else:
                        styles.append('')
                return styles
                
            st.dataframe(df.style.apply(coloriser_brouillon, axis=0), use_container_width=True)
            if ev_type == "qualif" and unanimous_athletes:
                st.caption(t['LEGEND_UNANIMOUS'])
    else:
        st.info(t['INFO_NO_PREDICTS'])

# =========================================================
# SECTION 3 : ZONE ADMIN
# =========================================================
elif choix == t['NAVI_COACH'] or choix == 'Zone Admin' or choix == "Admin Zone":
    st.header(t['SUB_COACH_TITLE'])
    
    if not st.session_state.coach_authentifie:
        st.write(t['COACH_LOGIN_TEXT'])
        mdp = st.text_input(t['INPUT_PWD_LABEL'], type="password")
        if st.button(t['BTN_UNLOCK']):
            if mdp == "coach":
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
            t['ACTION_CHANGE_NB_Q']: "CHANGE_NB_Q",
            t['ACTION_REPLACE_ATHLETE']: "REPLACE_ATH",
            t['ACTION_EDIT_PARTICIPANT_NAME']: "EDIT_PART",
            t['ACTION_DELETE_PRED']: "DELETE_PRED",
            t['ACTION_ENTER_RESULTS']: "ENTER_RESULTS", 
            t['ACTION_MANAGE_ARCHIVES']: "MANAGE_ARCHIVES"
        }
        action_coach = action_map[st.selectbox(t['COACH_ACTION_LABEL'], list(action_map.keys()))]
        
        # --- A. CRÉER UN ÉVÉNEMENT ---
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

        # --- B. RENOMMER ---
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

        # --- C. MODIFIER LA LISTE DE DÉPART ---
        elif evenement_actif and action_coach == "EDIT_FIN":
            st.subheader(f"{t['SUB_EDIT_FIN']} : {evenement_actif}")
            ev_type = st.session_state.evenements[evenement_actif].get("type", "finale")
            nb_q = st.session_state.evenements[evenement_actif].get("nb_qualifies", 8)
            finalistes_actuels = st.session_state.evenements[evenement_actif]["finalistes"]
            
            texte_noms_defaut = "\n".join(finalistes_actuels)
            noms_entres = st.text_area(t['INPUT_ATHLETES_AREA'], value=texte_noms_defaut, height=300)
            
            if st.button(t['BTN_SAVE_FIN_NAMES']):
                nouveaux_noms = [nom.strip() for nom in noms_entres.split('\n') if nom.strip()]
                
                if len(set(nouveaux_noms)) != len(nouveaux_noms):
                    st.error(t['ERR_FIN_NAMES_DUPLICATE'])
                elif ev_type == "finale" and len(nouveaux_noms) != 8:
                    st.error(t['ERR_NOT_EXACTLY_8'])
                elif ev_type == "qualif" and len(nouveaux_noms) <= nb_q:
                    st.error(t['ERR_NOT_ENOUGH_QUALIF'].format(nb_q))
                else:
                    st.session_state.evenements[evenement_actif]["finalistes"] = nouveaux_noms
                    sauvegarder_donnees()
                    st.success(t['SUCCESS_FIN_NAMES_UPDATED'])

        # --- C.b MODIFIER NOMBRE QUALIFIÉS (#1) ---
        elif evenement_actif and action_coach == "CHANGE_NB_Q":
            ev_type = st.session_state.evenements[evenement_actif].get("type", "finale")
            if ev_type == "qualif":
                st.subheader(t['SUB_CHANGE_NB_Q'])
                current_nb = st.session_state.evenements[evenement_actif].get("nb_qualifies", 8)
                new_nb = st.number_input(t['INPUT_NEW_NB_LABEL'], min_value=1, value=current_nb)
                if st.button(t['BTN_SAVE_NB']):
                    st.session_state.evenements[evenement_actif]["nb_qualifies"] = new_nb
                    sauvegarder_donnees()
                    st.success(t['SUCCESS_NB_CHANGED'])
            else:
                st.warning(t['WARN_ONLY_QUALIF'])

        # --- C.c REMPLACER UN ATHLÈTE (#3) ---
        elif evenement_actif and action_coach == "REPLACE_ATH":
            st.subheader(t['SUB_REPLACE_ATHLETE'])
            finalistes_actuels = st.session_state.evenements[evenement_actif]["finalistes"]
            old_a = st.selectbox(t['OLD_ATHLETE_LABEL'], finalistes_actuels)
            new_a = st.text_input(t['NEW_ATHLETE_LABEL'])
            
            if st.button(t['BTN_REPLACE']):
                if new_a and new_a not in finalistes_actuels:
                    ev = st.session_state.evenements[evenement_actif]
                    ev_type = ev.get("type", "finale")
                    # Remplacer dans la liste
                    ev["finalistes"] = [new_a if x == old_a else x for x in ev["finalistes"]]
                    # Remplacer dans TOUTES les prédictions
                    for nom, data in ev["predictions"].items():
                        choix = data["choix"]
                        if ev_type == "finale":
                            if old_a in choix: choix[new_a] = choix.pop(old_a)
                        elif ev_type == "qualif":
                            if old_a in choix:
                                val = choix.pop(old_a)
                                choix[new_a] = val
                    sauvegarder_donnees()
                    st.success(t['SUCCESS_REPLACED'])
                    st.rerun()
                elif new_a in finalistes_actuels:
                    st.error(t['ERR_PART_NAME_EXISTS'])

        # --- D. MODIFIER LE NOM D'UN PARTICIPANT ---
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
            
        # --- D.b SUPPRIMER UNE PRÉDICTION (#4) ---
        elif evenement_actif and action_coach == "DELETE_PRED":
            st.subheader(t['SUB_DELETE_PRED'])
            predictions_actuelles = list(st.session_state.evenements[evenement_actif]["predictions"].keys())
            if predictions_actuelles:
                to_delete = st.selectbox(t['INPUT_SELECT_PART_LABEL'], predictions_actuelles)
                if st.button(t['BTN_DELETE_PRED']):
                    del st.session_state.evenements[evenement_actif]["predictions"][to_delete]
                    sauvegarder_donnees()
                    st.success(t['SUCCESS_PRED_DELETED'])
                    st.rerun()
            else: st.info(t['INFO_NO_PART_YET'])

        # --- E. ENTRER LES RÉSULTATS ---
        elif evenement_actif and action_coach == "ENTER_RESULTS":
            st.subheader(f"{t['SUB_ENTER_RESULTS']} : {evenement_actif}")
            ev_type = st.session_state.evenements[evenement_actif].get("type", "finale")
            nb_q = st.session_state.evenements[evenement_actif].get("nb_qualifies", 8)
            vrais_resultats_rang = {}
            colonnes_vrai = st.columns(2)
            finalistes_actuels = st.session_state.evenements[evenement_actif]["finalistes"]
            
            limite_resultats = 8 if ev_type == "finale" else nb_q
            
            for i in range(1, limite_resultats + 1):
                with colonnes_vrai[(i - 1) % 2]:
                    gagnant = st.selectbox(t['INPUT_TRUE_POS'].format(i), options=[None] + finalistes_actuels, key=f"vrai_{i}")
                    if gagnant: vrais_resultats_rang[i] = gagnant

            if st.button(t['BTN_CALC_RESULTS'], type="primary"):
                if len(set(vrais_resultats_rang.values())) != limite_resultats: st.error(t['ERR_INCOMPLETE_RESULTS'].format(limite_resultats))
                else:
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
                predictions_actuelles = st.session_state.evenements[evenement_actif]["predictions"]
                
                for nom, data in predictions_actuelles.items():
                    score = 0
                    preds = data["choix"]
                    if ev_type == "finale":
                        pred_top_3 = {athl for athl, rang in preds.items() if rang <= 3}
                        for athl, rang in preds.items():
                            if vrais_resultats_athlete.get(athl) == rang: score += 1
                        score += len(vrai_top_3.intersection(pred_top_3))
                        if preds.get(vrai_premier) == 1: score += 1
                    
                    elif ev_type == "qualif":
                        for athl in preds.keys():
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

        # --- F. ARCHIVES ---
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