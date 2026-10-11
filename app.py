import numpy as np
import requests
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="Predictor AI - Match Center Pro", page_icon="⚽", layout="wide"
)


# --- SISTEMA DI PASSWORD ---
def check_password():
  """Restituisce True se l'utente ha inserito la password corretta."""

  def password_entered():
    if st.session_state["password"] == "nga":
      st.session_state["password_correct"] = True
      del st.session_state["password"]
    else:
      st.session_state["password_correct"] = False

  if "password_correct" not in st.session_state:
    st.markdown(
        "<h2 style='text-align: center; color: #34d399;'>🔐 Accesso Riservato"
        " - Predictor AI</h2>",
        unsafe_allow_html=True,
    )
    st.text_input(
        "Inserisci la password per accedere:",
        type="password",
        on_change=password_entered,
        key="password",
    )
    return False
  elif not st.session_state["password_correct"]:
    st.markdown(
        "<h2 style='text-align: center; color: #34d399;'>🔐 Accesso Riservato"
        " - Predictor AI</h2>",
        unsafe_allow_html=True,
    )
    st.text_input(
        "Inserisci la password per accedere:",
        type="password",
        on_change=password_entered,
        key="password",
    )
    st.error("😕 Password errata. Riprova.")
    return False
  else:
    return True


