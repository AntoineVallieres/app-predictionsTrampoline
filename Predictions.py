import streamlit as st
import pandas as pd
import json
import os

# --- ÉTAPE A : DÉFINIR TOUTES LES TRADUCTIONS (LE DICTIONNAIRE) ---
# Ce tableau clé-valeur contient absolument tout le texte visible sur le site.
TEXTS = {
    'Français': {
        'APP_TITLE': "🤸 Prédictions de l'équipe",
        'SIDEBAR_LANG_LABEL': "🌐 Langue / Language :",
        'NAVI_LABEL': "Navigation",
        'NAVI_PREDICT': "Faire une prédiction",
        'NAVI_VIEW_PREDICTS': "Voir les prédictions",
        'NAVI_COACH': "Zone Entraîneur",
        'WELCOME_MSG_TITLE': "👋 Bienvenue !",
        'WELCOME_MSG_COACH_ACTION': "Veuillez aller dans la 'Zone Entraîneur' pour créer votre première finale.",
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
        'SUCCESS_PREDICT_RECORDED': "✅ Tes prédictions sont enregistrées, {0}!", # {0} sera remplacé par le nom

        # Section 2 : Voir
        'SUB_VIEW_TITLE': "📊 Tableau des prédictions",
        'INFO_RESULTS_ENTERED': "Les résultats officiels sont entrés ! Compare les choix avec la première colonne.",
        'TABLE_PREDICTS_COL_TRUE_RESULT': "🏆 RÉSULTAT",
        'TABLE_PREDICTS_COL_RANK': "Rang",
        'INFO_NO_PREDICTS': "Aucune prédiction pour le moment.",
        'INFO_NO_EVENTS': "👋 Bienvenue ! Aucun événement actif pour le moment. Allez dans la Zone Entraîneur pour en créer un.",

        # Section 3 : Coach - Login
        'SUB_COACH_TITLE': "🔒 Zone d'administration",
        'COACH_LOGIN_TEXT': "Cette zone est réservée à l'entraîneur.",
        'INPUT_PWD_LABEL': "Mot de passe :",
        'BTN_UNLOCK': "Déverrouiller",
        'ERR_WRONG_PWD': "Mot de passe incorrect.",
        'BTN_LOGOUT': "Se déconnecter (Verrouiller)",

        # Section 3 : Coach - Actions
        'COACH_ACTION_LABEL': "Action :",
        'ACTION_CREATE_EVENT': "Créer une nouvelle épreuve",
        'ACTION_RENAME_EVENT': "Renommer l'épreuve actuelle",
        'ACTION_EDIT_FIN': "Modifier les finalistes",
        'ACTION_EDIT_PARTICIPANT_NAME': "Modifier le nom d'un participant",
        'ACTION_ENTER_RESULTS': "Entrer les résultats et calculer",
        'ACTION_MANAGE_ARCHIVES': "Gérer / Archiver les épreuves",

        'SUB_CREATE_EVENT': "➕ Ajouter une compétition",
        'INPUT_NEW_EVENT_NAME': "Nom de l'épreuve",
        'BTN_CREATE_EVENT': "Créer l'épreuve",
        'SUCCESS_EVENT_CREATED': "L'épreuve a été créée ! Rends-toi dans 'Modifier les finalistes' pour ajuster les noms.",
        'ERR_EVENT_EXISTS': "Une épreuve porte déjà ce nom.",

        'SUB_RENAME_EVENT': "✏️ Renommer l'épreuve",
        'INPUT_NEW_NAME_EV': "Nouveau nom :",
        'BTN_CONFIRM_RENAME': "Confirmer le nouveau nom",
        'SUCCESS_RENAMED': "L'épreuve a été renommée avec succès !",

        'SUB_EDIT_FIN': "📝 Finalistes pour l'épreuve",
        'INPUT_FIN_LABEL': "Finaliste {0}", # {0} pour le numéro
        'BTN_SAVE_FIN_NAMES': "Sauvegarder les noms",
        'ERR_FIN_NAMES_DUPLICATE': "Assure-toi que les 8 noms sont différents.",
        'SUCCESS_FIN_NAMES_UPDATED': "Les noms ont été mis à jour !",

        'SUB_EDIT_PART': "👤 Corriger le nom d'un participant",
        'INPUT_SELECT_PART_LABEL': "Sélectionner le participant :",
        'INPUT_NEW_NAME_PART_LABEL': "Nouveau nom :",
        'BTN_MODIFY_PART': "Modifier le nom du participant",
        'SUCCESS_PART_NAME_UPDATED': "Le nom du participant a été corrigé !",
        'ERR_PART_NAME_EXISTS': "Ce nom de participant existe déjà pour cette épreuve.",
        'INFO_NO_PART_YET': "Aucun participant n'a encore fait de prédiction pour cette épreuve.",

        'SUB_ENTER_RESULTS': "🏆 Résultats officiels pour l'épreuve",
        'INPUT_TRUE_POS': "Vraie position {0}", # {0} pour le rang
        'BTN_CALC_RESULTS': "CALCULER ET APPLIQUER LES COULEURS",
        'ERR_INCOMPLETE_RESULTS': "Remplis les 8 positions avec des athlètes différents.",
        'SUCCESS_RESULTS_SAVED': "Résultats sauvegardés ! Va voir le tableau des prédictions.",
        
        'CALC_LEADERBOARD_TITLE': "Classement final des experts",
        'CALC_COL_PART': "Participant",
        'CALC_COL_POINTS': "Points Total",

        'SUB_MANAGE_ARCHIVES': "🗑️ Nettoyage des événements",
        'INFO_NO_EVENTS_TO_MANAGE': "Aucun événement à gérer.",
        'ARCHIVE_STATUS_LABEL': "Statut actuel :",
        'ARCHIVE_STATUS_ACTIF': "ACTIF",
        'ARCHIVE_STATUS_ARCHIVE': "ARCHIVÉ",
        'COL1_BTN_ARCHIVE': "Dossier jaune : Archiver",
        'COL1_BTN_UNARCHIVE': "Dossier vert : Désarchiver (Réactiver)",
        'SUCCESS_ARCHIVED': "Épreuve archivée ! Elle n'apparaîtra plus dans le menu principal.",
        'SUCCESS_UNARCHIVED': "Épreuve réactivée !",
        'COL2_BTN_DELETE_FOREVER': "Dossier rouge : Supprimer DÉFINITIVEMENT",
        'SUCCESS_DELETED': "L'épreuve a été supprimée à tout jamais."
    },
    'English': {
        'APP_TITLE': "🤸 Team Predictions",
        'SIDEBAR_LANG_LABEL': "🌐 Language / Langue :",
        'NAVI_LABEL': "Navigation",
        'NAVI_PREDICT': "Make a prediction",
        'NAVI_VIEW_PREDICTS': "View predictions",
        'NAVI_COACH': "Coach's Zone",
        'WELCOME_MSG_TITLE': "👋 Welcome!",
        'WELCOME_MSG_COACH_ACTION': "Please go to the 'Coach's Zone' to create your first event.",
        'CHOOSE_EVENT_LABEL': "Choose the event:",
        'NAVI_SUB_GO': "Go to:",

        # Section 1 : Prediction
        'SUB_PREDICT_TITLE': "Make your choices",
        'INPUT_NAME_LABEL': "What is your name?",
        'INPUT_FIN_RANK_LABEL': "Rank for",
        'BTN_CONFIRM_PREDICT': "CONFIRM MY PREDICTIONS",
        'ERR_NO_NAME': "Don't forget to enter your name!",
        'ERR_PREDICT_INCOMPLETE': "You must assign a position to ALL athletes.",
        'ERR_PREDICT_DUPLICATE_RANK': "You have given the same position to more than one athlete.",
        'SUCCESS_PREDICT_RECORDED': "✅ Your predictions are recorded, {0}!",

        # Section 2 : View
        'SUB_VIEW_TITLE': "📊 Prediction Leaderboard",
        'INFO_RESULTS_ENTERED': "Official results are in! Compare choices with the first column.",
        'TABLE_PREDICTS_COL_TRUE_RESULT': "🏆 RESULTS",
        'TABLE_PREDICTS_COL_RANK': "Rank",
        'INFO_NO_PREDICTS': "No predictions have been made yet.",
        'INFO_NO_EVENTS': "👋 Welcome! There are no active events at this time. Go to the Coach Zone to create one.",

        # Section 3 : Coach - Login
        'SUB_COACH_TITLE': "🔒 Admin Area",
        'COACH_LOGIN_TEXT': "This zone is for the coach only.",
        'INPUT_PWD_LABEL': "Password:",
        'BTN_UNLOCK': "Unlock",
        'ERR_WRONG_PWD': "Incorrect password.",
        'BTN_LOGOUT': "Log out (Lock)",

        # Section 3 : Coach - Actions
        'COACH_ACTION_LABEL': "Action:",
        'ACTION_CREATE_EVENT': "Create a new event",
        'ACTION_RENAME_EVENT': "Rename current event",
        'ACTION_EDIT_FIN': "Edit finalists",
        'ACTION_EDIT_PARTICIPANT_NAME': "Edit a participant's name",
        'ACTION_ENTER_RESULTS': "Enter results and calculate",
        'ACTION_MANAGE_ARCHIVES': "Manage / Archive events",

        'SUB_CREATE_EVENT': "➕ Add a competition",
        'INPUT_NEW_EVENT_NAME': "Event name",
        'BTN_CREATE_EVENT': "Create event",
        'SUCCESS_EVENT_CREATED': "Event created! Go to 'Edit finalists' to adjust names.",
        'ERR_EVENT_EXISTS': "An event already has this name.",

        'SUB_RENAME_EVENT': "✏️ Rename event",
        'INPUT_NEW_NAME_EV': "New name:",
        'BTN_CONFIRM_RENAME': "Confirm new name",
        'SUCCESS_RENAMED': "Event renamed successfully!",

        'SUB_EDIT_FIN': "📝 Finalists for event",
        'INPUT_FIN_LABEL': "Finalist {0}",
        'BTN_SAVE_FIN_NAMES': "Save names",
        'ERR_FIN_NAMES_DUPLICATE': "Ensure all 8 names are different.",
        'SUCCESS_FIN_NAMES_UPDATED': "Names have been updated!",

        'SUB_EDIT_PART': "👤 Correct participant name",
        'INPUT_SELECT_PART_LABEL': "Select participant:",
        'INPUT_NEW_NAME_PART_LABEL': "New name:",
        'BTN_MODIFY_PART': "Modify participant name",
        'SUCCESS_PART_NAME_UPDATED': "Participant name corrected!",
        'ERR_PART_NAME_EXISTS': "This participant name already exists for this event.",
        'INFO_NO_PART_YET': "No participant has made a prediction for this event yet.",

        'SUB_ENTER_RESULTS': "🏆 Official results for event",
        'INPUT_TRUE_POS': "True position {0}",
        'BTN_CALC_RESULTS': "CALCULATE AND APPLY COLORS",
        'ERR_INCOMPLETE_RESULTS': "Fill all 8 positions with different athletes.",
        'SUCCESS_RESULTS_SAVED': "Results saved! Go check the prediction leaderboard.",

        'CALC_LEADERBOARD_TITLE': "Final Leaderboard",
        'CALC_COL_PART': "Participant",
        'CALC_COL_POINTS': "Total Points",

        'SUB_MANAGE_ARCHIVES': "🗑️ Event Management",
        'INFO_NO_EVENTS_TO_MANAGE': "No events to manage.",
        'ARCHIVE_STATUS_LABEL': "Current status:",
        'ARCHIVE_STATUS_ACTIF': "ACTIVE",
        'ARCHIVE_STATUS_ARCHIVE': "ARCHIVED",
        'COL1_BTN_ARCHIVE': "Yellow Folder: Archive",
        'COL1_BTN_UNARCHIVE': "Green Folder: Unarchive (Reactive)",
        'SUCCESS_ARCHIVED': "Event archived! It will no longer appear in the main menu.",
        'SUCCESS_UNARCHIVED': "Event reactivated!",
        'COL2_BTN_DELETE_FOREVER': "Red Folder: Delete FOREVER",
        'SUCCESS_DELETED': "The event has been deleted forever."
    }
}

