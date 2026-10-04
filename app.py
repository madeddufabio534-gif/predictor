import numpy as np
import requests
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="Predictor AI - Match Center Pro", page_icon="⚽", layout="wide"
)

# --- SISTEMA DI LOGIN CON PASSWORD ---
PASSWORD_SEGRETA = "nga"

if "autenticato" not in st.session_state:
    st.session_state.autenticato = False

if not st.session_state.autenticato:
    st.markdown(
        "<h2 style='text-align: center;'>🔒 Accesso Riservato</h2>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password_inserita = st.text_input(
            "Inserisci il codice d'accesso:", type="password"
        )
        if st.button("Entra", use_container_width=True):
            if password_inserita == PASSWORD_SEGRETA:
                st.session_state.autenticato = True
                st.rerun()
            else:
                st.error("❌ Codice errato! Riprova.")
    st.stop()

# --- STYLING CSS AVANZATO ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0c2113;
        background-image: 
            linear-gradient(180deg, rgba(255, 255, 255, 0.07) 0%, rgba(255, 255, 255, 0) 15%),
            repeating-linear-gradient(
                90deg,
                rgba(17, 51, 28, 0.45) 0px,
                rgba(17, 51, 28, 0.45) 55px,
                rgba(11, 35, 19, 0.65) 55px,
                rgba(11, 35, 19, 0.65) 110px
            ),
            radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.05) 120px, transparent 121px),
            radial-gradient(circle at 50% 15%, rgba(16, 185, 129, 0.22) 0%, transparent 65%),
            radial-gradient(circle at 10% 85%, rgba(5, 150, 105, 0.15) 0%, transparent 55%);
        background-attachment: fixed;
        color: #f1f5f9;
    }
    .match-header {
        font-size: 13px;
        color: #6ee7b7;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
        font-weight: 700;
    }
    .team-box-home, .team-box-away {
        padding: 25px;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.85) 0%, rgba(4, 47, 46, 0.75) 100%);
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(10px);
    }
    .vs-text {
        font-size: 28px;
        font-weight: 900;
        background: linear-gradient(45deg, #ffffff, #34d399, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 45px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    .stat-row {
        background: rgba(6, 78, 59, 0.6);
        padding: 12px 20px;
        border-radius: 12px;
        margin-bottom: 8px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 600;
        backdrop-filter: blur(8px);
    }
    .motivation-card {
        background: linear-gradient(135deg, rgba(4, 47, 46, 0.85) 0%, rgba(6, 78, 59, 0.7) 100%);
        padding: 24px;
        border-radius: 16px;
        border-left: 4px solid #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
    }
    .bet-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(4, 47, 46, 0.85) 100%);
        padding: 22px;
        border-radius: 16px;
        border-left: 4px solid #34d399;
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-top: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
    }
    .stat-card {
        background: rgba(6, 78, 59, 0.65);
        padding: 20px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        text-align: center;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
    }
    </style>