if not check_password():
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
        padding: 20px;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.85) 0%, rgba(4, 47, 46, 0.75) 100%);
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(10px);
    }
    .vs-text {
        font-size: 26px;
        font-weight: 900;
        background: linear-gradient(45deg, #ffffff, #34d399, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 35px;
    }
    .summary-card {
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.9) 0%, rgba(4, 47, 46, 0.85) 100%);
        border: 1px solid rgba(52, 211, 153, 0.4);
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .res-box {
        background: rgba(4, 47, 46, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        color: #ffffff;
    }
    .stat-row-clean {
        background: rgba(6, 78, 59, 0.5);
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 6px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 600;
    }
    .badge-live {
        display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700;
        background-color: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(255, 255, 255, 0.3);
    }
    .alert-box {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-top: 30px;
        color: #fca5a5;
    }
    </style>
""",
    unsafe_allow_html=True,
)

API_KEY = "d7f0800ed81a46509b1d980232a61fdb"

st.title("⚽ Football Match Center & Pronostici Pro")
st.markdown(
    "Modello avanzato con **4 Categorie (Big, Media, Bassa, Neopromosse)** e"
    " Dashboard Unificata."
)

competizioni = {
    "🇮🇹 Serie A": "SA",
    "🇬🇧 Premier": "PL",
    "🇪🇸 Liga": "PD",
    "🇩🇪 Bundesliga": "BL1",
    "🇫🇷 Ligue 1": "FL1",
    "🇪🇺 Champions": "CL",
}

scelta_comp_label = st.radio(
    "Seleziona Campionato / Torneo:",
    list(competizioni.keys()),
    horizontal=True,
)
COMPETITION_CODE = competizioni[scelta_comp_label]

st.markdown("---")


@st.cache_data(ttl=3600)
def scarica_dati_completi(comp_code):
  headers = {"X-Auth-Token": API_KEY}
  url_scheduled = f"https://api.football-data.org/v4/competitions/{comp_code}/matches?status=SCHEDULED,TIMED"
  url_finished = f"https://api.football-data.org/v4/competitions/{comp_code}/matches?status=FINISHED"
  url_standings = (
      f"https://api.football-data.org/v4/competitions/{comp_code}/standings"
  )
  url_scorers = f"https://api.football-data.org/v4/competitions/{comp_code}/scorers"
  url_teams = (
      f"https://api.football-data.org/v4/competitions/{comp_code}/teams"
  )

  matches_future = []
  history_matches = []
  standings_dict = {}
  scorers_dict = {}
  teams_data = {}

  try:
    res_teams = requests.get(url_teams, headers=headers, timeout=5)
    if res_teams.status_code == 200:
      for t in res_teams.json().get("teams", []):
        t_name = t["name"]
        teams_data[t_name] = {"crest": t.get("crest", "")}

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
                m["utcDate"].split("T")[1][:5] if "T" in m["utcDate"] else "00:00"
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
      data_s = res_std.json()
      table = []
      for st_block in data_s.get("standings", []):
        if st_block.get("type") == "TOTAL" or "table" in st_block:
          table = st_block.get("table", [])
          break

      tot_squadre = len(table) if table else 20
      for idx_pos, row in enumerate(table):
        team_name = row["team"]["name"]
        played = row["playedGames"] if row["playedGames"] > 0 else 1

        neopromosse_keywords = ["monza", "frosinone", "venezia"]
        bassa_keywords = ["lecce", "cagliari", "empoli", "verona", "spezia"]
        big_keywords = [
            "inter",
            "milan",
            "juventus",
            "napoli",
            "atalanta",
            "roma",
            "lazio",
            "real madrid",
            "barcelona",
            "atletico",
            "manchester city",
            "arsenal",
            "liverpool",
            "chelsea",
            "bayern",
            "dortmund",
            "leverkusen",
            "psg",
        ]

        is_neopromossa = any(
            kw in team_name.lower() for kw in neopromosse_keywords
        )
        is_bassa = any(bk in team_name.lower() for bk in bassa_keywords)
        is_big = any(bg in team_name.lower() for bg in big_keywords)

        if is_big:
          status_multiplier = 1.15
          status_label = "⭐ Big Team"
        elif is_neopromossa:
          status_multiplier = 0.88
          status_label = "🌱 Neopromossa"
        elif is_bassa:
          status_multiplier = 0.93
          status_label = "📉 Fascia Bassa"
        else:
          status_multiplier = 1.00
          status_label = "⚖️ Media Classifica"

        coeff_posizione = 1.8 - (idx_pos / max(1, tot_squadre - 1)) * 1.3

        standings_dict[team_name] = {
            "posizione": idx_pos + 1,
            "punti": row["points"],
            "giocate": played,
            "gol_fatti_media": row["goalsFor"] / played,
            "gol_subiti_media": row["goalsAgainst"] / played,
            "forza_base": coeff_posizione,
            "status_multiplier": status_multiplier,
            "status_label": status_label,
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

  return matches_future, history_matches, standings_dict, scorers_dict, teams_data


def analizza_partita_pro(casa, ospite, history, standings):
  dati_casa = standings.get(
      casa,
      {
          "forza_base": 1.0,
          "posizione": 10,
          "gol_fatti_media": 1.3,
          "gol_subiti_media": 1.1,
          "status_multiplier": 1.0,
          "status_label": "Media Classifica",
      },
  )
  dati_ospite = standings.get(
      ospite,
      {
          "forza_base": 1.0,
          "posizione": 10,
          "gol_fatti_media": 1.3,
          "gol_subiti_media": 1.1,
          "status_multiplier": 1.0,
          "status_label": "Media Classifica",
      },
  )

  forza_c = dati_casa["forza_base"] * dati_casa["status_multiplier"]
  forza_o = dati_ospite["forza_base"] * dati_ospite["status_multiplier"]

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

  reale_gf_c = (
      (gf_c * 0.55) + (formaf_c * 0.45)
  ) * dati_casa["status_multiplier"]
  reale_gs_c = (gs_c * 0.55) + (formas_c * 0.45)
  reale_gf_o = (
      (gf_o * 0.55) + (formaf_o * 0.45)
  ) * dati_ospite["status_multiplier"]
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
  falli_casa = int(round(11 + (xg_ospite * 0.8), 0))
  falli_ospite = int(round(11 + (xg_casa * 0.8), 0))
  gialli_casa = int(round(1.5 + (xg_ospite * 0.3), 0))
  gialli_ospite = int(round(1.5 + (xg_casa * 0.3), 0))

  return {
      "xg_f": xg_casa,
      "xg_s": xg_ospite,
      "tiri_c": tiri_casa,
      "tiri_t": tiri_ospite,
      "porta_c": porta_casa,
      "porta_t": porta_ospite,
      "falli_c": falli_casa,
      "falli_t": falli_ospite,
      "gialli_c": gialli_casa,
      "gialli_t": gialli_ospite,
      "media_gf_c": reale_gf_c,
      "media_gs_c": reale_gs_c,
      "media_gf_o": reale_gf_o,
      "media_gs_o": reale_gs_o,
      "status_c": dati_casa["status_label"],
      "status_o": dati_ospite["status_label"],
  }


(
    matches_future,
    history_matches,
    standings,
    scorers,
    teams_data,
) = scarica_dati_completi(COMPETITION_CODE)

if not matches_future:
  st.markdown(
      f"""
        <div class="alert-box">
            <h3 style="margin:0 0 10px 0; color:#f87171;">⚠️ Nessun match disponibile per {scelta_comp_label}</h3>
            <p style="margin:0; font-size:14px; color:#cbd5e1;">Seleziona <b>🇮🇹 Serie A</b> o <b>🇬🇧 Premier</b>.</p>
        </div>
    """,
      unsafe_allow_html=True,
  )
else:
  if history_matches:
    st.markdown(
        f'<span class="badge-live">🟢 Dashboard Unificata Attiva'
        f" ({scelta_comp_label})</span>",
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        '<span class="badge-fallback" style="background-color:rgba(245,158,11,0.2); color:#fbbf24; padding:4px 12px; border-radius:20px; font-weight:700; font-size:12px;">🟡 Connessione limitata</span>',
        unsafe_allow_html=True,
    )

  st.markdown("<br>", unsafe_allow_html=True)

  opzioni = [
      f"⏰ {p['ora']} | {p['casa']} vs {p['ospite']}" for p in matches_future
  ]
  scelta_match = st.selectbox("Seleziona la partita da analizzare:", opzioni)
  idx_scelta = opzioni.index(scelta_match)

  casa = matches_future[idx_scelta]["casa"]
  ospite = matches_future[idx_scelta]["ospite"]
  orario = matches_future[idx_scelta]["ora"]
  crest_c = matches_future[idx_scelta]["crest_casa"]
  crest_o = matches_future[idx_scelta]["crest_ospite"]

  st.markdown("---")

  analisi = analizza_partita_pro(casa, ospite, history_matches, standings)

  # --- INTESTAZIONE SQUADRE ---
  c_box1, c_box_vs, c_box2 = st.columns([3, 1, 3])
  with c_box1:
    logo_html_c = (
        f'<img src="{crest_c}" width="50" style="margin-bottom:8px;">'
        if crest_c
        else ""
    )
    st.markdown(
        f"""
            <div class="team-box-home">
                {logo_html_c}
                <h3 style="margin:0; color:#ffffff; font-size:15px;">{casa}</h3>
                <span style="font-size:11px; color:#34d399;">{analisi['status_c']}</span>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with c_box_vs:
    st.markdown('<div class="vs-text">VS</div>', unsafe_allow_html=True)
  with c_box2:
    logo_html_o = (
        f'<img src="{crest_o}" width="50" style="margin-bottom:8px;">'
        if crest_o
        else ""
    )
    st.markdown(
        f"""
            <div class="team-box-away">
                {logo_html_o}
                <h3 style="margin:0; color:#ffffff; font-size:15px;">{ospite}</h3>
                <span style="font-size:11px; color:#34d399;">{analisi['status_o']}</span>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("<br>", unsafe_allow_html=True)

  # --- MOTORE DI SIMULAZIONE AUTOMATICO (SENZA BISOGNO DI CLICCARE PULSANTI) ---
  N_SIM = 1_000_000
  gol_c = np.random.poisson(analisi["xg_f"], N_SIM)
  gol_t = np.random.poisson(analisi["xg_s"], N_SIM)

  p_1 = np.sum(gol_c > gol_t) / N_SIM * 100
  p_x = np.sum(gol_c == gol_t) / N_SIM * 100
  p_2 = np.sum(gol_c < gol_t) / N_SIM * 100

  coppie = list(zip(gol_c, gol_t))
  ris_unici, counts = np.unique(coppie, axis=0, return_counts=True)
  ordinati = np.argsort(counts)[::-1]

  # Top risultato esatto principale
  top_rc, top_ro = ris_unici[ordinati[0]]
  top_prob = (counts[ordinati[0]] / N_SIM) * 100

  dominante_txt = (
      f"{casa} AVANTI AL 90'"
      if p_1 > p_2
      else (f"{ospite} AVANTI AL 90'" if p_2 > p_1 else "EQUILIBRIO AL 90'")
  )
  vincente_perc = max(p_1, p_2, p_x)

  # Top 4 risultati esatti per la riga stile app
  top_4 = []
  for i in range(min(4, len(ordinati))):
    r = ris_unici[ordinati[i]]
    p = (counts[ordinati[i]] / N_SIM) * 100
    top_4.append((f"{r[0]}-{r[1]}", p))

  # --- SCHERMATA UNIFICATA STILE APP (FOTO) ---
  st.markdown(
      f"""
    <div class="summary-card">
        <p style="margin:0; font-size:11px; color:#94a3b8; text-transform:uppercase; letter-spacing:1px;">SCELTO TRA I 1.000.000 DI SIMULAZIONI PRO</p>
        <h2 style="margin:5px 0; color:#ffffff; font-size:26px;">{casa} {top_rc} - {top_ro} {ospite}</h2>
        <p style="margin:0; font-size:13px; color:#34d399; font-weight:bold;">{dominante_txt}</p>
        <p style="margin:3px 0 15px 0; font-size:12px; color:#cbd5e1;">Risultato: {top_prob:.1f}% | Probabilità esito principale al {vincente_perc:.0f}%</p>
        
        <p style="margin:10px 0 5px 0; font-size:11px; color:#94a3b8; text-transform:uppercase;">RISULTATI ESATTI AL 90° PIÙ PROBABILI</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

  # Riga dei 4 risultati esatti
  r_cols = st.columns(4)
  for i, (res_str, prob_val) in enumerate(top_4):
    with r_cols[i]:
      st.markdown(
          f"""
            <div class="res-box">
                <div style="font-size:18px; color:#ffffff;">{res_str}</div>
                <div style="font-size:12px; color:#34d399; font-weight:normal;">{prob_val:.1f}%</div>
            </div>
        """,
          unsafe_allow_html=True,
      )

  st.markdown("<br>", unsafe_allow_html=True)

  # --- TABELLA STATISTICHE & 1X2 (STILE FOTO) ---
  st.markdown(
      """
    <div style="background: rgba(6, 78, 59, 0.7); padding: 15px; border-radius: 14px; border: 1px solid rgba(255,255,255,0.15);">
        <p style="text-align:center; font-size:12px; color:#6ee7b7; text-transform:uppercase; font-weight:bold; margin-bottom:10px;">📊 1X2 & METRICHE DI GARA</p>
    """,
      unsafe_allow_html=True,
  )

  statistiche_mostrate = [
      (
          f"Vittoria {casa} ({p_1:.1f}%)",
          "PROBABILITÀ 1X2",
          f"Vittoria {ospite} ({p_2:.1f}%)",
      ),
      ("Pareggio (X)", f"{p_x:.1f}%", "ESITO X"),
      (f"{analisi['tiri_c']:.0f}", "TIRI STIMATI", f"{analisi['tiri_t']:.0f}"),
      (
          f"{analisi['porta_c']:.0f}",
          "TIRI IN PORTA",
          f"{analisi['porta_t']:.0f}",
      ),
      (f"{analisi['falli_c']}", "FALLI STIMATI", f"{analisi['falli_t']}"),
      (f"{analisi['gialli_c']}", "CARTELLINI GIALLI", f"{analisi['gialli_t']}"),
  ]

  # Mostriamo le metriche chiave in modo pulito
  st.markdown(
      f"""
        <div class="stat-row-clean"><span style="color:#ffffff; width:33%; text-align:left;"><b>{p_1:.1f}%</b></span><span style="color:#94a3b8; width:33%; text-align:center; font-size:11px;">PROBABILITÀ SEGNO 1</span><span style="color:#ffffff; width:33%; text-align:right;"><b>{p_2:.1f}%</b> (Segno 2)</span></div>
        <div class="stat-row-clean"><span style="color:#ffffff; width:33%; text-align:left;"><b>{analisi['tiri_c']}</b></span><span style="color:#94a3b8; width:33%; text-align:center; font-size:11px;">TIRI</span><span style="color:#ffffff; width:33%; text-align:right;"><b>{analisi['tiri_t']}</b></span></div>
        <div class="stat-row-clean"><span style="color:#ffffff; width:33%; text-align:left;"><b>{analisi['porta_c']}</b></span><span style="color:#94a3b8; width:33%; text-align:center; font-size:11px;">TIRI IN PORTA</span><span style="color:#ffffff; width:33%; text-align:right;"><b>{analisi['porta_t']}</b></span></div>
        <div class="stat-row-clean"><span style="color:#ffffff; width:33%; text-align:left;"><b>{analisi['falli_c']}</b></span><span style="color:#94a3b8; width:33%; text-align:center; font-size:11px;">FALLI</span><span style="color:#ffffff; width:33%; text-align:right;"><b>{analisi['falli_t']}</b></span></div>
        <div class="stat-row-clean"><span style="color:#ffffff; width:33%; text-align:left;"><b>{analisi['gialli_c']}</b></span><span style="color:#94a3b8; width:33%; text-align:center; font-size:11px;">GIALLI</span><span style="color:#ffffff; width:33%; text-align:right;"><b>{analisi['gialli_t']}</b></span></div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("</div>", unsafe_allow_html=True)
  st.markdown("<br>", unsafe_allow_html=True)

  # --- SEZIONE IN BASSO: GOL ATTESI (xG) E STATISTICHE PREVISTE (come nella foto) ---
  st.markdown(
      """
    <div style="background: linear-gradient(135deg, rgba(4, 47, 46, 0.9) 0%, rgba(6, 78, 59, 0.8) 100%); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.2);">
        <p style="text-align:center; font-size:11px; color:#6ee7b7; text-transform:uppercase; font-weight:bold; letter-spacing:1px; margin-bottom:15px;">STATISTICHE PREVISTE (GOL ATTESI xG)</p>
        <div style="display:flex; justify-content:space-between; align-items:center; padding: 0 20px;">
            <div style="text-align:center;">
                <h1 style="margin:0; color:#ffffff; font-size:36px;">{:.2f}</h1>
                <p style="margin:0; font-size:12px; color:#cbd5e1;">{casa}</p>
            </div>
            <div style="text-align:center; font-size:13px; color:#94a3b8; text-transform:uppercase; font-weight:bold;">
                GOL ATTESI
            </div>
            <div style="text-align:center;">
                <h1 style="margin:0; color:#ffffff; font-size:36px;">{:.2f}</h1>
                <p style="margin:0; font-size:12px; color:#cbd5e1;">{ospite}</p>
            </div>
        </div>
    </div>
    """.format(
          analisi["xg_f"], analisi["xg_s"]
      ),
      unsafe_allow_html=True,
  )

  # --- SEZIONE MARCATORI ---
  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown("### ⚽ Principali Firme Offensive")
  col_m1, col_m2 = st.columns(2)
  with col_m1:
    st.markdown(f"**{casa} - Capocannonieri:**")
    for p_name, goals in sorted(
        scorers.get(casa, []), key=lambda x: x[1], reverse=True
    )[:3]:
      st.markdown(f"- 👤 **{p_name}** ({goals} gol)")
  with col_m2:
    st.markdown(f"**{ospite} - Capocannonieri:**")
    for p_name, goals in sorted(
        scorers.get(ospite, []), key=lambda x: x[1], reverse=True
    )[:3]:
      st.markdown(f"- 👤 **{p_name}** ({goals} gol)")