# --- ÉTAPE B : CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Team Predictions", page_icon="🤸", layout="wide")
FICHIER_DONNEES = "historique_competitions.json"

# --- ÉTAPE C : SÉLECTION DE LA LANGUE DANS LA BARRE LATÉRALE ---
st.sidebar.markdown(f"**{TEXTS['Français']['SIDEBAR_LANG_LABEL']}**")
selected_lang = st.sidebar.selectbox("", options=['Français', 'English'], label_visibility="collapsed")
t = TEXTS[selected_lang] # Récupère le dictionnaire de traduction approprié

# Mise à jour du titre de l'onglet du navigateur
st.markdown(f"<script>document.title = '{t['APP_TITLE']}'</script>", unsafe_allow_html=True)

def charger_donnees():
    if os.path.exists(FICHIER_DONNEES):
        with open(FICHIER_DONNEES, "r", encoding="utf-8") as f:
            donnees = json.load(f)
            for ev_nom, ev_data in donnees.items():
                if "statut" not in ev_data:
                    ev_data["statut"] = "actif"
                if "vrais_resultats" not in ev_data:
                    ev_data["vrais_resultats"] = None
            return donnees
    return {}

def sauvegarder_donnees():
    with open(FICHIER_DONNEES, "w", encoding="utf-8") as f:
        json.dump(st.session_state.evenements, f, ensure_ascii=False, indent=4)

