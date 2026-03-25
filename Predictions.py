import streamlit as st
import pandas as pd
import json
import os

# 1. Configuration et Sauvegarde Permanente
st.set_page_config(page_title="Prédictions Finales", page_icon="🤸", layout="wide")
FICHIER_DONNEES = "historique_competitions.json"

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

# Initialisation de l'état d'authentification du coach
if 'coach_authentifie' not in st.session_state:
    st.session_state.coach_authentifie = False

st.title("🤸 Prédictions de l'équipe")

# ---------------------------------------------------------
# BARRE LATÉRALE : FILTRER LES ÉVÉNEMENTS ACTIFS
# ---------------------------------------------------------
st.sidebar.header("Navigation")
liste_evenements_actifs = [ev for ev, data in st.session_state.evenements.items() if data.get("statut", "actif") == "actif"]

if not liste_evenements_actifs:
    st.warning("👋 Bienvenue ! Aucun événement actif pour le moment. Allez dans la Zone Entraîneur pour en créer un.")
    evenement_actif = None
    choix = "Zone Entraîneur"
else:
    evenement_actif = st.sidebar.selectbox("Choisir l'épreuve :", liste_evenements_actifs)
    menu = ["Faire une prédiction", "Voir les prédictions", "Zone Entraîneur"]
    choix = st.sidebar.radio("Aller à :", menu)

st.write("---")

# ---------------------------------------------------------
# SECTION 1 : FAIRE UNE PRÉDICTION
# ---------------------------------------------------------
if choix == "Faire une prédiction" and evenement_actif:
    st.header(f"Fais tes choix : {evenement_actif}")
    nom_athlete = st.text_input("Quel est ton nom?")
    
    choix_utilisateur = {}
    colonnes = st.columns(2)
    finalistes_actuels = st.session_state.evenements[evenement_actif]["finalistes"]
    
    for i, athlete in enumerate(finalistes_actuels):
        with colonnes[i % 2]:
            position = st.selectbox(f"Rang pour {athlete}", options=[None, 1, 2, 3, 4, 5, 6, 7, 8], key=f"pred_{athlete}")
            choix_utilisateur[athlete] = position
            
    if st.button("CONFIRMER MES PRÉDICTIONS", type="primary"):
        valeurs = list(choix_utilisateur.values())
        if not nom_athlete:
            st.error("N'oublie pas d'inscrire ton nom!")
        elif None in valeurs:
            st.error("Tu dois assigner une position à TOUS les athlètes.")
        elif len(set(valeurs)) != 8:
            st.error("Tu as donné la même position à plus d'un athlète.")
        else:
            st.session_state.evenements[evenement_actif]["predictions"][nom_athlete] = choix_utilisateur
            sauvegarder_donnees()
            st.success(f"✅ Tes prédictions sont enregistrées, {nom_athlete}!")

# ---------------------------------------------------------
# SECTION 2 : VOIR LES PRÉDICTIONS (Avec Vrais Résultats)
# ---------------------------------------------------------
elif choix == "Voir les prédictions" and evenement_actif:
    st.header(f"📊 Tableau : {evenement_actif}")
    
    predictions_actuelles = st.session_state.evenements[evenement_actif]["predictions"]
    vrais_resultats = st.session_state.evenements[evenement_actif].get("vrais_resultats")
    
    if predictions_actuelles:
        affichage_predictions = {}
        for nom, preds in predictions_actuelles.items():
            affichage_predictions[nom] = {rang: athlete for athlete, rang in preds.items()}
            
        df = pd.DataFrame(affichage_predictions)
        df.index.name = "Rang"
        df = df.sort_index()

        # Si les résultats sont confirmés
        if vrais_resultats:
            st.info("Les résultats officiels sont entrés ! Compare les choix avec la première colonne.")
            
            # JSON convertit les clés (1, 2, 3) en texte ("1", "2", "3"), on sécurise donc la lecture
            vrais_resultats_propres = {int(k): v for k, v in vrais_resultats.items()}
            
            # 1. On crée la liste des vrais résultats dans l'ordre des rangs (1 à 8)
            colonne_resultats = [vrais_resultats_propres.get(i) for i in df.index]
            
            # 2. On insère cette liste à la position 0 (tout à gauche)
            df.insert(0, "🏆 RÉSULTAT", colonne_resultats)

            def coloriser_cellules(colonne):
                # On ne colorise pas la colonne des vrais résultats (on la met en gras et fond gris)
                if colonne.name == "🏆 RÉSULTAT":
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
        st.info("Aucune prédiction pour le moment.")

