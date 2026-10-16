import html
import streamlit as st


# ============================================================
# GLOBAL APPLICATION CSS
# ============================================================

APP_CSS = r"""
<style>

:root {
  --ink: #102a43;
  --ink-soft: #334e68;
  --muted: #6b7f93;

  --navy: #0b2438;
  --navy-2: #103b50;

  --teal: #0f8b8d;
  --teal-2: #1bb3a9;
  --cyan: #76d7d0;

  --ice: #eef8f7;
  --sky: #edf5fb;

  --amber: #f3b34c;
  --coral: #e7775b;

  --card: rgba(255,255,255,.94);
  --border: #dce7ef;

  --shadow:
    0 14px 38px rgba(16, 42, 67, .08);
}


/* ============================================================
   GLOBAL TYPOGRAPHY
   ============================================================ */

html,
body,
[class*="css"] {
  font-family:
    Inter,
    ui-sans-serif,
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;
}


/* ============================================================
   APPLICATION BACKGROUND
   ============================================================ */

[data-testid="stAppViewContainer"] {
  background:
    radial-gradient(
      circle at 82% 8%,
      rgba(27,179,169,.10),
      transparent 22%
    ),
    radial-gradient(
      circle at 8% 26%,
      rgba(76,139,190,.08),
      transparent 20%
    ),
    linear-gradient(
      180deg,
      #f8fbfd 0%,
      #f5f9fc 100%
    );
}


[data-testid="stHeader"] {
  background: rgba(248,251,253,.72);
  backdrop-filter: blur(10px);
}


.block-container {
  max-width: 1450px;
  padding-top: 1.5rem;
  padding-bottom: 4rem;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
  background:
    linear-gradient(
      180deg,
      #0b2438 0%,
      #0d3148 60%,
      #0b2438 100%
    );

  border-right:
    1px solid rgba(255,255,255,.08);
}


section[data-testid="stSidebar"] * {
  color: #e9f4f7;
}


section[data-testid="stSidebar"] hr {
  border-color:
    rgba(255,255,255,.12);
}


[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNavItems"] a {
  border-radius: 12px;
  margin: .15rem .45rem;
  transition: .18s ease;
}


[data-testid="stSidebarNav"] a:hover,
[data-testid="stSidebarNavItems"] a:hover {
  background:
    rgba(118,215,208,.10);
}


[data-testid="stSidebarNav"] a[aria-current="page"],
[data-testid="stSidebarNavItems"] a[aria-current="page"] {
  background:
    rgba(118,215,208,.16);

  border:
    1px solid rgba(118,215,208,.20);
}


/* ============================================================
   SIDEBAR BRAND
   ============================================================ */

.sidebar-brand {
  padding:
    .4rem .35rem .2rem .35rem;
}


.sidebar-brand .brand-mark {

  width: 42px;
  height: 42px;

  border-radius: 13px;

  display: inline-flex;
  align-items: center;
  justify-content: center;

  background:
    linear-gradient(
      135deg,
      #1bb3a9,
      #76d7d0
    );

  color: #082537 !important;

  font-weight: 900;
  font-size: 1.15rem;

  box-shadow:
    0 10px 25px
    rgba(27,179,169,.22);

  margin-bottom: .75rem;
}


.sidebar-brand .brand-title {

  font-size: 1rem;
  font-weight: 800;
  line-height: 1.2;

  color: white !important;
}


.sidebar-brand .brand-copy {

  color: #aec3d0 !important;

  font-size: .78rem;
  line-height: 1.55;

  margin-top: .4rem;
}


.sidebar-note {

  margin:
    1rem .35rem 0 .35rem;

  padding:
    .8rem .85rem;

  border-radius: 13px;

  background:
    rgba(255,255,255,.055);

  border:
    1px solid rgba(255,255,255,.08);

  color:
    #bdd0da !important;

  font-size: .72rem;
  line-height: 1.55;
}


/* ============================================================
   HERO
   ============================================================ */

.hero-shell {

  position: relative;
  overflow: hidden;

  background:
    linear-gradient(
      120deg,
      #0a2941 0%,
      #0d5360 56%,
      #119b91 100%
    );

  border-radius: 28px;

  padding:
    2.35rem
    2.65rem
    2.25rem
    2.65rem;

  box-shadow:
    0 24px 60px
    rgba(12,54,76,.20);

  margin-bottom: 1.6rem;

  min-height: 250px;
}


.hero-shell:before {

  content: "";

  position: absolute;

  width: 330px;
  height: 330px;

  right: -80px;
  top: -110px;

  border-radius: 50%;

  background:
    radial-gradient(
      circle,
      rgba(118,215,208,.32),
      rgba(118,215,208,0) 68%
    );
}


.hero-shell:after {

  content: "";

  position: absolute;

  width: 220px;
  height: 220px;

  right: 150px;
  bottom: -155px;

  border-radius: 50%;

  border:
    1px solid
    rgba(255,255,255,.15);

  box-shadow:
    0 0 0 32px
      rgba(255,255,255,.025),
    0 0 0 66px
      rgba(255,255,255,.018);
}


.hero-kicker {

  display: inline-flex;
  align-items: center;

  gap: .45rem;

  background:
    rgba(255,255,255,.10);

  border:
    1px solid
    rgba(255,255,255,.15);

  border-radius: 999px;

  color: #d8fffb;

  font-size: .74rem;
  font-weight: 800;

  letter-spacing: .09em;

  text-transform: uppercase;

  padding:
    .42rem .72rem;

  margin-bottom: 1rem;
}


.hero-title {

  position: relative;
  z-index: 1;

  color: white;

  font-size:
    clamp(
      2.15rem,
      4vw,
      4rem
    );

  font-weight: 850;

  line-height: 1.03;

  letter-spacing: -.04em;

  max-width: 900px;

  margin: 0;
}


.hero-subtitle {

  position: relative;
  z-index: 1;

  color: #d6e8ee;

  font-size: 1.04rem;

  line-height: 1.7;

  max-width: 850px;

  margin-top: 1rem;
}


.hero-pills {

  position: relative;
  z-index: 1;

  display: flex;
  flex-wrap: wrap;

  gap: .55rem;

  margin-top: 1.25rem;
}


.hero-pill {

  background:
    rgba(255,255,255,.095);

  border:
    1px solid
    rgba(255,255,255,.14);

  color: #edfafa;

  border-radius: 999px;

  padding:
    .43rem .68rem;

  font-size: .75rem;

  font-weight: 650;
}


/* ============================================================
   PAGE HEADER
   ============================================================ */

.page-eyebrow {

  color: var(--teal);

  font-weight: 850;

  font-size: .74rem;

  letter-spacing: .10em;

  text-transform: uppercase;

  margin-bottom: .35rem;
}


.page-title {

  color: var(--ink);

  font-weight: 850;

  letter-spacing: -.035em;

  font-size:
    clamp(
      2rem,
      3vw,
      3.25rem
    );

  line-height: 1.08;

  margin: 0;
}


.page-subtitle {

  color: var(--muted);

  font-size: .98rem;

  line-height: 1.65;

  max-width: 900px;

  margin-top: .55rem;

  margin-bottom: 1.25rem;
}


/* ============================================================
   SECTION HEADER
   ============================================================ */

.section-head {

  display: flex;

  align-items: center;

  gap: .7rem;

  margin:
    1.8rem
    0
    .9rem
    0;
}


.section-number {

  width: 29px;
  height: 29px;

  display: inline-flex;

  align-items: center;
  justify-content: center;

  border-radius: 9px;

  background: #dff5f3;

  color: #0b7475;

  font-size: .78rem;

  font-weight: 900;
}


.section-title {

  color: var(--ink);

  font-size: 1.28rem;

  font-weight: 830;

  letter-spacing: -.02em;
}


.section-copy {

  color: var(--muted);

  font-size: .82rem;

  margin-top: -.5rem;

  margin-bottom: .8rem;
}


/* ============================================================
   METRIC CARDS
   ============================================================ */

.metric-card {

  height: 100%;

  min-height: 126px;

  padding:
    1.05rem 1.1rem;

  border-radius: 18px;

  background: var(--card);

  border:
    1px solid
    var(--border);

  box-shadow:
    var(--shadow);

  position: relative;

  overflow: hidden;
}


.metric-card:after {

  content: "";

  position: absolute;

  top: 0;
  right: 0;

  width: 58px;
  height: 58px;

  border-radius:
    0 0 0 58px;

  background:
    rgba(15,139,141,.055);
}


.metric-top {

  display: flex;

  align-items: center;

  justify-content:
    space-between;

  gap: .5rem;
}


.metric-icon {

  width: 34px;
  height: 34px;

  display: inline-flex;

  align-items: center;

  justify-content: center;

  border-radius: 11px;

  background: #e8f7f6;

  font-size: 1rem;
}


.metric-label {

  color: var(--muted);

  font-size: .73rem;

  font-weight: 700;

  line-height: 1.3;

  text-transform:
    uppercase;

  letter-spacing: .04em;
}


.metric-value {

  color: var(--ink);

  font-size: 1.82rem;

  font-weight: 850;

  letter-spacing: -.035em;

  line-height: 1.05;

  margin-top: .8rem;
}


.metric-note {

  color: #8091a2;

  font-size: .72rem;

  margin-top: .38rem;
}


/* ============================================================
   STORY CARDS
   ============================================================ */

.story-card {

  background:
    linear-gradient(
      135deg,
      #ffffff 0%,
      #f6fbfb 100%
    );

  border:
    1px solid
    var(--border);

  border-radius: 20px;

  box-shadow:
    var(--shadow);

  padding:
    1.3rem 1.4rem;

  height: 100%;
}


.story-kicker {

  color: var(--teal);

  text-transform:
    uppercase;

  letter-spacing: .09em;

  font-size: .68rem;

  font-weight: 850;

  margin-bottom: .45rem;
}


.story-title {

  color: var(--ink);

  font-size: 1.1rem;

  font-weight: 820;

  line-height: 1.3;
}


.story-copy {

  color:
    var(--ink-soft);

  font-size: .84rem;

  line-height: 1.62;

  margin-top: .6rem;
}


/* ============================================================
   NAVIGATION CARDS
   ============================================================ */

.nav-card {

  height: 100%;

  min-height: 176px;

  border-radius: 22px;

  padding:
    1.25rem 1.3rem;

  background: white;

  border:
    1px solid
    var(--border);

  box-shadow:
    var(--shadow);

  transition:
    transform .18s ease,
    box-shadow .18s ease;
}


.nav-card:hover {

  transform:
    translateY(-3px);

  box-shadow:
    0 19px 45px
    rgba(16,42,67,.12);
}


.nav-icon {

  width: 42px;
  height: 42px;

  border-radius: 13px;

  background:
    linear-gradient(
      135deg,
      #dff5f3,
      #e7f3fb
    );

  display: inline-flex;

  align-items: center;

  justify-content: center;

  font-size: 1.2rem;
}


.nav-title {

  color: var(--ink);

  font-weight: 820;

  font-size: 1rem;

  margin-top: .9rem;
}


.nav-copy {

  color: var(--muted);

  font-size: .78rem;

  line-height: 1.55;

  margin-top: .35rem;
}


/* ============================================================
   STATUS CHIPS
   ============================================================ */

.status-row {

  display: flex;

  flex-wrap: wrap;

  gap: .48rem;

  margin:
    .4rem 0
    .7rem 0;
}


.status-chip {

  display: inline-flex;

  align-items: center;

  gap: .35rem;

  padding:
    .42rem .62rem;

  border-radius: 999px;

  border:
    1px solid #d5e5ec;

  background: #f8fbfd;

  color: #385369;

  font-size: .73rem;

  font-weight: 700;
}


.status-chip.good {

  background: #e8f7f3;

  color: #176b62;

  border-color: #ccece5;
}


.status-chip.warn {

  background: #fff6df;

  color: #895f13;

  border-color: #f5e0ad;
}


.status-chip.neutral {

  background: #eef4f8;

  color: #48657b;

  border-color: #dce7ef;
}


/* ============================================================
   CALLOUT
   ============================================================ */

.callout {

  border-radius: 18px;

  padding:
    1.05rem 1.15rem;

  border:
    1px solid #cfe4e7;

  background:
    linear-gradient(
      135deg,
      #eaf8f6 0%,
      #eff7fb 100%
    );

  color: #284b5e;

  font-size: .86rem;

  line-height: 1.65;
}


.callout strong {
  color: #0e5961;
}


/* ============================================================
   PROCESS RAIL
   ============================================================ */

.process-wrap {

  display: grid;

  grid-template-columns:
    repeat(
      4,
      minmax(0, 1fr)
    );

  gap: .75rem;

  margin:
    .8rem 0
    1.4rem 0;
}


.process-step {

  padding:
    .85rem .95rem;

  border-radius: 16px;

  background: white;

  border:
    1px solid
    var(--border);

  box-shadow:
    0 8px 24px
    rgba(16,42,67,.055);

  min-height: 145px;
}


.process-step .num {

  color: var(--teal);

  font-weight: 900;

  font-size: .72rem;
}


.process-step .label {

  color: var(--ink);

  font-weight: 820;

  margin-top: .18rem;

  font-size: .92rem;
}


.process-step .copy {

  color: var(--muted);

  font-size: .71rem;

  line-height: 1.45;

  margin-top: .28rem;
}


/* ============================================================
   NATIVE STREAMLIT COMPONENTS
   ============================================================ */

[data-testid="stVerticalBlockBorderWrapper"] {

  border-color:
    var(--border) !important;

  border-radius:
    18px !important;

  box-shadow:
    0 10px 30px
    rgba(16,42,67,.045);

  background:
    rgba(255,255,255,.76);
}


[data-testid="stDataFrame"] {

  border-radius: 14px;

  overflow: hidden;

  border:
    1px solid
    var(--border);
}


div[data-baseweb="select"] > div,
[data-testid="stSelectbox"]
div[data-baseweb="select"] > div {

  border-radius:
    12px !important;
}


.stButton > button,
.stLinkButton > a {

  border-radius:
    12px !important;

  font-weight:
    750 !important;
}


/* ============================================================
   PLOTLY CHARTS
   ============================================================ */

[data-testid="stPlotlyChart"] {

  border-radius: 18px;

  overflow: hidden;
}


/* ============================================================
   FOOTER
   ============================================================ */

footer {
  visibility: hidden;
}


/* ============================================================
   RESPONSIVE DESIGN
   ============================================================ */

@media (max-width: 900px) {

  .hero-shell {
    padding:
      1.8rem 1.5rem;

    border-radius: 22px;
  }

  .process-wrap {
    grid-template-columns:
      1fr 1fr;
  }
}


@media (max-width: 600px) {

  .process-wrap {
    grid-template-columns:
      1fr;
  }

}

</style>
"""


