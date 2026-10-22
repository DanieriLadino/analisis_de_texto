import re
import html

import altair as alt
import pandas as pd
import streamlit as st
from textblob import TextBlob
from googletrans import Translator

# ─────────────────────────────────────────────────────────────
# Configuración de la página
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Analizador de Texto",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# Estilos
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Inter:wght@400;500;600&display=swap');

:root{
  --bg:#0f1020;
  --panel:#17182e;
  --panel-2:#1e2040;
  --line:#2c2f5a;
  --text:#ecebff;
  --muted:#9a9cc7;
  --accent:#ff7a59;
  --accent-2:#7c6cff;
  --pos:#3ddc97;
  --neg:#ff5d73;
  --neu:#ffc857;
}

html, body, [class*="css"], .stApp { font-family:'Inter',sans-serif; }
.stApp {
  background:
    radial-gradient(1200px 600px at 10% -10%, rgba(124,108,255,.18), transparent 60%),
    radial-gradient(900px 500px at 110% 10%, rgba(255,122,89,.14), transparent 60%),
    var(--bg);
  color:var(--text);
}
#MainMenu, footer, header[data-testid="stHeader"] {visibility:hidden;}
.block-container {padding-top:2rem; max-width:1200px;}

/* Hero */
.hero{
  border:1px solid var(--line);
  background:linear-gradient(135deg, rgba(124,108,255,.22), rgba(255,122,89,.12));
  border-radius:24px; padding:2.2rem 2.4rem; margin-bottom:1.6rem;
  position:relative; overflow:hidden;
}
.hero:after{
  content:""; position:absolute; right:-60px; top:-60px; width:220px; height:220px;
  border-radius:50%; background:radial-gradient(circle, rgba(255,122,89,.45), transparent 70%);
}
.hero h1{
  font-family:'Fraunces',serif; font-weight:800; font-size:2.8rem; line-height:1.05;
  margin:0 0 .5rem 0; color:var(--text); letter-spacing:-.02em;
}
.hero h1 span{ background:linear-gradient(90deg,var(--accent),var(--accent-2));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
.hero p{ color:var(--muted); font-size:1.05rem; margin:0 0 1rem 0; max-width:640px;}
.chips{display:flex; gap:.5rem; flex-wrap:wrap;}
.chip{ font-size:.82rem; padding:.35rem .8rem; border-radius:999px;
  background:rgba(255,255,255,.06); border:1px solid var(--line); color:var(--text);}

/* Tarjetas */
.card{
  background:var(--panel); border:1px solid var(--line); border-radius:18px;
  padding:1.3rem 1.4rem; height:100%;
}
.card .label{ color:var(--muted); font-size:.8rem; text-transform:uppercase; letter-spacing:.08em;}
.card .value{ font-family:'Fraunces',serif; font-size:2.3rem; font-weight:800; margin:.2rem 0;}
.card .sub{ font-size:.92rem; color:var(--muted);}

/* Medidor */
.gauge{ position:relative; height:12px; border-radius:999px; margin:.9rem 0 .4rem;
  background:linear-gradient(90deg,var(--neg),var(--neu) 50%,var(--pos)); }
.gauge.subj{ background:linear-gradient(90deg,#3a3d72,var(--accent-2)); }
.gauge .dot{ position:absolute; top:50%; width:22px; height:22px; border-radius:50%;
  transform:translate(-50%,-50%); background:#fff; border:4px solid var(--bg);
  box-shadow:0 0 0 2px rgba(255,255,255,.4);}
.scale{ display:flex; justify-content:space-between; font-size:.75rem; color:var(--muted);}

/* Frases */
.phrase{
  background:var(--panel); border:1px solid var(--line); border-left:5px solid var(--neu);
  border-radius:14px; padding:1rem 1.2rem; margin-bottom:.8rem;
}
.phrase.pos{border-left-color:var(--pos);}
.phrase.neg{border-left-color:var(--neg);}
.phrase .orig{ font-size:1rem; color:var(--text); margin-bottom:.35rem;}
.phrase .trans{ font-size:.88rem; color:var(--muted); font-style:italic;}
.badge{ float:right; font-size:.78rem; font-weight:600; padding:.2rem .6rem; border-radius:999px;
  background:rgba(255,255,255,.07); }

/* Textos lado a lado */
.textbox{ background:var(--panel); border:1px solid var(--line); border-radius:14px;
  padding:1rem 1.2rem; white-space:pre-wrap; max-height:360px; overflow:auto;
  font-size:.92rem; color:var(--text);}
.boxtitle{ font-weight:600; margin-bottom:.5rem; color:var(--muted); font-size:.85rem;
  text-transform:uppercase; letter-spacing:.06em;}

/* Controles de Streamlit */
.stTextArea textarea{
  background:var(--panel) !important; color:var(--text) !important;
  border:1px solid var(--line) !important; border-radius:16px !important; font-size:1rem !important;
}
.stButton > button{
  background:linear-gradient(90deg,var(--accent),var(--accent-2)); color:#fff; border:0;
  border-radius:12px; padding:.65rem 1.6rem; font-weight:600; transition:transform .15s, box-shadow .15s;
}
.stButton > button:hover{ transform:translateY(-2px); box-shadow:0 10px 24px rgba(124,108,255,.35); color:#fff;}
[data-testid="stSidebar"]{ background:var(--panel); border-right:1px solid var(--line);}
[data-testid="stFileUploader"] section{ background:var(--panel); border:1px dashed var(--line); border-radius:16px;}
.stTabs [data-baseweb="tab-list"]{ gap:.4rem;}
.stTabs [data-baseweb="tab"]{ background:var(--panel); border-radius:10px; padding:.5rem 1rem; border:1px solid var(--line);}
.stTabs [aria-selected="true"]{ background:var(--panel-2); border-color:var(--accent-2);}
h2, h3 { font-family:'Fraunces',serif; }
.foot{ text-align:center; color:var(--muted); font-size:.85rem; margin-top:3rem; }
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
# Lógica de análisis (igual que antes)
# ─────────────────────────────────────────────────────────────
STOP_WORDS = set("""
a al algo algunas algunos ante antes como con contra cual cuando de del desde donde durante e el ella
ellas ellos en entre era eras es esa esas ese eso esos esta estas este esto estos ha había han has hasta
he la las le les lo los me mi mía mías mío míos mis mucho muchos muy nada ni no nos nosotras nosotros
nuestra nuestras nuestro nuestros o os otra otras otro otros para pero poco por porque que quien quienes
qué se sea sean según si sido sin sobre sois somos son soy su sus suya suyas suyo suyos también tanto te
tenéis tenemos tener tengo ti tiene tienen todo todos tu tus tuya tuyas tuyo tuyos tú un una uno unos
vosotras vosotros vuestra vuestras vuestro vuestros y ya yo
about above after again against all am an and any are aren't as at be because been before being below
between both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each
few for from further had hadn't has hasn't have haven't having he'd he'll he's her here here's hers
herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's more
most mustn't my myself nor not of off on once only or other ought our ours ourselves out over own same
shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them
themselves then there there's these they they'd they'll they're they've this those through to too under
until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's
which while who who's whom why why's with would wouldn't you you'd you'll you're you've your yours
yourself yourselves
""".split())


def contar_palabras(texto):
    palabras = re.findall(r"\b\w+\b", texto.lower())
    filtradas = [p for p in palabras if p not in STOP_WORDS and len(p) > 2]
    contador = {}
    for p in filtradas:
        contador[p] = contador.get(p, 0) + 1
    return dict(sorted(contador.items(), key=lambda x: x[1], reverse=True)), filtradas


@st.cache_resource
def get_translator():
    return Translator()


def traducir_texto(texto):
    try:
        return get_translator().translate(texto, src="es", dest="en").text
    except Exception as e:
        st.error(f"Error al traducir: {e}")
        return texto


def dividir_frases(texto):
    return [f.strip() for f in re.split(r"[.!?]+", texto) if f.strip()]


def procesar_texto(texto):
    texto_ingles = traducir_texto(texto)
    blob = TextBlob(texto_ingles)
    originales, traducidas = dividir_frases(texto), dividir_frases(texto_ingles)
    frases = [{"original": o, "traducido": t} for o, t in zip(originales, traducidas)]
    contador, palabras = contar_palabras(texto_ingles)
    return {
        "sentimiento": blob.sentiment.polarity,
        "subjetividad": blob.sentiment.subjectivity,
        "frases": frases,
        "contador_palabras": contador,
        "palabras": palabras,
        "texto_original": texto,
        "texto_traducido": texto_ingles,
    }


# ─────────────────────────────────────────────────────────────
# Componentes visuales
# ─────────────────────────────────────────────────────────────
def etiqueta_sentimiento(s):
    if s > 0.05:
        return "Positivo", "😊", "var(--pos)", "pos"
    if s < -0.05:
        return "Negativo", "😟", "var(--neg)", "neg"
    return "Neutral", "😐", "var(--neu)", "neu"


def tarjeta_sentimiento(s):
    nombre, emoji, color, _ = etiqueta_sentimiento(s)
    pos = (s + 1) / 2 * 100
    st.markdown(
        f"""
<div class="card">
  <div class="label">Sentimiento</div>
  <div class="value" style="color:{color}">{emoji} {s:+.2f}</div>
  <div class="sub">El texto se percibe <b style="color:{color}">{nombre.lower()}</b></div>
  <div class="gauge"><div class="dot" style="left:{pos:.1f}%"></div></div>
  <div class="scale"><span>-1 negativo</span><span>0</span><span>+1 positivo</span></div>
</div>""",
        unsafe_allow_html=True,
    )


def tarjeta_subjetividad(v):
    texto = "Más opinión que hechos" if v > 0.5 else "Más hechos que opinión"
    icono = "💭" if v > 0.5 else "📋"
    st.markdown(
        f"""
<div class="card">
  <div class="label">Subjetividad</div>
  <div class="value" style="color:var(--accent-2)">{icono} {v:.2f}</div>
  <div class="sub">{texto}</div>
  <div class="gauge subj"><div class="dot" style="left:{v*100:.1f}%"></div></div>
  <div class="scale"><span>0 objetivo</span><span>1 subjetivo</span></div>
</div>""",
        unsafe_allow_html=True,
    )


def tarjeta_dato(label, valor, sub):
    st.markdown(
        f"""<div class="card"><div class="label">{label}</div>
        <div class="value">{valor}</div><div class="sub">{sub}</div></div>""",
        unsafe_allow_html=True,
    )


def grafico_palabras(contador, n=12):
    if not contador:
        st.info("No se encontraron palabras relevantes.")
        return
    df = pd.DataFrame(list(contador.items())[:n], columns=["palabra", "frecuencia"])
    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusEnd=8, height=22)
        .encode(
            x=alt.X("frecuencia:Q", title=None, axis=alt.Axis(grid=False, tickMinStep=1)),
            y=alt.Y("palabra:N", sort="-x", title=None),
            color=alt.Color(
                "frecuencia:Q",
                scale=alt.Scale(range=["#7c6cff", "#ff7a59"]),
                legend=None,
            ),
            tooltip=["palabra", "frecuencia"],
        )
        .properties(height=max(220, 34 * len(df)))
        .configure_view(strokeWidth=0)
        .configure(background="transparent")
        .configure_axis(labelColor="#ecebff", labelFontSize=13, domain=False, tickColor="transparent")
    )
    st.altair_chart(chart, use_container_width=True)


def mostrar_resultados(r):
    n_palabras = len(re.findall(r"\b\w+\b", r["texto_original"]))
    c1, c2, c3, c4 = st.columns([1.3, 1.3, 1, 1])
    with c1:
        tarjeta_sentimiento(r["sentimiento"])
    with c2:
        tarjeta_subjetividad(r["subjetividad"])
    with c3:
        tarjeta_dato("Palabras", n_palabras, "en el texto original")
    with c4:
        tarjeta_dato("Frases", len(r["frases"]), "detectadas")

    st.write("")
    tab1, tab2, tab3 = st.tabs(["🔠 Palabras clave", "💬 Frases", "🌐 Traducción"])

    with tab1:
        grafico_palabras(r["contador_palabras"])

    with tab2:
        if not r["frases"]:
            st.info("No se detectaron frases.")
        for i, f in enumerate(r["frases"][:10], 1):
            try:
                s = TextBlob(f["traducido"]).sentiment.polarity
            except Exception:
                s = 0.0
            nombre, emoji, color, clase = etiqueta_sentimiento(s)
            st.markdown(
                f"""
<div class="phrase {clase}">
  <span class="badge" style="color:{color}">{emoji} {s:+.2f}</span>
  <div class="orig"><b>{i}.</b> {html.escape(f['original'])}</div>
  <div class="trans">{html.escape(f['traducido'])}</div>
</div>""",
                unsafe_allow_html=True,
            )

    with tab3:
        a, b = st.columns(2)
        with a:
            st.markdown(
                f'<div class="boxtitle">🇪🇸 Original</div><div class="textbox">{html.escape(r["texto_original"])}</div>',
                unsafe_allow_html=True,
            )
        with b:
            st.markdown(
                f'<div class="boxtitle">🇬🇧 Inglés</div><div class="textbox">{html.escape(r["texto_traducido"])}</div>',
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────────────────────
# Interfaz
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="hero">
  <h1>Lee lo que tu texto <span>siente</span></h1>
  <p>Pega un texto en español o sube un archivo. Lo traducimos, medimos su tono y te mostramos
  las palabras y frases que lo definen.</p>
  <div class="chips">
    <span class="chip">😊 Sentimiento</span>
    <span class="chip">💭 Subjetividad</span>
    <span class="chip">🔠 Palabras clave</span>
    <span class="chip">🌐 Traducción ES → EN</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## ⚙️ Opciones")
    modo = st.radio("Modo de entrada", ["✍️ Texto directo", "📄 Archivo de texto"])
    st.markdown("---")
    st.markdown(
        """
**¿Cómo leer los resultados?**

- **Sentimiento**: de -1 (muy negativo) a +1 (muy positivo)
- **Subjetividad**: de 0 (objetivo) a 1 (subjetivo)

<small>El análisis se hace sobre la traducción al inglés, que es donde TextBlob funciona mejor.</small>
""",
        unsafe_allow_html=True,
    )

texto = None
if modo.startswith("✍️"):
    entrada = st.text_area(
        "Tu texto",
        height=200,
        placeholder="Escribe o pega aquí el texto que quieres analizar…",
        label_visibility="collapsed",
    )
    if st.button("✨ Analizar texto"):
        if entrada.strip():
            texto = entrada
        else:
            st.warning("Escribe algún texto para analizar.")
else:
    archivo = st.file_uploader("Sube un archivo", type=["txt", "csv", "md"], label_visibility="collapsed")
    if archivo is not None:
        try:
            contenido = archivo.getvalue().decode("utf-8")
            with st.expander("👀 Vista previa del archivo"):
                st.text(contenido[:1000] + ("…" if len(contenido) > 1000 else ""))
            if st.button("✨ Analizar archivo"):
                texto = contenido
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

if texto:
    with st.spinner("Traduciendo y analizando…"):
        st.session_state["resultados"] = procesar_texto(texto)

if "resultados" in st.session_state:
    mostrar_resultados(st.session_state["resultados"])

st.markdown(
    '<div class="foot">Hecho con ❤️ usando Streamlit y TextBlob</div>',
    unsafe_allow_html=True,
)