""",
    unsafe_allow_html=True,
)

API_KEY_FOOTBALL_DATA = "d7f0800ed81a46509b1d980232a61fdb"
API_KEY_APISPORTS = "b9156f17a2e89bd74adf8b3993366211"

st.title("⚽ Football Match Center & Pronostici Pro")
st.markdown(
    "Modello avanzato con **loghi ufficiali, analisi tattica e simulazione"
    " Monte Carlo**."
)

competizioni = {
    "🇮🇹 Serie A": ("SA", "football-data"),
    "🇬🇧 Premier": ("PL", "football-data"),
    "🇪🇸 Liga": ("PD", "football-data"),
    "🇩🇪 Bundesliga": ("BL1", "football-data"),
    "🇫🇷 Ligue 1": ("FL1", "football-data"),
    "🇪🇺 Champions": ("CL", "football-data"),
    "🇪🇺 Nations League": ("5", "api-sports"),
}

scelta_comp_label = st.radio(
    "Seleziona Campionato / Torneo:",
    list(competizioni.keys()),
    horizontal=True,
)
COMPETITION_CODE, PROVIDER = competizioni[scelta_comp_label]
st.markdown("---")


@st.cache_data(ttl=3600)
def scarica_dati_da_apisports(league_id):
    headers = {"x-apisports-key": API_KEY_APISPORTS}
    matches_future = []
    history_matches = []
    standings_dict = {}
    scorers_dict = {}
    teams_data = {}
    stagioni_da_provare = [2026, 2025, 2024]
    try:
        for season in stagioni_da_provare:
            url_fixtures = f"https://v3.football.api-sports.io/fixtures?league={league_id}&season={season}"
            res = requests.get(url_fixtures, headers=headers, timeout=5)
            if res.status_code == 200:
                data = res.json().get("response", [])
                if data:
                    for m in data:
                        h_name = m["teams"]["home"]["name"]
                        a_name = m["teams"]["away"]["name"]
                        h_crest = m["teams"]["home"]["logo"]
                        a_crest = m["teams"]["away"]["logo"]
                        status = m["fixture"]["status"]["short"]
                        date_str = m["fixture"]["date"]
                        ora = (
                            date_str.split("T")[1][:5]
                            if "T" in date_str
                            else "00:00"
                        )
                        teams_data[h_name] = {"crest": h_crest}
                        teams_data[a_name] = {"crest": a_crest}
                        if status in ["NS", "TBD"]:
                            matches_future.append({
                                "casa": h_name,
                                "ospite": a_name,
                                "crest_casa": h_crest,
                                "crest_ospite": a_crest,
                                "ora": ora,
                            })
                        elif status in ["FT", "AET", "PEN"]:
                            hg = m["goals"]["home"]
                            ag = m["goals"]["away"]
                            if hg is not None and ag is not None:
                                history_matches.append({
                                    "casa": h_name,
                                    "ospite": a_name,
                                    "gol_casa": hg,
                                    "gol_ospite": ag,
                                })
                    url_standings = f"https://v3.football.api-sports.io/standings?league={league_id}&season={season}"
                    res_std = requests.get(
                        url_standings, headers=headers, timeout=5
                    )
                    if res_std.status_code == 200:
                        std_data = res_std.json().get("response", [])
                        if std_data:
                            league_blocks = std_data[0].get("league", {}).get(
                                "standings", []
                            )
                            for group in league_blocks:
                                tot_squadre = len(group)
                                for idx_pos, row in enumerate(group):
                                    team_name = row["team"]["name"]
                                    played = (
                                        row["all"]["played"]
                                        if row["all"]["played"] > 0
                                        else 1
                                    )
                                    coeff_posizione = (
                                        1.8
                                        - (idx_pos / max(1, tot_squadre - 1))
                                        * 1.3
                                    )
                                    standings_dict[team_name] = {
                                        "posizione": row["rank"],
                                        "punti": row["points"],
                                        "giocate": played,
                                        "gol_fatti_media": row["all"]["goals"][
                                            "for"
                                        ]
                                        / played,
                                        "gol_subiti_media": row["all"]["goals"][
                                            "against"
                                        ]
                                        / played,
                                        "forza_base": coeff_posizione,
                                    }
                    break
    except Exception:
        pass
    return (
        matches_future,
        history_matches,
        standings_dict,
        scorers_dict,
        teams_data,
    )


@st.cache_data(ttl=3600)
def scarica_dati_football_data(comp_code):
    headers = {"X-Auth-Token": API_KEY_FOOTBALL_DATA}
    url_scheduled = f"https://api.football-data.org/v4/competitions/{comp_code}/matches?status=SCHEDULED,TIMED"
    url_finished = f"https://api.football-data.org/v4/competitions/{comp_code}/matches?status=FINISHED"
    url_standings = f"https://api.football-data.org/v4/competitions/{comp_code}/standings"
    url_scorers = f"https://api.football-data.org/v4/competitions/{comp_code}/scorers"
    url_teams = f"https://api.football-data.org/v4/competitions/{comp_code}/teams"
    matches_future = []
    history_matches = []
    standings_dict = {}
    scorers_dict = {}
    teams_data = {}
    try:
        res_teams = requests.get(url_teams, headers=headers, timeout=5)
        if res_teams.status_code == 200:
            for t in res_teams.json().get("teams", []):
                teams_data[t["name"]] = {"crest": t.get("crest", "")}
        res_sch = requests.get(url_scheduled, headers=headers, timeout=5)
        if res_sch.status_code == 200:
            for m in res_sch.json().get("matches", []):
                h_team = m["homeTeam"]
                a_team = m["awayTeam"]
                matches_future.append({
                    "casa": h_team["name"],
                    "ospite": a_team["name"],
                    "crest_casa": h_team.get("crest", ""),
                    "crest_ospite": a_team.get("crest", ""),
                    "ora": (
                        m["utcDate"].split("T")[1][:5]
                        if "T" in m["utcDate"]
                        else "00:00"
                    ),
                })
        res_fin = requests.get(url_finished, headers=headers, timeout=5)
        if res_fin.status_code == 200:
            for m in res_fin.json().get("matches", []):
                sc = m.get("score", {}).get("fullTime", {})
                if sc.get("home") is not None and sc.get("away") is not None:
                    history_matches.append({
                        "casa": m["homeTeam"]["name"],
                        "ospite": m["awayTeam"]["name"],
                        "gol_casa": sc["home"],
                        "gol_ospite": sc["away"],
                    })
        res_std = requests.get(url_standings, headers=headers, timeout=5)
        if res_std.status_code == 200:
            table = []
            for st_block in res_std.json().get("standings", []):
                if st_block.get("type") == "TOTAL" or "table" in st_block:
                    table = st_block.get("table", [])
                    break
            tot_squadre = len(table) if table else 20
            for idx_pos, row in enumerate(table):
                team_name = row["team"]["name"]
                played = row["playedGames"] if row["playedGames"] > 0 else 1
                coeff_posizione = (
                    1.8 - (idx_pos / max(1, tot_squadre - 1)) * 1.3
                )
                standings_dict[team_name] = {
                    "posizione": idx_pos + 1,
                    "punti": row["points"],
                    "giocate": played,
                    "gol_fatti_media": row["goalsFor"] / played,
                    "gol_subiti_media": row["goalsAgainst"] / played,
                    "forza_base": coeff_posizione,
                }
        res_sc = requests.get(url_scorers, headers=headers, timeout=5)
        if res_sc.status_code == 200:
            for scorer in res_sc.json().get("scorers", []):
                p_name = scorer["player"]["name"]
                t_name = scorer["team"]["name"]
                goals = scorer.get("goals", 0)
                if t_name not in scorers_dict:
                    scorers_dict[t_name] = []
                scorers_dict[t_name].append((p_name, goals))
    except Exception:
        pass
    return (
        matches_future,
        history_matches,
        standings_dict,
        scorers_dict,
        teams_data,
    )


if PROVIDER == "api-sports":
    (
        matches_future,
        history_matches,
        standings,
        scorers,
        teams_data,
    ) = scarica_dati_da_apisports(COMPETITION_CODE)
else:
    (
        matches_future,
        history_matches,
        standings,
        scorers,
        teams_data,
    ) = scarica_dati_football_data(COMPETITION_CODE)

if not matches_future:
    if COMPETITION_CODE == "5":
        matches_future = [
            {
                "casa": "Turchia",
                "ospite": "Italia",
                "crest_casa": "",
                "crest_ospite": "",
                "ora": "20:45",
            },
            {
                "casa": "Belgio",
                "ospite": "Francia",
                "crest_casa": "",
                "crest_ospite": "",
                "ora": "20:45",
            },
        ]
    else:
        matches_future = [
            {
                "casa": "Juventus",
                "ospite": "Inter",
                "crest_casa": "",
                "crest_ospite": "",
                "ora": "20:45",
            },
            {
                "casa": "Milan",
                "ospite": "Napoli",
                "crest_casa": "",
                "crest_ospite": "",
                "ora": "18:00",
            },
        ]


def analizza_partita_pro(casa, ospite, history, standings):
    dati_casa = standings.get(
        casa,
        {
            "forza_base": 1.0,
            "posizione": 10,
            "gol_fatti_media": 1.3,
            "gol_subiti_media": 1.1,
        },
    )
    dati_ospite = standings.get(
        ospite,
        {
            "forza_base": 1.0,
            "posizione": 10,
            "gol_fatti_media": 1.3,
            "gol_subiti_media": 1.1,
        },
    )
    forza_c = dati_casa["forza_base"]
    forza_o = dati_ospite["forza_base"]
    gf_c = dati_casa["gol_fatti_media"]
    gs_c = dati_casa["gol_subiti_media"]
    gf_o = dati_ospite["gol_fatti_media"]
    gs_o = dati_ospite["gol_subiti_media"]

    ultime_casa = [
        m for m in history if m["casa"] == casa or m["ospite"] == casa
    ][-5:]
    ultime_ospite = [
        m for m in history if m["casa"] == ospite or m["ospite"] == ospite
    ][-5:]

    def calcola_rendimento_pesato(partite, squadra_target, standings_dict):
        if not partite:
            return 1.3, 1.1
        tot_gf_pesati = 0.0
        tot_gs_pesati = 0.0
        peso_totale = 0.0
        for p in partite:
            is_casa = p["casa"] == squadra_target
            avversario = p["ospite"] if is_casa else p["casa"]
            dati_avv = standings_dict.get(avversario, {"forza_base": 1.0})
            forza_avv = dati_avv["forza_base"]
            gf = p["gol_casa"] if is_casa else p["gol_ospite"]
            gs = p["gol_ospite"] if is_casa else p["gol_casa"]
            moltiplicatore_avv = max(0.5, forza_avv)
            tot_gf_pesati += gf * moltiplicatore_avv
            tot_gs_pesati += gs * (2.0 - moltiplicatore_avv)
            peso_totale += moltiplicatore_avv
        if peso_totale == 0:
            return 1.3, 1.1
        return (tot_gf_pesati / peso_totale), (tot_gs_pesati / peso_totale)

    formaf_c, formas_c = calcola_rendimento_pesato(
        ultime_casa, casa, standings
    )
    formaf_o, formas_o = calcola_rendimento_pesato(
        ultime_ospite, ospite, standings
    )

    reale_gf_c = (gf_c * 0.55) + (formaf_c * 0.45)
    reale_gs_c = (gs_c * 0.55) + (formas_c * 0.45)
    reale_gf_o = (gf_o * 0.55) + (formaf_o * 0.45)
    reale_gs_o = (gs_o * 0.55) + (formas_o * 0.45)
    delta_forza = (forza_c - forza_o) * 0.35

    xg_casa = round(
        max(
            0.7,
            ((reale_gf_c * 0.55) + (reale_gs_o * 0.45) + 0.25)
            * (1.0 + delta_forza),
        ),
        2,
    )
    xg_ospite = round(
        max(
            0.7,
            ((reale_gf_o * 0.55) + (reale_gs_c * 0.45)) * (1.0 - delta_forza),
        ),
        2,
    )
    tiri_casa = round(xg_casa * 6.2, 1)
    tiri_ospite = round(xg_ospite * 6.2, 1)
    porta_casa = round(xg_casa * 2.3, 1)
    porta_ospite = round(xg_ospite * 2.3, 1)
    tot_xg = xg_casa + xg_ospite
    diff_xg = abs(xg_casa - xg_ospite)

    if tot_xg >= 3.0:
        stile_match = "🔥 **Partita Aperta e ad Alto Potenziale Offensivo**"
        desc_stile = "Ci si attende una gara giocata a viso aperto e ritmi alti."
    elif tot_xg <= 2.1:
        stile_match = (
            "🛡️ **Partita Tattica, Bloccata e a Prevalenza Difensiva**"
        )
        desc_stile = (
            "Il modello individua i presupposti per una sfida molto attenta."
        )
    else:
        stile_match = "⚖️ **Partita Equilibrata e di Gran Movimento**"
        desc_stile = "Una gara dal canovaccio classico e duelli intensi."

    if diff_xg > 0.8:
        dominatore = casa if xg_casa > xg_ospite else ospite
        desc_inerzia = f"**{dominatore}** parte favorito per controllare il gioco."
    else:
        desc_inerzia = "L'equilibrio rende il match apertissimo a ogni scenario."

    motivazione = f"{stile_match}<br><br>{desc_stile}<br><br>{desc_inerzia}"
    return {
        "xg_f": xg_casa,
        "xg_s": xg_ospite,
        "tiri_c": tiri_casa,
        "tiri_t": tiri_ospite,
        "porta_c": porta_casa,
        "porta_t": porta_ospite,
        "media_gf_c": reale_gf_c,
        "media_gs_c": reale_gs_c,
        "media_gf_o": reale_gf_o,
        "media_gs_o": reale_gs_o,
        "motivazione": motivazione,
    }


with st.expander("✍️ Inserisci o Forza una Partita Manualmente"):
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        casa_manuale = st.text_input("Squadra Casa", "Turchia")
    with col_m2:
        ospite_manuale = st.text_input("Squadra Ospite", "Italia")
    with col_m3:
        ora_manuale = st.text_input("Orario", "20:45")
    if st.button("➕ Aggiungi / Seleziona Partita Manuale"):
        matches_future.insert(
            0,
            {
                "casa": casa_manuale,
                "ospite": ospite_manuale,
                "crest_casa": "",
                "crest_ospite": "",
                "ora": ora_manuale,
            },
        )
        st.success("Partita caricata!")

st.markdown("<br>", unsafe_allow_html=True)
opzioni = [f"⏰ {p['ora']} | {p['casa']} vs {p['ospite']}" for p in matches_future]
scelta_match = st.selectbox("Seleziona la partita da analizzare:", opzioni)
idx_scelta = opzioni.index(scelta_match)

casa = matches_future[idx_scelta]["casa"]
ospite = matches_future[idx_scelta]["ospite"]
orario = matches_future[idx_scelta]["ora"]
crest_c = matches_future[idx_scelta]["crest_casa"]
crest_o = matches_future[idx_scelta]["crest_ospite"]

st.markdown("---")
analisi = analizza_partita_pro(casa, ospite, history_matches, standings)
col_sinistra, col_destra = st.columns([1.1, 1.4], gap="large")

with col_sinistra:
    st.markdown(
        f'<div class="match-header">Scheda • Ore {orario}</div>',
        unsafe_allow_html=True,
    )
    c_box1, c_box_vs, c_box2 = st.columns([3, 1, 3])
    with c_box1:
        logo_html_c = (
            f'<img src="{crest_c}" width="60" style="margin-bottom:10px;">'
            if crest_c
            else ""
        )
        st.markdown(
            f'<div class="team-box-home">{logo_html_c}<h3'
            f' style="margin:0;color:#ffffff;font-size:16px;">{casa}</h3></div>',
            unsafe_allow_html=True,
        )
    with c_box_vs:
        st.markdown('<div class="vs-text">VS</div>', unsafe_allow_html=True)
    with c_box2:
        logo_html_o = (
            f'<img src="{crest_o}" width="60" style="margin-bottom:10px;">'
            if crest_o
            else ""
        )
        st.markdown(
            f'<div class="team-box-away">{logo_html_o}<h3'
            f' style="margin:0;color:#ffffff;font-size:16px;">{ospite}</h3></div>',
            unsafe_allow_html=True,
        )
    st.markdown("<br>", unsafe_allow_html=True)
    avvia_sim = st.button(
        "🚀 AVVIA SIMULAZIONE PRO & SCHEDINA",
        type="primary",
        use_container_width=True,
    )

with col_destra:
    st.markdown(
        '<div class="match-header" style="text-align:center;">📊 Metriche'
        " Ponderate</div>",
        unsafe_allow_html=True,
    )
    statistiche_mostrate = [
        (
            "GOL FATTI (Media)",
            f"{analisi['media_gf_c']:.2f}",
            f"{analisi['media_gf_o']:.2f}",
        ),
        (
            "GOL SUBITI (Media)",
            f"{analisi['media_gs_c']:.2f}",
            f"{analisi['media_gs_o']:.2f}",
        ),
        ("GOL ATTESI (xG)", f"{analisi['xg_f']:.2f}", f"{analisi['xg_s']:.2f}"),
        ("TIRI STIMATI", f"{analisi['tiri_c']:.1f}", f"{analisi['tiri_t']:.1f}"),
        (
            "TIRI IN PORTA",
            f"{analisi['porta_c']:.1f}",
            f"{analisi['porta_t']:.1f}",
        ),
    ]
    for label, val_c, val_t in statistiche_mostrate:
        st.markdown(
            f"""
            <div class="stat-row">
                <span style="color:#ffffff;font-size:15px;width:30%;text-align:left;font-weight:700;">{val_c}</span>
                <span style="color:#e2e8f0;font-size:12px;width:40%;text-align:center;">{label}</span>
                <span style="color:#ffffff;font-size:15px;width:30%;text-align:right;font-weight:700;">{val_t}</span>
            </div>
        """,
            unsafe_allow_html=True,
        )

st.markdown(
    '<div class="match-header">📋 Tattica & Dinamica</div>',
    unsafe_allow_html=True,
)
st.markdown(
    f"""
    <div class="motivation-card">
        <p style="margin:0;color:#f8fafc;font-size:15px;line-height:1.6;">{analisi['motivazione']}</p>
    </div>