# ============================================================
# APPLICATION BOOTSTRAP
# ============================================================

def bootstrap_app(
    title="Regional Innovation Explorer",
    icon="🌐"
):

    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        APP_CSS,
        unsafe_allow_html=True
    )


# ============================================================
# SIDEBAR BRAND
# ============================================================

def sidebar_brand():

    st.sidebar.markdown(
        """
<div class="sidebar-brand">
    <div class="brand-mark">RI</div>
    <div class="brand-title">
        Regional Innovation Explorer
    </div>
    <div class="brand-copy">
        Interactive county intelligence from technological
        specialization, predictive modelling and spatial diffusion.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        """
<div class="sidebar-note">
    <b>Interpretation boundary</b><br>
    Results are descriptive and predictive.
    They support screening and diagnosis,
    not causal policy claims.
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# HERO
# ============================================================

def hero(
    eyebrow,
    title,
    subtitle,
    pills=None
):

    pills = pills or []

    pill_html = "".join(
        (
            '<span class="hero-pill">'
            f'{html.escape(str(p))}'
            '</span>'
        )
        for p in pills
    )

    hero_html = (
        '<div class="hero-shell">'
        f'<div class="hero-kicker">✦ {html.escape(str(eyebrow))}</div>'
        f'<h1 class="hero-title">{html.escape(str(title))}</h1>'
        f'<div class="hero-subtitle">{html.escape(str(subtitle))}</div>'
        f'<div class="hero-pills">{pill_html}</div>'
        '</div>'
    )

    st.markdown(
        hero_html,
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE HEADER
# ============================================================

def page_header(
    eyebrow,
    title,
    subtitle
):

    page_html = (
        f'<div class="page-eyebrow">{html.escape(str(eyebrow))}</div>'
        f'<h1 class="page-title">{html.escape(str(title))}</h1>'
        f'<div class="page-subtitle">{html.escape(str(subtitle))}</div>'
    )

    st.markdown(
        page_html,
        unsafe_allow_html=True,
    )


# ============================================================
# SECTION HEADER
# ============================================================

def section_header(
    number,
    title,
    copy=None
):

    copy_html = ""

    if copy:
        copy_html = (
            '<div class="section-copy">'
            f'{html.escape(str(copy))}'
            '</div>'
        )

    section_html = (
        '<div class="section-head">'
        '<span class="section-number">'
        f'{html.escape(str(number))}'
        '</span>'
        '<span class="section-title">'
        f'{html.escape(str(title))}'
        '</span>'
        '</div>'
        f'{copy_html}'
    )

    st.markdown(
        section_html,
        unsafe_allow_html=True,
    )


# ============================================================
# METRIC CARD
# ============================================================

def metric_card(
    label,
    value,
    icon="•",
    note=None
):

    note_html = ""

    if note:
        note_html = (
            '<div class="metric-note">'
            f'{html.escape(str(note))}'
            '</div>'
        )

    metric_html = (
        '<div class="metric-card">'
        '<div class="metric-top">'
        '<div class="metric-label">'
        f'{html.escape(str(label))}'
        '</div>'
        '<div class="metric-icon">'
        f'{html.escape(str(icon))}'
        '</div>'
        '</div>'
        '<div class="metric-value">'
        f'{html.escape(str(value))}'
        '</div>'
        f'{note_html}'
        '</div>'
    )

    st.markdown(
        metric_html,
        unsafe_allow_html=True,
    )


# ============================================================
# STORY CARD
# ============================================================

def story_card(
    kicker,
    title,
    copy
):

    story_html = (
        '<div class="story-card">'
        '<div class="story-kicker">'
        f'{html.escape(str(kicker))}'
        '</div>'
        '<div class="story-title">'
        f'{html.escape(str(title))}'
        '</div>'
        '<div class="story-copy">'
        f'{html.escape(str(copy))}'
        '</div>'
        '</div>'
    )

    st.markdown(
        story_html,
        unsafe_allow_html=True,
    )


# ============================================================
# NAVIGATION CARD
# ============================================================

def nav_card(
    icon,
    title,
    copy
):

    nav_html = (
        '<div class="nav-card">'
        '<div class="nav-icon">'
        f'{html.escape(str(icon))}'
        '</div>'
        '<div class="nav-title">'
        f'{html.escape(str(title))}'
        '</div>'
        '<div class="nav-copy">'
        f'{html.escape(str(copy))}'
        '</div>'
        '</div>'
    )

    st.markdown(
        nav_html,
        unsafe_allow_html=True,
    )


# ============================================================
# STATUS CHIPS
# ============================================================

def status_chips(items):

    chips = "".join(
        (
            '<span class="status-chip '
            f'{html.escape(str(css_class))}'
            '">'
            f'{html.escape(str(label))}'
            '</span>'
        )
        for label, css_class in items
    )

    status_html = (
        '<div class="status-row">'
        f'{chips}'
        '</div>'
    )

    st.markdown(
        status_html,
        unsafe_allow_html=True
    )


# ============================================================
# CALLOUT
# ============================================================

def callout(text):

    callout_html = (
        '<div class="callout">'
        f'{text}'
        '</div>'
    )

    st.markdown(
        callout_html,
        unsafe_allow_html=True
    )


# ============================================================
# PROCESS RAIL
#
# IMPORTANT:
# The HTML is intentionally constructed as one continuous
# string. This prevents Streamlit / Markdown from interpreting
# indented HTML blocks as literal code.
# ============================================================

def process_rail(steps):

    cards = []

    for i, (title, copy) in enumerate(
        steps,
        start=1
    ):

        card_html = (
            '<div class="process-step">'
            '<div class="num">'
            f'{i:02d}'
            '</div>'
            '<div class="label">'
            f'{html.escape(str(title))}'
            '</div>'
            '<div class="copy">'
            f'{html.escape(str(copy))}'
            '</div>'
            '</div>'
        )

        cards.append(
            card_html
        )

    rail_html = (
        '<div class="process-wrap">'
        + "".join(cards)
        + '</div>'
    )

    st.markdown(
        rail_html,
        unsafe_allow_html=True
    )


# ============================================================
# METHOD NOTE
# ============================================================

def method_note(text):

    with st.expander(
        "ℹ️ Method & interpretation note"
    ):

        st.markdown(
            text
        )