if 'evenements' not in st.session_state:
    st.session_state.evenements = charger_donnees()

if 'coach_authentifie' not in st.session_state:
    st.session_state.coach_authentifie = False

# --- ÉTAPE D : MISE À JOUR DU TITRE PRINCIPAL ---
st.title(t['APP_TITLE'])

# --- ÉTAPE E : MISE À JOUR DU FILTRAGE DES ÉVÉNEMENTS ---
st.sidebar.markdown("---")
st.sidebar.header(t['NAVI_LABEL'])
liste_evenements_actifs = [ev for ev, data in st.session_state.evenements.items() if data.get("statut", "actif") == "actif"]

if not liste_evenements_actifs:
    st.sidebar.info(t['WELCOME_MSG_COACH_ACTION'])
    evenement_actif = None
    choix = t['NAVI_COACH']
else:
    evenement_actif = st.sidebar.selectbox(t['CHOOSE_EVENT_LABEL'], liste_evenements_actifs)
    menu_options = [t['NAVI_PREDICT'], t['NAVI_VIEW_PREDICTS'], t['NAVI_COACH']]
    choix = st.sidebar.radio(t['NAVI_SUB_GO'], menu_options)

st.write("---")

# ---------------------------------------------------------
# SECTION 1 : FAIRE UNE PRÉDICTION (MISE À JOUR)
# ---------------------------------------------------------
if evenement_actif and choix == t['NAVI_PREDICT']:
    # f-string utilisant la traduction
    st.header(f"{t['SUB_PREDICT_TITLE']} : {evenement_actif}")
    nom_athlete = st.text_input(t['INPUT_NAME_LABEL'])
    
    choix_utilisateur = {}
    colonnes = st.columns(2)
    finalistes_actuels = st.session_state.evenements[evenement_actif]["finalistes"]
    
    for i, athlete in enumerate(finalistes_actuels):
        with colonnes[i % 2]:
            position = st.selectbox(f"{t['INPUT_FIN_RANK_LABEL']} {athlete}", options=[None, 1, 2, 3, 4, 5, 6, 7, 8], key=f"pred_{athlete}")
            choix_utilisateur[athlete] = position
            
    if st.button(t['BTN_CONFIRM_PREDICT'], type="primary"):
        valeurs = list(choix_utilisateur.values())
        if not nom_athlete:
            st.error(t['ERR_NO_NAME'])
        elif None in valeurs:
            st.error(t['ERR_PREDICT_INCOMPLETE'])
        elif len(set(valeurs)) != 8:
            st.error(t['ERR_PREDICT_DUPLICATE_RANK'])
        else:
            st.session_state.evenements[evenement_actif]["predictions"][nom_athlete] = choix_utilisateur
            sauvegarder_donnees()
            # f-string utilisant la traduction avec un paramètre
            st.success(t['SUCCESS_PREDICT_RECORDED'].format(nom_athlete))