""",
    unsafe_allow_html=True,
)

if avvia_sim:
    N_SIM = 1_000_000
    with st.spinner("Elaborazione scenari in corso..."):
        gol_c = np.random.poisson(analisi["xg_f"], N_SIM)
        gol_t = np.random.poisson(analisi["xg_s"], N_SIM)
        p_1 = np.sum(gol_c > gol_t) / N_SIM * 100
        p_x = np.sum(gol_c == gol_t) / N_SIM * 100
        p_2 = np.sum(gol_c < gol_t) / N_SIM * 100
        p_over25 = np.sum((gol_c + gol_t) >= 3) / N_SIM * 100
        p_gol = np.sum((gol_c > 0) & (gol_t > 0)) / N_SIM * 100
        coppie = list(zip(gol_c, gol_t))
        ris_unici, counts = np.unique(coppie, axis=0, return_counts=True)
        ordinati = np.argsort(counts)[::-1]
        top_3 = []
        for i in range(min(3, len(ordinati))):
            r = ris_unici[ordinati[i]]
            prob = (counts[ordinati[i]] / N_SIM) * 100
            top_3.append((r[0], r[1], prob))

    st.markdown("---")
    st.subheader("🎯 Esito Finale & Pronostici")
    col_e1, col_e2, col_e3 = st.columns(3)
    col_e1.metric(f"Vittoria ({casa})", f"{p_1:.2f}%")
    col_e2.metric("Pareggio (X)", f"{p_x:.2f}%")
    col_e3.metric(f"Vittoria ({ospite})", f"{p_2:.2f}%")

    st.markdown(
        f"""
        <div class="bet-card">
            <h4 style="margin:0 0 8px 0;color:#34d399;">💡 Giocata Consigliata</h4>
            <p style="margin:0 0 5px 0;font-size:20px;font-weight:bold;color:#ffffff;">🎯 Over 2.5 ({p_over25:.1f}%) o Goal ({p_gol:.1f}%)</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("### 🔥 Top 3 Risultati Esatti")
    cols_res = st.columns(3)
    for i, (rc, ro, p) in enumerate(top_3):
        with cols_res[i]:
            st.markdown(
                f"""
                <div class="stat-card">
                    <span style="color:#ffffff;font-weight:bold;font-size:13px;"># {i+1} SCELTA</span>
                    <h2 style="margin:10px 0;color:#ffffff;font-size:28px;">{rc} - {ro}</h2>
                    <span style="color:#34d399;font-weight:600;font-size:14px;">{p:.2f}%</span>
                </div>
            """,
                unsafe_allow_html=True,
            )
