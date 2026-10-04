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
      del st.session_state["password"]  # Non memorizzare la password
    else:
      st.session_state["password_correct"] = False

  if "password_correct" not in st.session_state:
    # Prima esecuzione, mostra il campo password
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
    # Password errata, rimanda il campo e mostra errore
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
    # Password corretta.
    return True


if not check_password():
  st.stop()  # Interrompe l'esecuzione se la password non è corretta

# --- STYLING CSS AVANZATO: STILE CAMPO DA CALCIO E PULSANTI LEGA ---
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
    .badge-live {
        display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700;
        background-color: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(255, 255, 255, 0.3);
    }
    .badge-fallback {
        display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700;
        background-color: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(255, 255, 255, 0.3);
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

# --- INTESTAZIONE E SELETTORE COMPETIZIONE INTEGRATO ---
st.title("⚽ Football Match Center & Pronostici Pro")
st.markdown(
    "Modello avanzato con **loghi ufficiali, analisi tattica e simulazione"
    " Monte Carlo**."
)

competizioni = {
    "🇮🇹 Serie A": "SA",
    "🇬🇧 Premier": "PL",
    "🇪🇸 Liga": "PD",
    "🇩🇪 Bundesliga": "BL1",
    "🇫🇷 Ligue 1": "FL1",
    "🇪🇺 Champions": "CL",
}

# Selettore orizzontale integrato
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
        coeff_posizione = 1.8 - (idx_pos / max(1, tot_squadre - 1)) * 1.3
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

  return matches_future, history_matches, standings_dict, scorers_dict, teams_data


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
    desc_stile = (
        f"Ci si attende una gara giocata a viso aperto, con ritmi alti e spazi"
        f" concessi in fase difensiva. Entrambe le squadre ({casa} e {ospite})"
        f" hanno le doti per pungere con continuità e creare numerosi pericoli"
        f" nei sedici metri finali."
    )
  elif tot_xg <= 2.1:
    stile_match = (
        "🛡️ **Partita Tattica, Bloccata e a Prevalenza Difensiva**"
    )
    desc_stile = (
        f"Il modello individua i presupposti per una sfida tattica e molto"
        f" attenta. Le difese tenderanno a prevalere sugli attacchi, con pochi"
        f" spazi tra le linee e un ritmo controllato. Episodi o calci piazzati"
        f" potrebbero sbloccare il risultato."
    )
  else:
    stile_match = "⚖️ **Partita Equilibrata e di Gran Movimento a Metà Campo**"
    desc_stile = (
        f"Una gara dal canovaccio classico: fase di studio iniziale, duelli"
        f" intensi a centrocampo e tentativi di affondo ben bilanciati. Nessuna"
        f" delle due formazioni sembra in grado di schiacciantemente dominare"
        f" l'altra per intero."
    )

  if diff_xg > 0.8:
    dominatore = casa if xg_casa > xg_ospite else ospite
    sfavorito = ospite if xg_casa > xg_ospite else casa
    desc_inerzia = (
        f"Dal punto di vista del controllo territoriale, **{dominatore}**"
        f" parte con i favori del pronostico per imporre il proprio gioco,"
        f" mentre **{sfavorito}** dovrà agire principalmente di rimessa o sfruttare"
        f" le ripartenze."
    )
  else:
    desc_inerzia = (
        f"L'equilibrio dei valori in campo rende il match apertissimo a ogni"
        f" scenario, con ribaltamenti di fronte e inerzia che potrebbe"
        f" cambiare da un momento all'altro."
    )

  motivazione = (
      f"{stile_match}<br><br>{desc_stile}<br><br>{desc_inerzia}<br><br>"
      f"<span style='color:#6ee7b7;'>Dati chiave:</span> xG stimati"
      f" ({casa}: <b>{xg_casa}</b> vs {ospite}: <b>{xg_ospite}</b>) calcolati"
      " su classifica e forma."
  )

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


(
    matches_future,
    history_matches,
    standings,
    scorers,
    teams_data,
) = scarica_dati_completi(COMPETITION_CODE)

# Controllo se ci sono match disponibili per la lega selezionata
if not matches_future:
  st.markdown(
      f"""
        <div class="alert-box">
            <h3 style="margin:0 0 10px 0; color:#f87171;">⚠️ Nessun match disponibile per {scelta_comp_label}</h3>
            <p style="margin:0; font-size:14px; color:#cbd5e1;">
                Al momento l'API gratuita non restituisce partite programmate per questa competizione (potrebbe essere in pausa o non attiva sul piano free). 
                Ti consigliamo di selezionare <b>🇮🇹 Serie A</b> o <b>🇬🇧 Premier</b> che dispongono di calendari attivi.
            </p>
        </div>
    """,
      unsafe_allow_html=True,
  )
else:
  if history_matches:
    st.markdown(
        f'<span class="badge-live">🟢 Motore Pro Attivo ({scelta_comp_label}):'
        f" {len(history_matches)} match elaborati</span>",
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        '<span class="badge-fallback">🟡 Connessione limitata - Utilizzo dati'
        " standard</span>",
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

  col_sinistra, col_destra = st.columns([1.1, 1.4], gap="large")

  with col_sinistra:
    st.markdown(
        f'<div class="match-header">Scheda della Partita • Ore {orario}</div>',
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
          f"""
                <div class="team-box-home">
                    {logo_html_c}
                    <h3 style="margin:0; color:#ffffff; font-size:16px;">{casa}</h3>
                </div>
            """,
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
          f"""
                <div class="team-box-away">
                    {logo_html_o}
                    <h3 style="margin:0; color:#ffffff; font-size:16px;">{ospite}</h3>
                </div>
            """,
          unsafe_allow_html=True,
      )

    st.markdown("<br>", unsafe_allow_html=True)
    avvia_sim = st.button(
        "🚀 AVVIA SIMULAZIONE PRO & GENERA SCHEDINA",
        type="primary",
        use_container_width=True,
    )

  with col_destra:
    st.markdown(
        '<div class="match-header" style="text-align:center;">📊 Metriche'
        " Ponderate (Stagione, Avversari & Forma)</div>",
        unsafe_allow_html=True,
    )

    statistiche_mostrate = [
        (
            "GOL FATTI (Media Ponderata)",
            f"{analisi['media_gf_c']:.2f}",
            f"{analisi['media_gf_o']:.2f}",
        ),
        (
            "GOL SUBITI (Media Ponderata)",
            f"{analisi['media_gs_c']:.2f}",
            f"{analisi['media_gs_o']:.2f}",
        ),
        (
            "GOL ATTESI (xG)",
            f"{analisi['xg_f']:.2f}",
            f"{analisi['xg_s']:.2f}",
        ),
        ("TIRI STIMATI", f"{analisi['tiri_c']:.1f}", f"{analisi['tiri_t']:.1f}"),
        (
            "TIRI IN PORTA STIMATI",
            f"{analisi['porta_c']:.1f}",
            f"{analisi['porta_t']:.1f}",
        ),
    ]

    for label, val_c, val_t in statistiche_mostrate:
      st.markdown(
          f"""
                <div class="stat-row">
                    <span style="color: #ffffff; font-size: 15px; width: 30%; text-align: left; font-weight:700;">{val_c}</span>
                    <span style="color: #e2e8f0; font-size: 12px; width: 40%; text-align: center; letter-spacing: 0.5px;">{label}</span>
                    <span style="color: #ffffff; font-size: 15px; width: 30%; text-align: right; font-weight:700;">{val_t}</span>
                </div>
            """,
          unsafe_allow_html=True,
      )

  # --- SEZIONE TATTICA E DINAMICA DEL MATCH ---
  st.markdown(
      '<div class="match-header">📋 Tattica & Dinamica del Match</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      f"""
        <div class="motivation-card">
            <p style="margin:0; color:#f8fafc; font-size:15px; line-height:1.6;">
                {analisi['motivazione']}
            </p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  # --- SIMULAZIONE MONTE CARLO & SCHEDINA ---
  if avvia_sim:
    N_SIM = 1_000_000
    with st.spinner(
        "Elaborazione in corso di 1.000.000 di scenari avanzati su tutti i"
        " mercati..."
    ):
      gol_c = np.random.poisson(analisi["xg_f"], N_SIM)
      gol_t = np.random.poisson(analisi["xg_s"], N_SIM)

      p_1 = np.sum(gol_c > gol_t) / N_SIM * 100
      p_x = np.sum(gol_c == gol_t) / N_SIM * 100
      p_2 = np.sum(gol_c < gol_t) / N_SIM * 100
      p_1x = np.sum(gol_c >= gol_t) / N_SIM * 100
      p_x2 = np.sum(gol_c <= gol_t) / N_SIM * 100
      p_over15 = np.sum((gol_c + gol_t) >= 2) / N_SIM * 100
      p_over25 = np.sum((gol_c + gol_t) >= 3) / N_SIM * 100
      p_gol = np.sum((gol_c > 0) & (gol_t > 0)) / N_SIM * 100
      p_nogol = 100 - p_gol

      coppie = list(zip(gol_c, gol_t))
      ris_unici, counts = np.unique(coppie, axis=0, return_counts=True)
      ordinati = np.argsort(counts)[::-1]

      top_3 = []
      for i in range(min(3, len(ordinati))):
        r = ris_unici[ordinati[i]]
        prob = (counts[ordinati[i]] / N_SIM) * 100
        top_3.append((r[0], r[1], prob))

    st.markdown("---")
    st.subheader("🎯 Esito Finale & Pronostici Statistici Pro")

    col_e1, col_e2, col_e3 = st.columns(3)
    col_e1.metric(f"Vittoria ({casa})", f"{p_1:.2f}%")
    col_e2.metric("Pareggio (X)", f"{p_x:.2f}%")
    col_e3.metric(f"Vittoria ({ospite})", f"{p_2:.2f}%")

    candidati_giocata = []
    if p_gol > 52:
      candidati_giocata.append((
          "Goal (Entrambe a segno)",
          p_gol,
          (
              f"Entrambe le squadre mostrano una buona media realizzativa"
              f" recente, con il {p_gol:.1f}% di probabilità nei test."
          ),
      ))
    elif p_nogol > 52:
      candidati_giocata.append((
          "No Goal",
          p_nogol,
          (
              f"Almeno una delle due difese mostra lacune, con il"
              f" {p_nogol:.1f}% di No Goal."
          ),
      ))

    if p_over25 > 50:
      candidati_giocata.append((
          "Over 2.5 Gol",
          p_over25,
          (
              f"Il volume di tiri e xG stimati porta a pronosticare almeno 3 gol"
              f" totali ({p_over25:.1f}%)."
          ),
      ))
    else:
      p_under25 = 100 - p_over25
      if p_under25 > 50:
        candidati_giocata.append((
            "Under 2.5 Gol",
            p_under25,
            (
                f"Partita bloccata o difese attente: Under 2.5 probabile al"
                f" {p_under25:.1f}%."
            ),
        ))

    if p_1 > 48:
      candidati_giocata.append((
          f"1 (Vittoria {casa})",
          p_1,
          f"Il fattore campo spinge per il segno 1 ({p_1:.1f}%).",
      ))
    elif p_2 > 45:
      candidati_giocata.append((
          f"2 (Vittoria {ospite})",
          p_2,
          (
              f"La solidità in trasferta della squadra ospite emerge nel"
              f" {p_2:.1f}% dei test."
          ),
      ))
    elif p_1x > 70:
      candidati_giocata.append((
          f"1X Doppia Chance",
          p_1x,
          (
              f"Copertura solida per la squadra di casa ({p_1x:.1f}% di esiti"
              " favorevoli)."
          ),
      ))
    elif p_x2 > 70:
      candidati_giocata.append((
          f"X2 Doppia Chance",
          p_x2,
          (
              f"Copertura solida per la trasferta ({p_x2:.1f}% di esiti"
              " favorevoli)."
          ),
      ))

    if not candidati_giocata:
      candidati_giocata.append((
          "Over 1.5 Gol",
          p_over15,
          (
              f"Mercato conservativo: almeno 2 gol totali nel {p_over15:.1f}%"
              " dei casi."
          ),
      ))

    candidati_giocata.sort(key=lambda x: x[1], reverse=True)
    miglior_nome, miglior_prob, miglior_motivazione = candidati_giocata[0]

    affidabilita = (
        "Alta"
        if miglior_prob >= 70
        else ("Media / Buona" if miglior_prob >= 55 else "Studiata")
    )

    st.markdown(
        f"""
        <div class="bet-card">
            <h4 style="margin:0 0 8px 0; color:#34d399;">💡 Giocata Consigliata (Filtrata per Valore Statistico)</h4>
            <p style="margin:0 0 5px 0; font-size:20px; font-weight:bold; color:#ffffff;">🎯 {miglior_nome} ({miglior_prob:.1f}%)</p>
            <p style="margin:0 0 8px 0; font-size:13px; color:#cbd5e1;"><b>Analisi:</b> {miglior_motivazione}</p>
            <p style="margin:0; font-size:12px; color:#94a3b8;">Affidabilità del Modello: <span style="color:#34d399; font-weight:bold;">{affidabilita}</span></p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔥 Top 3 Risultati Esatti più Probabili")

    cols_res = st.columns(3)
    for i, (rc, ro, p) in enumerate(top_3):
      with cols_res[i]:
        st.markdown(
            f"""
                <div class="stat-card">
                    <span style="color:#ffffff; font-weight:bold; font-size:13px; letter-spacing:1px;"># {i+1} SCELTA</span>
                    <h2 style="margin:10px 0; color:#ffffff; font-size:28px;">{rc} - {ro}</h2>
                    <span style="color:#34d399; font-weight:600; font-size:14px;">Probabilità: {p:.2f}%</span>
                </div>
            """,
            unsafe_allow_html=True,
        )

  # --- SEZIONE MARCATORI ---
  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown("### ⚽ Principali Firme Offensive")
  col_m1, col_m2 = st.columns(2)
  with col_m1:
    st.markdown(f"**{casa} - Capocannonieri:**")
    marcatori_casa = scorers.get(casa, [])
    if marcatori_casa:
      for p_name, goals in sorted(
          marcatori_casa, key=lambda x: x[1], reverse=True
      )[:3]:
        st.markdown(f"- 👤 **{p_name}** ({goals} gol)")
    else:
      st.markdown("_Nessun marcatore registrato di recente._")
  with col_m2:
    st.markdown(f"**{ospite} - Capocannonieri:**")
    marcatori_ospite = scorers.get(ospite, [])
    if marcatori_ospite:
      for p_name, goals in sorted(
          marcatori_ospite, key=lambda x: x[1], reverse=True
      )[:3]:
        st.markdown(f"- 👤 **{p_name}** ({goals} gol)")
    else:
      st.markdown("_Nessun marcatore registrato di recente._")
