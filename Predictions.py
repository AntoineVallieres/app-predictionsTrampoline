import streamlit as st
import pandas as pd
import json
import os

# --- ÉTAPE A : LE DICTIONNAIRE DE TRADUCTIONS ---
TEXTS = {
    'Français': {
        'APP_TITLE': "🤸 Prédictions de l'équipe",
        'SIDEBAR_LANG_LABEL': "🌐 Langue / Language :",
        'NAVI_LABEL': "Navigation",
        'NAVI_PREDICT': "Faire une prédiction",
        'NAVI_VIEW_PREDICTS': "Voir les prédictions",
        'NAVI_COACH': "Zone Admin", # <-- MODIFIÉ ICI
        'WELCOME_MSG_TITLE': "👋 Bienvenue !",
        'WELCOME_MSG_COACH_ACTION': "Veuillez aller dans la 'Zone Admin' pour créer votre premier événement.",
        'CHOOSE_EVENT_LABEL': "Choisir l'épreuve :",
        'NAVI_SUB_GO': "Aller à :",
        
        # Section 1 : Prédiction
        'SUB_PREDICT_TITLE': "Fais tes choix",
        'INPUT_NAME_LABEL': "Quel est ton nom?",
        'INPUT_FIN_RANK_LABEL': "Rang pour",
        'BTN_CONFIRM_PREDICT': "CONFIRMER MES PRÉDICTIONS",
        'ERR_NO_NAME': "N'oublie pas d'inscrire ton nom!",
        'ERR_PREDICT_INCOMPLETE': "Tu dois assigner une position à TOUS les athlètes.",
        'ERR_PREDICT_DUPLICATE_RANK': "Tu as donné la même position à plus d'un athlète.",
        'SUCCESS_PREDICT_RECORDED': "✅ Tes prédictions sont enregistrées, {0}!",
        'MULTISELECT_8_LABEL': "Sélectionne tes 8 finalistes (Cliquez dans la boîte) :",
        'ERR_NOT_8_SELECTED': "Tu dois sélectionner EXACTEMENT 8 athlètes.",

        # Section 2 : Voir
        'SUB_VIEW_TITLE': "📊 Tableau des prédictions",
        'INFO_RESULTS_ENTERED': "Les résultats officiels sont entrés ! Compare les choix avec la première colonne.",
        'TABLE_PREDICTS_COL_TRUE_RESULT': "🏆 RÉSULTAT",
        'TABLE_PREDICTS_COL_RANK': "Rang / Choix",
        'INFO_NO_PREDICTS': "Aucune prédiction pour le moment.",

        # Section 3 : Coach - Login
        'SUB_COACH_TITLE': "🔒 Zone d'administration",
        'COACH_LOGIN_TEXT': "Cette zone est réservée à l'administrateur.",
        'INPUT_PWD_LABEL': "Mot de passe :",
        'BTN_UNLOCK': "Déverrouiller",
        'ERR_WRONG_PWD': "Mot de passe incorrect.",
        'BTN_LOGOUT': "Se déconnecter (Verrouiller)",

        # Section 3 : Coach - Actions
        'COACH_ACTION_LABEL': "Action :",
        'ACTION_CREATE_EVENT': "Créer une nouvelle épreuve",
        'ACTION_RENAME_EVENT': "Renommer l'épreuve",
        'ACTION_EDIT_FIN': "Modifier la liste de départ",
        'ACTION_EDIT_PARTICIPANT_NAME': "Modifier le nom d'un participant",
        'ACTION_ENTER_RESULTS': "Entrer les résultats et calculer",
        'ACTION_MANAGE_ARCHIVES': "Gérer / Archiver les épreuves",

        'SUB_CREATE_EVENT': "➕ Ajouter une compétition",
        'INPUT_NEW_EVENT_NAME': "Nom de l'épreuve",
        'EVENT_TYPE_LABEL': "Type d'épreuve :",
        'TYPE_FINALE': "Finale (Classer de 1 à 8)",
        'TYPE_DEMI': "Demi-finale (Trouver les 8 finalistes parmi 16/24)",
        'BTN_CREATE_EVENT': "Créer l'épreuve",
        'SUCCESS_EVENT_CREATED': "L'épreuve a été créée ! Rends-toi dans 'Modifier la liste de départ' pour ajuster les noms.",
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
        'ERR_NOT_ENOUGH_DEMI': "Pour une demi-finale, tu dois inscrire plus de 8 athlètes.",
        'SUCCESS_FIN_NAMES_UPDATED': "La liste a été mise à jour !",

        'SUB_EDIT_PART': "👤 Corriger le nom d'un participant",
        'INPUT_SELECT_PART_LABEL': "Sélectionner le participant :",
        'INPUT_NEW_NAME_PART_LABEL': "Nouveau nom :",
        'BTN_MODIFY_PART': "Modifier le nom du participant",
        'SUCCESS_PART_NAME_UPDATED': "Le nom du participant a été corrigé !",
        'ERR_PART_NAME_EXISTS': "Ce nom existe déjà.",
        'INFO_NO_PART_YET': "Aucun participant pour cette épreuve.",

        'SUB_ENTER_RESULTS': "🏆 Résultats officiels pour l'épreuve",
        'INPUT_TRUE_POS': "Vraie position {0}",
        'BTN_CALC_RESULTS': "CALCULER ET APPLIQUER LES COULEURS",
        'ERR_INCOMPLETE_RESULTS': "Remplis les 8 positions avec des athlètes différents.",
        'SUCCESS_RESULTS_SAVED': "Résultats sauvegardés !",
        
        'CALC_LEADERBOARD_TITLE': "Classement final des experts",
        'CALC_COL_PART': "Participant",
        'CALC_COL_POINTS': "Points Total",
        'BTN_CREATE_FINAL_FROM_DEMI': "🔗 Créer la FINALE avec ces 8 athlètes",
        'SUCCESS_LINKED_FINAL': "La finale a été créée avec succès !",

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
        'NAVI_COACH': "Admin Zone", # <-- CHANGED HERE
        'WELCOME_MSG_TITLE': "👋 Welcome!",
        'WELCOME_MSG_COACH_ACTION': "Please go to the 'Admin Zone' to create your first event.",
        'CHOOSE_EVENT_LABEL': "Choose the event:",
        'NAVI_SUB_GO': "Go to:",

        'SUB_PREDICT_TITLE': "Make your choices",
        'INPUT_NAME_LABEL': "What is your name?",
        'INPUT_FIN_RANK_LABEL': "Rank for",
        'BTN_CONFIRM_PREDICT': "CONFIRM MY PREDICTIONS",
        'ERR_NO_NAME': "Don't forget to enter your name!",
        'ERR_PREDICT_INCOMPLETE': "You must assign a position to ALL athletes.",
        'ERR_PREDICT_DUPLICATE_RANK': "You have given the same position to more than one athlete.",
        'SUCCESS_PREDICT_RECORDED': "✅ Your predictions are recorded, {0}!",
        'MULTISELECT_8_LABEL': "Select your 8 finalists (Click in the box):",
        'ERR_NOT_8_SELECTED': "You must select EXACTLY 8 athletes.",

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
        'ACTION_EDIT_PARTICIPANT_NAME': "Edit a participant's name",
        'ACTION_ENTER_RESULTS': "Enter results and calculate",
        'ACTION_MANAGE_ARCHIVES': "Manage / Archive events",

        'SUB_CREATE_EVENT': "➕ Add an event",
        'INPUT_NEW_EVENT_NAME': "Event name",
        'EVENT_TYPE_LABEL': "Event Type:",
        'TYPE_FINALE': "Final (Rank 1 to 8)",
        'TYPE_DEMI': "Semi-final (Find the 8 finalists from 16/24)",
        'BTN_CREATE_EVENT': "Create event",
        'SUCCESS_EVENT_CREATED': "Event created! Go to 'Edit start list' to adjust names.",
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
        'ERR_NOT_ENOUGH_DEMI': "For a semi-final, you must enter more than 8 athletes.",
        'SUCCESS_FIN_NAMES_UPDATED': "List has been updated!",

        'SUB_EDIT_PART': "👤 Correct participant name",
        'INPUT_SELECT_PART_LABEL': "Select participant:",
        'INPUT_NEW_NAME_PART_LABEL': "New name:",
        'BTN_MODIFY_PART': "Modify name",
        'SUCCESS_PART_NAME_UPDATED': "Participant name corrected!",
        'ERR_PART_NAME_EXISTS': "Name already exists.",
        'INFO_NO_PART_YET': "No participant yet.",

        'SUB_ENTER_RESULTS': "🏆 Official results for",
        'INPUT_TRUE_POS': "True position {0}",
        'BTN_CALC_RESULTS': "CALCULATE AND APPLY COLORS",
        'ERR_INCOMPLETE_RESULTS': "Fill all 8 positions.",
        'SUCCESS_RESULTS_SAVED': "Results saved!",

        'CALC_LEADERBOARD_TITLE': "Final Leaderboard",
        'CALC_COL_PART': "Participant",
        'CALC_COL_POINTS': "Total Points",
        'BTN_CREATE_FINAL_FROM_DEMI': "🔗 Create FINAL with these 8 athletes",
        'SUCCESS_LINKED_FINAL': "Final event successfully created!",

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
FICHIER_DONNEES = "historique_competitions.json"

st.sidebar.markdown(f"**{TEXTS['Français']['SIDEBAR_LANG_LABEL']}**")
selected_lang = st.sidebar.selectbox("", options=['Français', 'English'], label_visibility="collapsed")
t = TEXTS[selected_lang]

st.markdown(f"<script>document.title = '{t['APP_TITLE']}'</script>", unsafe_allow_html=True)

def charger_donnees():
    if os.path.exists(FICHIER_DONNEES):
        with open(FICHIER_DONNEES, "r", encoding="utf-8") as f:
            donnees = json.load(f)
            # Patch de rétrocompatibilité pour les anciennes sauvegardes
            for ev_nom, ev_data in donnees.items():
                if "statut" not in ev_data: ev_data["statut"] = "actif"
                if "vrais_resultats" not in ev_data: ev_data["vrais_resultats"] = None
                if "type" not in ev_data: ev_data["type"] = "finale"
            return donnees
    return {}

def sauvegarder_donnees():
    with open(FICHIER_DONNEES, "w", encoding="utf-8") as f:
        json.dump(st.session_state.evenements, f, ensure_ascii=False, indent=4)

if 'evenements' not in st.session_state:
    st.session_state.evenements = charger_donnees()
if 'coach_authentifie' not in st.session_state:
    st.session_state.coach_authentifie = False

st.title(t['APP_TITLE'])

st.sidebar.markdown("---")
st.sidebar.header(t['NAVI_LABEL'])
liste_evenements_actifs = [ev for ev, data in st.session_state.evenements.items() if data.get("statut", "actif") == "actif"]

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
    
    ev_type = st.session_state.evenements[evenement_actif].get("type", "finale")
    finalistes_actuels = st.session_state.evenements[evenement_actif]["finalistes"]
    
    # LOGIQUE FINALE : Classer de 1 à 8
    if ev_type == "finale":
        choix_utilisateur = {}
        colonnes = st.columns(2)
        for i, athlete in enumerate(finalistes_actuels):
            with colonnes[i % 2]:
                position = st.selectbox(f"{t['INPUT_FIN_RANK_LABEL']} {athlete}", options=[None, 1, 2, 3, 4, 5, 6, 7, 8], key=f"pred_{athlete}")
                choix_utilisateur[athlete] = position
                
        if st.button(t['BTN_CONFIRM_PREDICT'], type="primary"):
            valeurs = list(choix_utilisateur.values())
            if not nom_athlete: st.error(t['ERR_NO_NAME'])
            elif None in valeurs: st.error(t['ERR_PREDICT_INCOMPLETE'])
            elif len(set(valeurs)) != 8: st.error(t['ERR_PREDICT_DUPLICATE_RANK'])
            else:
                st.session_state.evenements[evenement_actif]["predictions"][nom_athlete] = choix_utilisateur
                sauvegarder_donnees()
                st.success(t['SUCCESS_PREDICT_RECORDED'].format(nom_athlete))

    # LOGIQUE DEMI-FINALE : Choisir 8 noms parmi la liste
    elif ev_type == "demi-finale":
        st.write(f"**{t['MULTISELECT_8_LABEL']}**")
        choix_utilisateur = st.multiselect("", options=finalistes_actuels, max_selections=8, label_visibility="collapsed")
        
        if st.button(t['BTN_CONFIRM_PREDICT'], type="primary"):
            if not nom_athlete: st.error(t['ERR_NO_NAME'])
            elif len(choix_utilisateur) != 8: st.error(t['ERR_NOT_8_SELECTED'])
            else:
                # On sauvegarde sous forme de dictionnaire pour garder la même structure (Choix 1, Choix 2, etc.)
                dict_choix = {athlete: (i+1) for i, athlete in enumerate(choix_utilisateur)}
                st.session_state.evenements[evenement_actif]["predictions"][nom_athlete] = dict_choix
                sauvegarder_donnees()
                st.success(t['SUCCESS_PREDICT_RECORDED'].format(nom_athlete))


# =========================================================
# SECTION 2 : VOIR LES PRÉDICTIONS
# =========================================================
elif evenement_actif and choix == t['NAVI_VIEW_PREDICTS']:
    st.header(f"{t['SUB_VIEW_TITLE']} : {evenement_actif}")
    ev_type = st.session_state.evenements[evenement_actif].get("type", "finale")
    predictions_actuelles = st.session_state.evenements[evenement_actif]["predictions"]
    vrais_resultats = st.session_state.evenements[evenement_actif].get("vrais_resultats")
    
    if predictions_actuelles:
        affichage_predictions = {}
        for nom, preds in predictions_actuelles.items():
            if ev_type == "finale":
                affichage_predictions[nom] = {rang: athlete for athlete, rang in preds.items()}
            else: # Demi-finale (On affiche juste la liste des 8 choix, l'ordre n'importe pas)
                affichage_predictions[nom] = {f"Choix {i+1}": athlete for i, athlete in enumerate(preds.keys())}
            
        df = pd.DataFrame(affichage_predictions)
        df.index.name = t['TABLE_PREDICTS_COL_RANK']
        if ev_type == "finale": df = df.sort_index()

        if vrais_resultats:
            st.info(t['INFO_RESULTS_ENTERED'])
            vrais_resultats_propres = {int(k): v for k, v in vrais_resultats.items()}
            
            if ev_type == "finale":
                colonne_resultats = [vrais_resultats_propres.get(i) for i in df.index]
            else:
                # En demi-finale, la vraie colonne affiche simplement les 8 finalistes qualifiés
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
                    elif ev_type == "demi-finale":
                        # En demi-finale, vert si l'athlète a fait la finale, rouge sinon.
                        if athlete in vrais_athletes: styles.append('background-color: rgba(76, 175, 80, 0.4); color: black;')
                        else: styles.append('background-color: rgba(244, 67, 54, 0.4); color: black;')
                return styles

            st.dataframe(df.style.apply(coloriser_cellules, axis=0), use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
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
            t['ACTION_EDIT_PARTICIPANT_NAME']: "EDIT_PART",
            t['ACTION_ENTER_RESULTS']: "ENTER_RESULTS", 
            t['ACTION_MANAGE_ARCHIVES']: "MANAGE_ARCHIVES"
        }
        action_coach = action_map[st.selectbox(t['COACH_ACTION_LABEL'], list(action_map.keys()))]
        
        # --- A. CRÉER UN ÉVÉNEMENT ---
        if action_coach == "CREATE":
            st.subheader(t['SUB_CREATE_EVENT'])
            nouvel_evenement = st.text_input(t['INPUT_NEW_EVENT_NAME'])
            
            # NOUVEAUTÉ : Choisir le type
            type_ev_label = st.radio(t['EVENT_TYPE_LABEL'], [t['TYPE_FINALE'], t['TYPE_DEMI']])
            type_ev_code = "finale" if type_ev_label == t['TYPE_FINALE'] else "demi-finale"
            
            if st.button(t['BTN_CREATE_EVENT']):
                if nouvel_evenement and nouvel_evenement not in st.session_state.evenements:
                    st.session_state.evenements[nouvel_evenement] = {
                        "type": type_ev_code,
                        "finalistes": ["Athlète 1", "Athlète 2", "Athlète 3", "Athlète 4", "Athlète 5", "Athlète 6", "Athlète 7", "Athlète 8"],
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

        # --- C. MODIFIER LA LISTE DE DÉPART (TEXT AREA MAGIQUE) ---
        elif evenement_actif and action_coach == "EDIT_FIN":
            st.subheader(f"{t['SUB_EDIT_FIN']} : {evenement_actif}")
            ev_type = st.session_state.evenements[evenement_actif].get("type", "finale")
            finalistes_actuels = st.session_state.evenements[evenement_actif]["finalistes"]
            
            # On affiche les noms existants sous forme de texte (un par ligne)
            texte_noms_defaut = "\n".join(finalistes_actuels)
            
            noms_entres = st.text_area(t['INPUT_ATHLETES_AREA'], value=texte_noms_defaut, height=300)
            
            if st.button(t['BTN_SAVE_FIN_NAMES']):
                # On nettoie la liste (enlève les espaces vides et les lignes vides)
                nouveaux_noms = [nom.strip() for nom in noms_entres.split('\n') if nom.strip()]
                
                if len(set(nouveaux_noms)) != len(nouveaux_noms):
                    st.error(t['ERR_FIN_NAMES_DUPLICATE'])
                elif ev_type == "finale" and len(nouveaux_noms) != 8:
                    st.error(t['ERR_NOT_EXACTLY_8'])
                elif ev_type == "demi-finale" and len(nouveaux_noms) < 8:
                    st.error(t['ERR_NOT_ENOUGH_DEMI'])
                else:
                    st.session_state.evenements[evenement_actif]["finalistes"] = nouveaux_noms
                    sauvegarder_donnees()
                    st.success(t['SUCCESS_FIN_NAMES_UPDATED'])

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

        # --- E. ENTRER LES RÉSULTATS ---
        elif evenement_actif and action_coach == "ENTER_RESULTS":
            st.subheader(f"{t['SUB_ENTER_RESULTS']} : {evenement_actif}")
            ev_type = st.session_state.evenements[evenement_actif].get("type", "finale")
            vrais_resultats_rang = {}
            colonnes_vrai = st.columns(2)
            finalistes_actuels = st.session_state.evenements[evenement_actif]["finalistes"]
            
            for i in range(1, 9):
                with colonnes_vrai[(i - 1) % 2]:
                    gagnant = st.selectbox(t['INPUT_TRUE_POS'].format(i), options=[None] + finalistes_actuels, key=f"vrai_{i}")
                    if gagnant: vrais_resultats_rang[i] = gagnant

            if st.button(t['BTN_CALC_RESULTS'], type="primary"):
                if len(set(vrais_resultats_rang.values())) != 8: st.error(t['ERR_INCOMPLETE_RESULTS'])
                else:
                    st.session_state.evenements[evenement_actif]["vrais_resultats"] = vrais_resultats_rang
                    sauvegarder_donnees()
                    st.success(t['SUCCESS_RESULTS_SAVED'])
            
            # Si les résultats sont déjà entrés, on affiche le tableau des points
            if st.session_state.evenements[evenement_actif].get("vrais_resultats"):
                vrais_res = st.session_state.evenements[evenement_actif]["vrais_resultats"]
                vrais_resultats_athlete = {athlete: int(rang) for rang, athlete in vrais_res.items()}
                vrai_top_3 = {vrais_res["1"], vrais_res["2"], vrais_res["3"]}
                vrai_premier = vrais_res["1"]
                
                scores = {}
                predictions_actuelles = st.session_state.evenements[evenement_actif]["predictions"]
                
                for nom, preds in predictions_actuelles.items():
                    score = 0
                    if ev_type == "finale":
                        pred_top_3 = {athl for athl, rang in preds.items() if rang <= 3}
                        for athl, rang in preds.items():
                            if vrais_resultats_athlete.get(athl) == rang: score += 1
                        score += len(vrai_top_3.intersection(pred_top_3))
                        if preds.get(vrai_premier) == 1: score += 1
                    
                    elif ev_type == "demi-finale":
                        # Pour la demi-finale : 1 point par athlète correctement identifié dans le top 8
                        for athl in preds.keys():
                            if athl in vrais_resultats_athlete: score += 1
                            
                    scores[nom] = score
                    
                st.subheader(t['CALC_LEADERBOARD_TITLE'])
                df_scores = pd.DataFrame(list(scores.items()), columns=[t['CALC_COL_PART'], t['CALC_COL_POINTS']])
                df_scores = df_scores.sort_values(by=t['CALC_COL_POINTS'], ascending=False).reset_index(drop=True)
                df_scores.index += 1
                st.dataframe(df_scores, use_container_width=True)

                # NOUVEAUTÉ : Le bouton pour lier Demi-Finale vers Finale
                if ev_type == "demi-finale":
                    st.write("---")
                    nom_nouvelle_finale = f"{evenement_actif} - FINALE"
                    if st.button(t['BTN_CREATE_FINAL_FROM_DEMI']):
                        if nom_nouvelle_finale not in st.session_state.evenements:
                            st.session_state.evenements[nom_nouvelle_finale] = {
                                "type": "finale",
                                "finalistes": list(vrais_res.values()), # On prend les 8 vrais gagnants
                                "predictions": {}, "vrais_resultats": None, "statut": "actif"
                            }
                            sauvegarder_donnees()
                            st.success(t['SUCCESS_LINKED_FINAL'])
                        else:
                            st.info("Cette finale a déjà été générée.")

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