# ---------------------------------------------------------
# SECTION 2 : VOIR LES PRÉDICTIONS (MISE À JOUR)
# ---------------------------------------------------------
elif evenement_actif and choix == t['NAVI_VIEW_PREDICTS']:
    st.header(f"{t['SUB_VIEW_TITLE']} : {evenement_actif}")
    
    predictions_actuelles = st.session_state.evenements[evenement_actif]["predictions"]
    vrais_resultats = st.session_state.evenements[evenement_actif].get("vrais_resultats")
    
    if predictions_actuelles:
        affichage_predictions = {}
        for nom, preds in predictions_actuelles.items():
            affichage_predictions[nom] = {rang: athlete for athlete, rang in preds.items()}
            
        df = pd.DataFrame(affichage_predictions)
        # Colonne 'Rang' dynamique
        df.index.name = t['TABLE_PREDICTS_COL_RANK']
        df = df.sort_index()

        if vrais_resultats:
            st.info(t['INFO_RESULTS_ENTERED'])
            
            vrais_resultats_propres = {int(k): v for k, v in vrais_resultats.items()}
            colonne_resultats = [vrais_resultats_propres.get(i) for i in df.index]
            # Colonne dynamique '🏆 RESULTAT'
            col_true_name = t['TABLE_PREDICTS_COL_TRUE_RESULT']
            df.insert(0, col_true_name, colonne_resultats)

            def coloriser_cellules(colonne):
                if colonne.name == col_true_name:
                    return ['font-weight: bold; background-color: #e6e6e6; color: black;'] * len(colonne)
                
                vrais_athletes = {athlete: int(rang) for rang, athlete in vrais_resultats.items()}
                styles = []
                for rang_predit, athlete in colonne.items():
                    rang_vrai = vrais_athletes.get(athlete)
                    if rang_vrai == int(rang_predit):
                        styles.append('background-color: rgba(76, 175, 80, 0.4); color: black;')
                    elif int(rang_predit) <= 3 and rang_vrai and rang_vrai <= 3:
                        styles.append('background-color: rgba(255, 235, 59, 0.4); color: black;')
                    else:
                        styles.append('background-color: rgba(244, 67, 54, 0.4); color: black;')
                return styles

            st.dataframe(df.style.apply(coloriser_cellules, axis=0), use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
    else:
        st.info(t['INFO_NO_PREDICTS'])

# ---------------------------------------------------------
# SECTION 3 : ZONE ENTRAÎNEUR (MISE À JOUR COMPLET)
# ---------------------------------------------------------
elif choix == t['NAVI_COACH'] or choix == 'Zone Entraîneur' or choix == "Coach's Zone":
    st.header(t['SUB_COACH_TITLE'])
    
    if not st.session_state.coach_authentifie:
        st.write(t['COACH_LOGIN_TEXT'])
        mdp = st.text_input(t['INPUT_PWD_LABEL'], type="password")
        if st.button(t['BTN_UNLOCK']):
            if mdp == "coach":
                st.session_state.coach_authentifie = True
                st.rerun()
            else:
                st.error(t['ERR_WRONG_PWD'])
    else:
        if st.button(t['BTN_LOGOUT']):
            st.session_state.coach_authentifie = False
            st.rerun()
            
        st.write("---")
        # Les options du menu d'action sont dynamiques
        action_map = {
            t['ACTION_CREATE_EVENT']: "CREATE", 
            t['ACTION_RENAME_EVENT']: "RENAME",
            t['ACTION_EDIT_FIN']: "EDIT_FIN", 
            t['ACTION_EDIT_PARTICIPANT_NAME']: "EDIT_PART",
            t['ACTION_ENTER_RESULTS']: "ENTER_RESULTS", 
            t['ACTION_MANAGE_ARCHIVES']: "MANAGE_ARCHIVES"
        }
        action_selected_label = st.selectbox(t['COACH_ACTION_LABEL'], list(action_map.keys()))
        action_coach = action_map[action_selected_label]
        
        # --- OPTION A : CRÉER UN ÉVÉNEMENT ---
        if action_coach == "CREATE":
            st.subheader(t['SUB_CREATE_EVENT'])
            nouvel_evenement = st.text_input(t['INPUT_NEW_EVENT_NAME'])
            if st.button(t['BTN_CREATE_EVENT']):
                if nouvel_evenement and nouvel_evenement not in st.session_state.evenements:
                    st.session_state.evenements[nouvel_evenement] = {
                        "finalistes": ["Athlète 1", "Athlète 2", "Athlète 3", "Athlète 4", "Athlète 5", "Athlète 6", "Athlète 7", "Athlète 8"],
                        "predictions": {},
                        "vrais_resultats": None,
                        "statut": "actif"
                    }
                    sauvegarder_donnees()
                    st.success(t['SUCCESS_EVENT_CREATED'])
                    st.rerun()
                elif nouvel_evenement in st.session_state.evenements:
                    st.error(t['ERR_EVENT_EXISTS'])

        # --- OPTION B : RENOMMER ---
        elif evenement_actif and action_coach == "RENAME":
            st.subheader(f"{t['SUB_RENAME_EVENT']} : {evenement_actif}")
            nouveau_nom_ev = st.text_input(t['INPUT_NEW_NAME_EV'], value=evenement_actif)
            if st.button(t['BTN_CONFIRM_RENAME']):
                if nouveau_nom_ev != evenement_actif and nouveau_nom_ev not in st.session_state.evenements:
                    st.session_state.evenements[nouveau_nom_ev] = st.session_state.evenements.pop(evenement_actif)
                    sauvegarder_donnees()
                    st.success(t['SUCCESS_RENAMED'])
                    st.rerun()
                elif nouveau_nom_ev in st.session_state.evenements and nouveau_nom_ev != evenement_actif:
                    st.error(t['ERR_EVENT_EXISTS'])

        # --- OPTION C : MODIFIER LES NOMS ---
        elif evenement_actif and action_coach == "EDIT_FIN":
            st.subheader(f"{t['SUB_EDIT_FIN']} : {evenement_actif}")
            nouveaux_noms = []
            finalistes_actuels = st.session_state.evenements[evenement_actif]["finalistes"]
            for i in range(8):
                label_fin = t['INPUT_FIN_LABEL'].format(i+1)
                nom = st.text_input(label_fin, value=finalistes_actuels[i], key=f"fin_{i}")
                nouveaux_noms.append(nom)
            if st.button(t['BTN_SAVE_FIN_NAMES']):
                if len(set(nouveaux_noms)) != 8:
                    st.error(t['ERR_FIN_NAMES_DUPLICATE'])
                else:
                    st.session_state.evenements[evenement_actif]["finalistes"] = nouveaux_noms
                    sauvegarder_donnees()
                    st.success(t['SUCCESS_FIN_NAMES_UPDATED'])

        # --- OPTION D : MODIFIER LE NOM D'UN PARTICIPANT ---
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
                    elif nouveau_nom_part in predictions_actuelles and nouveau_nom_part != ancien_nom:
                        st.error(t['ERR_PART_NAME_EXISTS'])
            else:
                st.info(t['INFO_NO_PART_YET'])

        # --- OPTION E : CALCULER ---
        elif evenement_actif and action_coach == "ENTER_RESULTS":
            st.subheader(f"{t['SUB_ENTER_RESULTS']} : {evenement_actif}")
            vrais_resultats_rang = {}
            colonnes_vrai = st.columns(2)
            finalistes_actuels = st.session_state.evenements[evenement_actif]["finalistes"]
            
            for i in range(1, 9):
                with colonnes_vrai[(i - 1) % 2]:
                    label_pos = t['INPUT_TRUE_POS'].format(i)
                    gagnant = st.selectbox(label_pos, options=[None] + finalistes_actuels, key=f"vrai_{i}")
                    if gagnant:
                        vrais_resultats_rang[i] = gagnant

            if st.button(t['BTN_CALC_RESULTS'], type="primary"):
                if len(set(vrais_resultats_rang.values())) != 8:
                    st.error(t['ERR_INCOMPLETE_RESULTS'])
                else:
                    st.session_state.evenements[evenement_actif]["vrais_resultats"] = vrais_resultats_rang
                    sauvegarder_donnees()
                    st.success(t['SUCCESS_RESULTS_SAVED'])
                    
                    vrais_resultats_athlete = {athlete: rang for rang, athlete in vrais_resultats_rang.items()}
                    vrai_top_3 = {vrais_resultats_rang[1], vrais_resultats_rang[2], vrais_resultats_rang[3]}
                    vrai_premier = vrais_resultats_rang[1]
                    
                    scores = {}
                    predictions_actuelles = st.session_state.evenements[evenement_actif]["predictions"]
                    
                    for nom, preds in predictions_actuelles.items():
                        score = 0
                        pred_top_3 = {athl for athl, rang in preds.items() if rang <= 3}
                        for athl, rang in preds.items():
                            if vrais_resultats_athlete.get(athl) == rang:
                                score += 1
                        score += len(vrai_top_3.intersection(pred_top_3))
                        if preds.get(vrai_premier) == 1:
                            score += 1
                        scores[nom] = score
                        
                    st.subheader(t['CALC_LEADERBOARD_TITLE'])
                    # f-string utilisant les traductions pour les colonnes du classement
                    df_scores = pd.DataFrame(list(scores.items()), columns=[t['CALC_COL_PART'], t['CALC_COL_POINTS']])
                    df_scores = df_scores.sort_values(by=t['CALC_COL_POINTS'], ascending=False).reset_index(drop=True)
                    df_scores.index += 1
                    st.dataframe(df_scores, use_container_width=True)

        # --- OPTION F : ARCHIVES ---
        elif action_coach == "MANAGE_ARCHIVES":
            st.subheader(t['SUB_MANAGE_ARCHIVES'])
            tous_les_evenements = list(st.session_state.evenements.keys())
            
            if tous_les_evenements:
                ev_a_gerer = st.selectbox(t['CHOOSE_EVENT_LABEL'], tous_les_evenements)
                statut_label_key = 'ARCHIVE_STATUS_ACTIF' if st.session_state.evenements[ev_a_gerer].get("statut", "actif") == "actif" else 'ARCHIVE_STATUS_ARCHIVE'
                statut_actuel = t[statut_label_key]
                st.write(f"{t['ARCHIVE_STATUS_LABEL']} **{statut_actuel}**")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.session_state.evenements[ev_a_gerer].get("statut", "actif") == "actif":
                        if st.button(t['COL1_BTN_ARCHIVE']):
                            st.session_state.evenements[ev_a_gerer]["statut"] = "archivé"
                            sauvegarder_donnees()
                            st.success(t['SUCCESS_ARCHIVED'])
                            st.rerun()
                    else:
                        if st.button(t['COL1_BTN_UNARCHIVE']):
                            st.session_state.evenements[ev_a_gerer]["statut"] = "actif"
                            sauvegarder_donnees()
                            st.success(t['SUCCESS_UNARCHIVED'])
                            st.rerun()
                with col2:
                    if st.button(t['COL2_BTN_DELETE_FOREVER']):
                        del st.session_state.evenements[ev_a_gerer]
                        sauvegarder_donnees()
                        st.error(t['SUCCESS_DELETED'])
                        st.rerun()
            else:
                st.info(t['INFO_NO_EVENTS_TO_MANAGE'])