# ---------------------------------------------------------
# SECTION 3 : ZONE ENTRAÎNEUR (Protégée par mot de passe)
# ---------------------------------------------------------
elif choix == "Zone Entraîneur":
    st.header("🔒 Zone d'administration")
    
    # --- SYSTÈME DE MOT DE PASSE ---
    if not st.session_state.coach_authentifie:
        st.write("Cette zone est réservée à l'entraîneur.")
        mdp = st.text_input("Mot de passe :", type="password")
        
        # Le mot de passe actuel est "coach"
        if st.button("Déverrouiller"):
            if mdp == "coach":
                st.session_state.coach_authentifie = True
                st.rerun()
            else:
                st.error("Mot de passe incorrect.")
    
    # --- SI AUTHENTIFIÉ, ON MONTRE LE MENU ---
    else:
        if st.button("Se déconnecter (Verrouiller)"):
            st.session_state.coach_authentifie = False
            st.rerun()
            
        st.write("---")
        action_coach = st.selectbox("Action :", ["Créer une nouvelle épreuve", "Modifier les finalistes", "Entrer les résultats et calculer", "Gérer / Archiver les épreuves"])
        
        if action_coach == "Créer une nouvelle épreuve":
            st.subheader("➕ Ajouter une compétition")
            nouvel_evenement = st.text_input("Nom de l'épreuve")
            
            if st.button("Créer l'épreuve"):
                if nouvel_evenement and nouvel_evenement not in st.session_state.evenements:
                    st.session_state.evenements[nouvel_evenement] = {
                        "finalistes": ["Athlète 1", "Athlète 2", "Athlète 3", "Athlète 4", "Athlète 5", "Athlète 6", "Athlète 7", "Athlète 8"],
                        "predictions": {},
                        "vrais_resultats": None,
                        "statut": "actif"
                    }
                    sauvegarder_donnees()
                    st.success(f"L'épreuve a été créée !")
                    st.rerun()
                elif nouvel_evenement in st.session_state.evenements:
                    st.error("Ce nom d'événement existe déjà.")

        elif action_coach == "Modifier les finalistes" and evenement_actif:
            st.subheader(f"📝 Finalistes pour : {evenement_actif}")
            nouveaux_noms = []
            finalistes_actuels = st.session_state.evenements[evenement_actif]["finalistes"]
            
            for i in range(8):
                nom = st.text_input(f"Finaliste {i+1}", value=finalistes_actuels[i], key=f"fin_{i}")
                nouveaux_noms.append(nom)
                
            if st.button("Sauvegarder les noms"):
                if len(set(nouveaux_noms)) != 8:
                    st.error("Assure-toi que les 8 noms sont différents.")
                else:
                    st.session_state.evenements[evenement_actif]["finalistes"] = nouveaux_noms
                    sauvegarder_donnees()
                    st.success("Les noms ont été mis à jour !")

        elif action_coach == "Entrer les résultats et calculer" and evenement_actif:
            st.subheader(f"🏆 Résultats officiels : {evenement_actif}")
            vrais_resultats_rang = {}
            colonnes_vrai = st.columns(2)
            finalistes_actuels = st.session_state.evenements[evenement_actif]["finalistes"]
            
            for i in range(1, 9):
                with colonnes_vrai[(i - 1) % 2]:
                    gagnant = st.selectbox(f"Vraie position {i}", options=[None] + finalistes_actuels, key=f"vrai_{i}")
                    if gagnant:
                        vrais_resultats_rang[i] = gagnant

            if st.button("CALCULER ET APPLIQUER LES COULEURS", type="primary"):
                if len(set(vrais_resultats_rang.values())) != 8:
                    st.error("Remplis les 8 positions avec des athlètes différents.")
                else:
                    st.session_state.evenements[evenement_actif]["vrais_resultats"] = vrais_resultats_rang
                    sauvegarder_donnees()
                    st.success("Résultats sauvegardés ! Va voir le tableau des prédictions.")
                    
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
                        
                    st.subheader("Classement final des experts")
                    df_scores = pd.DataFrame(list(scores.items()), columns=["Participant", "Points Total"])
                    df_scores = df_scores.sort_values(by="Points Total", ascending=False).reset_index(drop=True)
                    df_scores.index += 1
                    st.dataframe(df_scores, use_container_width=True)

        elif action_coach == "Gérer / Archiver les épreuves":
            st.subheader("🗑️ Nettoyage des événements")
            tous_les_evenements = list(st.session_state.evenements.keys())
            
            if tous_les_evenements:
                ev_a_gerer = st.selectbox("Choisir l'épreuve à gérer :", tous_les_evenements)
                statut_actuel = st.session_state.evenements[ev_a_gerer].get("statut", "actif")
                
                st.write(f"Statut actuel : **{statut_actuel.upper()}**")
                
                col1, col2 = st.columns(2)
                with col1:
                    if statut_actuel == "actif":
                        if st.button("Dossier jaune : Archiver"):
                            st.session_state.evenements[ev_a_gerer]["statut"] = "archivé"
                            sauvegarder_donnees()
                            st.success("Épreuve archivée !")
                            st.rerun()
                    else:
                        if st.button("Dossier vert : Désarchiver"):
                            st.session_state.evenements[ev_a_gerer]["statut"] = "actif"
                            sauvegarder_donnees()
                            st.success("Épreuve réactivée !")
                            st.rerun()
                
                with col2:
                    if st.button("Dossier rouge : Supprimer DÉFINITIVEMENT"):
                        del st.session_state.evenements[ev_a_gerer]
                        sauvegarder_donnees()
                        st.error("L'épreuve a été supprimée.")
                        st.rerun()
            else:
                st.info("Aucun événement à gérer.")