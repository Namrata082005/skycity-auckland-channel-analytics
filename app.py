from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="SkyCity Channel Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Professional sidebar behavior for Streamlit Cloud:
# - No fixed sidebar width, so collapse/expand stays native and the main dashboard
#   automatically returns to full width.
# - Filters default to All without showing many selected chips.
# - If the user selects items manually, chips wrap cleanly instead of getting cut.
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    overflow-x: hidden !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] {
    width: 100% !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    flex-wrap: wrap !important;
    align-items: flex-start !important;
    overflow: visible !important;
    min-height: 44px !important;
    height: auto !important;
}

section[data-testid="stSidebar"] div[data-baseweb="tag"] {
    max-width: 100% !important;
    width: auto !important;
    height: auto !important;
    min-height: 30px !important;
    margin: 3px 4px 3px 0 !important;
    padding: 4px 8px !important;
    border-radius: 8px !important;
    white-space: normal !important;
    overflow: visible !important;
}

section[data-testid="stSidebar"] div[data-baseweb="tag"] span {
    max-width: none !important;
    width: auto !important;
    overflow: visible !important;
    text-overflow: clip !important;
    white-space: normal !important;
    line-height: 1.25 !important;
}

section[data-testid="stSidebar"] input {
    min-width: 120px !important;
}
</style>
""", unsafe_allow_html=True)


CHANNELS = {
    "In-Store": {
        "orders": "InStoreOrders",
        "revenue": "InStoreRevenue",
        "profit": "InStoreNetProfit",
        "share": "Final_InStoreShare",
        "type": "In-Store",
    },
    "Uber Eats": {
        "orders": "UberEatsOrders",
        "revenue": "UberEatsRevenue",
        "profit": "UberEatsNetProfit",
        "share": "Final_UE_share",
        "type": "Delivery",
    },
    "DoorDash": {
        "orders": "DoorDashOrders",
        "revenue": "DoorDashRevenue",
        "profit": "DoorDashNetProfit",
        "share": "Final_DD_share",
        "type": "Delivery",
    },
    "Self Delivery": {
        "orders": "SelfDeliveryOrders",
        "revenue": "SelfDeliveryRevenue",
        "profit": "SelfDeliveryNetProfit",
        "share": "Final_SD_share",
        "type": "Delivery",
    },
}

ORDER_COLS = [meta["orders"] for meta in CHANNELS.values()]
SHARE_COLS = [meta["share"] for meta in CHANNELS.values()]
AGGREGATOR_COLS = ["UberEatsOrders", "DoorDashOrders"]
CHANNEL_COLORS = {
    "In-Store": "#2563eb",
    "Uber Eats": "#0f766e",
    "DoorDash": "#7c3aed",
    "Self Delivery": "#d97706",
    "Delivery": "#64748b",
}
RISK_COLORS = {
    "High Risk": "#b42318",
    "Medium Risk": "#d97706",
    "Low Risk": "#2563eb",
}
PROFESSIONAL_SEQUENCE = ["#2563eb", "#0f766e", "#7c3aed", "#d97706", "#64748b", "#0891b2"]

px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = PROFESSIONAL_SEQUENCE


def show_chart(fig: go.Figure) -> None:
    dark_mode = st.session_state.get("appearance_mode") == "Executive Dark"
    paper = "#111827" if dark_mode else "#ffffff"
    plot = "#111827" if dark_mode else "#ffffff"
    text = "#e5e7eb" if dark_mode else "#111827"
    axis = "#cbd5e1" if dark_mode else "#334155"
    grid = "#334155" if dark_mode else "#e5e7eb"
    line = "#475569" if dark_mode else "#cbd5e1"
    fig.update_layout(
        template="plotly_dark" if dark_mode else "plotly_white",
        paper_bgcolor=paper,
        plot_bgcolor=plot,
        font=dict(color=text, family="Arial"),
        title=dict(font=dict(color=text, size=17)),
        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            font=dict(color=text),
        ),
        margin=dict(l=30, r=24, t=58, b=36),
    )
    fig.update_xaxes(
        color=axis,
        gridcolor=grid,
        linecolor=line,
        zerolinecolor=line,
        title_font_color=axis,
    )
    fig.update_yaxes(
        color=axis,
        gridcolor=grid,
        linecolor=line,
        zerolinecolor=line,
        title_font_color=axis,
    )
    st.plotly_chart(fig, width="stretch", theme=None)


def show_table(data: pd.DataFrame, height: int | None = None) -> None:
    max_height = f"max-height:{height}px;" if height else ""
    html = data.to_html(index=False, escape=True, classes="light-data-table")
    st.markdown(
        f"""
        <div class="light-table-wrap" style="{max_height}">
            {html}
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <style>
    :root {
        --ink: #111827;
        --muted: #475569;
        --line: #d7dde7;
        --brand: #1d4ed8;
        --brand-dark: #1e3a8a;
        --accent: #b7791f;
        --danger: #b42318;
        --success: #047857;
        --soft: #f5f7fb;
        --panel: #ffffff;
    }
    .stApp {
        background: #f3f6fb;
        color: var(--ink);
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #d8dee8;
    }
    section[data-testid="stSidebar"] * {
        color: #111827;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1e3a8a !important;
        font-weight: 760;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stCaptionContainer {
        color: #475569 !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #f8fafc !important;
        border-radius: 8px;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #f8fafc !important;
        border-color: #cbd5e1 !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] div {
        background-color: #f8fafc !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] span,
    section[data-testid="stSidebar"] div[data-baseweb="tag"] span,
    section[data-testid="stSidebar"] input {
        color: #111827 !important;
    }
    .stMultiSelect [data-baseweb="tag"],
    section[data-testid="stSidebar"] div[data-baseweb="tag"] {
        background-color: #dbeafe !important;
        border: 1px solid #bfdbfe !important;
        border-radius: 7px !important;
    }
    .stMultiSelect [data-baseweb="tag"] span,
    section[data-testid="stSidebar"] div[data-baseweb="tag"] span {
        color: #1e3a8a !important;
        font-weight: 650;
    }
    .stMultiSelect [data-baseweb="tag"] svg,
    section[data-testid="stSidebar"] div[data-baseweb="tag"] svg {
        fill: #1e3a8a !important;
    }
    section[data-testid="stSidebar"] button {
        color: #334155 !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        background: #f8fafc;
        border: 1px solid #d8dee8;
        border-radius: 8px;
        padding: 4px 8px;
        margin-bottom: 5px;
    }
    h1, h2, h3, h4, h5, h6, p, label, span {
        letter-spacing: 0;
    }
    .hero {
        background: linear-gradient(135deg, #ffffff 0%, #eef4ff 52%, #f8fafc 100%);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 22px 24px;
        margin-bottom: 18px;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
    }
    .hero h1 {
        color: var(--ink);
        font-size: 32px;
        line-height: 1.1;
        margin: 0 0 8px 0;
        letter-spacing: 0;
    }
    .hero p {
        color: var(--muted);
        font-size: 15px;
        margin: 0;
    }

    .visual-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 16px;
        margin: 4px 0 22px;
    }
    .visual-card {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.07);
    }
    .visual-card img {
        width: 100%;
        height: 165px;
        object-fit: cover;
        display: block;
    }
    .visual-card-body {
        padding: 13px 15px 15px;
    }
    .visual-card-title {
        color: var(--brand-dark);
        font-size: 16px;
        font-weight: 760;
        margin-bottom: 5px;
    }
    .visual-card-text {
        color: var(--muted);
        font-size: 13px;
        line-height: 1.45;
    }
    .sidebar-logo {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        color: #ffffff !important;
        border-radius: 10px;
        padding: 16px 14px;
        margin-bottom: 14px;
        box-shadow: 0 10px 22px rgba(30, 58, 138, 0.22);
    }
    .sidebar-logo-title {
        color: #ffffff !important;
        font-size: 21px;
        font-weight: 800;
        letter-spacing: .02em;
        margin-bottom: 4px;
    }
    .sidebar-logo-subtitle {
        color: #dbeafe !important;
        font-size: 12px;
        line-height: 1.35;
    }
    @media (max-width: 900px) {
        .visual-grid {
            grid-template-columns: 1fr;
        }
    }

    .metric-card {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 16px 16px 14px;
        min-height: 112px;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
    }
    .metric-label {
        color: var(--muted);
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: .06em;
        margin-bottom: 8px;
    }
    .metric-value {
        color: var(--brand-dark);
        font-size: 27px;
        font-weight: 760;
        line-height: 1.05;
    }
    .metric-note {
        color: var(--muted);
        font-size: 12px;
        margin-top: 8px;
    }
    .panel {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 14px 16px;
        margin: 8px 0 14px;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
        color: var(--ink) !important;
        font-size: 15px;
        line-height: 1.55;
    }
    .panel strong {
        color: var(--brand-dark) !important;
        font-weight: 760;
    }
    .panel br {
        display: block;
        margin-bottom: 4px;
        content: "";
    }
    .risk-high {
        border-left: 5px solid var(--danger);
        background: #fff7f7;
        color: #7f1d1d !important;
    }
    .risk-medium {
        border-left: 5px solid var(--accent);
        background: #fffbeb;
        color: #78350f !important;
    }
    .risk-low {
        border-left: 5px solid var(--brand);
        background: #eff6ff;
        color: #1e3a8a !important;
    }
    div[data-testid="stMetric"] {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 14px 16px;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
        color: var(--ink);
    }
    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
        color: var(--muted) !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--brand-dark) !important;
    }
    div[data-testid="stTabs"] button p {
        color: #111827;
        font-weight: 650;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] p {
        color: var(--brand-dark);
    }
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stCaptionContainer"],
    .stCaptionContainer {
        color: var(--muted) !important;
    }
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] h4 {
        color: var(--ink) !important;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 8px;
        overflow: hidden;
    }
    .light-table-wrap {
        width: 100%;
        overflow: auto;
        border: 1px solid #d8dee8;
        border-radius: 8px;
        background: #ffffff;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
        margin: 8px 0 16px;
    }
    table.light-data-table {
        width: 100%;
        border-collapse: collapse;
        background: #ffffff !important;
        color: #111827 !important;
        font-size: 14px;
    }
    table.light-data-table thead tr {
        background: #eaf1fb !important;
    }
    table.light-data-table th {
        background: #eaf1fb !important;
        color: #1e3a8a !important;
        font-weight: 750;
        text-align: left;
        padding: 11px 12px;
        border-bottom: 1px solid #cbd5e1;
        white-space: nowrap;
    }
    table.light-data-table td {
        background: #ffffff !important;
        color: #111827 !important;
        padding: 10px 12px;
        border-bottom: 1px solid #e5e7eb;
        white-space: nowrap;
    }
    table.light-data-table tbody tr:nth-child(even) td {
        background: #f8fafc !important;
    }
    table.light-data-table tbody tr:hover td {
        background: #eef4ff !important;
    }
    div.stDownloadButton > button {
        background: #1e3a8a !important;
        color: #ffffff !important;
        border: 1px solid #1e3a8a !important;
        border-radius: 8px !important;
        padding: 0.55rem 0.9rem;
        font-weight: 650;
        box-shadow: 0 8px 18px rgba(30, 58, 138, 0.22);
    }
    div.stDownloadButton > button p,
    div.stDownloadButton > button span {
        color: #ffffff !important;
        font-weight: 650 !important;
    }
    div.stDownloadButton > button:hover {
        background: #2563eb !important;
        border-color: #2563eb !important;
        color: #ffffff !important;
        box-shadow: 0 10px 22px rgba(37, 99, 235, 0.25);
    }
    div.stDownloadButton > button:hover p,
    div.stDownloadButton > button:hover span {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data() -> pd.DataFrame:
    data_path = Path(__file__).with_name("final_cleaned_skycity_data.csv")
    if not data_path.exists():
        data_path = Path("final_cleaned_skycity_data.csv")
    df = pd.read_csv(data_path)
    numeric_cols = [
        "MonthlyOrders",
        "TotalRevenue",
        "TotalNetProfit",
        "AOV",
        "AggregatorDependence",
        "InStoreReliance",
        *ORDER_COLS,
        *SHARE_COLS,
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def fmt_pct(value: float) -> str:
    if pd.isna(value):
        return "0.0%"
    return f"{value * 100:,.1f}%"


def fmt_num(value: float) -> str:
    return f"{value:,.0f}"


def fmt_money(value: float) -> str:
    return f"${value:,.0f}"


def selected_channel_names(channel_view: str) -> list[str]:
    if channel_view == "In-Store":
        return ["In-Store"]
    if channel_view == "Delivery":
        return ["Uber Eats", "DoorDash", "Self Delivery"]
    return list(CHANNELS.keys())


def build_channel_summary(data: pd.DataFrame, channel_names: list[str]) -> pd.DataFrame:
    rows = []
    total_orders = data["MonthlyOrders"].sum()
    for channel in channel_names:
        meta = CHANNELS[channel]
        orders = data[meta["orders"]].sum()
        revenue = data[meta["revenue"]].sum()
        profit = data[meta["profit"]].sum()
        rows.append(
            {
                "Channel": channel,
                "Channel Type": meta["type"],
                "Orders": orders,
                "Revenue": revenue,
                "Net Profit": profit,
                "Order Share": orders / total_orders if total_orders else 0,
                "Profit per Order": profit / orders if orders else 0,
            }
        )
    return pd.DataFrame(rows).sort_values("Orders", ascending=False)


def channel_long(data: pd.DataFrame, group_cols: list[str], channel_names: list[str]) -> pd.DataFrame:
    pieces = []
    for channel in channel_names:
        meta = CHANNELS[channel]
        grouped = data.groupby(group_cols, dropna=False)[meta["orders"]].sum().reset_index()
        grouped = grouped.rename(columns={meta["orders"]: "Orders"})
        grouped["Channel"] = channel
        pieces.append(grouped)
    long_df = pd.concat(pieces, ignore_index=True)
    totals = long_df.groupby(group_cols, dropna=False)["Orders"].transform("sum")
    long_df["Share"] = np.where(totals > 0, long_df["Orders"] / totals, 0)
    return long_df


def add_risk_columns(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data["MaxChannelShare"] = data[SHARE_COLS].max(axis=1)
    data["DominantChannel"] = data[SHARE_COLS].idxmax(axis=1).map(
        {
            "Final_InStoreShare": "In-Store",
            "Final_UE_share": "Uber Eats",
            "Final_DD_share": "DoorDash",
            "Final_SD_share": "Self Delivery",
        }
    )
    data["SingleAggregatorReliance"] = data[["Final_UE_share", "Final_DD_share"]].max(axis=1)
    data["SingleAggregatorRisk"] = data["SingleAggregatorReliance"] >= 0.70
    data["ChannelDiversificationScore"] = 1 - data["MaxChannelShare"]
    data["BalancedProfile"] = data["MaxChannelShare"] <= 0.45
    return data


def validate_data(data: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    checked = data.copy()
    checked["ChannelOrderTotal"] = checked[ORDER_COLS].sum(axis=1)
    checked["OrderCountGap"] = checked["MonthlyOrders"] - checked["ChannelOrderTotal"]
    checked["ShareTotal"] = checked[SHARE_COLS].sum(axis=1)
    checked["ShareGap"] = checked["ShareTotal"] - 1

    q1 = checked["MonthlyOrders"].quantile(0.25)
    q3 = checked["MonthlyOrders"].quantile(0.75)
    iqr = q3 - q1
    upper = q3 + (1.5 * iqr)
    lower = max(0, q1 - (1.5 * iqr))
    checked["OrderOutlier"] = (checked["MonthlyOrders"] < lower) | (checked["MonthlyOrders"] > upper)

    summary = {
        "order_mismatches": int((checked["OrderCountGap"].abs() > 1).sum()),
        "share_mismatches": int((checked["ShareGap"].abs() > 0.01).sum()),
        "outliers": int(checked["OrderOutlier"].sum()),
    }
    return checked, summary


df = add_risk_columns(load_data())


subregion_options = sorted(df["Subregion"].dropna().unique())
cuisine_options = sorted(df["CuisineType"].dropna().unique())
segment_options = sorted(df["Segment"].dropna().unique())

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-title">SkyCity Analytics</div>
        <div class="sidebar-logo-subtitle">Restaurant channel performance and delivery-risk dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    st.title("Dashboard Controls")
    appearance_mode = st.radio(
        "Appearance",
        ["Professional Light", "Executive Dark"],
        index=0,
        key="appearance_mode",
    )
    st.caption("Leave a filter blank to include all values. This keeps the sidebar clean and responsive on Streamlit Cloud.")

    subregions = st.multiselect(
        "Subregion",
        subregion_options,
        default=[],
        placeholder="All subregions included",
        help="Leave blank to include all subregions.",
    )
    cuisines = st.multiselect(
        "Cuisine",
        cuisine_options,
        default=[],
        placeholder="All cuisines included",
        help="Leave blank to include all cuisine types.",
    )
    segments = st.multiselect(
        "Restaurant segment",
        segment_options,
        default=[],
        placeholder="All segments included",
        help="Leave blank to include all restaurant segments.",
    )
    channel_view = st.radio(
        "Channel view",
        ["All Channels", "In-Store", "Delivery"],
        index=0,
    )
    risk_threshold = st.slider(
        "Single aggregator risk threshold",
        min_value=0.50,
        max_value=0.90,
        value=0.70,
        step=0.05,
        format="%.2f",
    )

    st.markdown("---")
    st.caption(
        f"Active view: "
        f"{len(subregions) if subregions else len(subregion_options)} subregions, "
        f"{len(cuisines) if cuisines else len(cuisine_options)} cuisines, "
        f"{len(segments) if segments else len(segment_options)} segments."
    )


if appearance_mode == "Executive Dark":
    st.markdown(
        """
        <style>
        .stApp {
            background: #0b1120 !important;
            color: #e5e7eb !important;
        }
        section[data-testid="stSidebar"] {
            background: #111827 !important;
            border-right: 1px solid #334155 !important;
        }
        section[data-testid="stSidebar"] * {
            color: #e5e7eb !important;
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #bfdbfe !important;
        }
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stCaptionContainer {
            color: #cbd5e1 !important;
        }
        section[data-testid="stSidebar"] div[data-baseweb="select"],
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
        section[data-testid="stSidebar"] [data-baseweb="select"] div {
            background-color: #1f2937 !important;
            border-color: #475569 !important;
        }
        .stMultiSelect [data-baseweb="tag"],
        section[data-testid="stSidebar"] div[data-baseweb="tag"] {
            background-color: #1d4ed8 !important;
            border-color: #3b82f6 !important;
        }
        .stMultiSelect [data-baseweb="tag"] span,
        section[data-testid="stSidebar"] div[data-baseweb="tag"] span {
            color: #ffffff !important;
        }
        .stMultiSelect [data-baseweb="tag"] svg,
        section[data-testid="stSidebar"] div[data-baseweb="tag"] svg {
            fill: #ffffff !important;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            background: #1f2937 !important;
            border-color: #475569 !important;
            color: #e5e7eb !important;
        }
        .hero {
            background: linear-gradient(135deg, #111827 0%, #172554 55%, #0f172a 100%) !important;
            border-color: #334155 !important;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28) !important;
        }
        .hero h1 {
            color: #f8fafc !important;
        }
        .hero p {
            color: #cbd5e1 !important;
        }
        .metric-card,
        div[data-testid="stMetric"],
        .panel {
            background: #111827 !important;
            border-color: #334155 !important;
            color: #e5e7eb !important;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.22) !important;
        }
        .metric-label,
        .metric-note,
        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] [data-testid="stMetricLabel"],
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stCaptionContainer"],
        .stCaptionContainer {
            color: #cbd5e1 !important;
        }
        .metric-value,
        div[data-testid="stMetric"] [data-testid="stMetricValue"],
        .panel strong,
        div[data-testid="stMarkdownContainer"] h1,
        div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stMarkdownContainer"] h3,
        div[data-testid="stMarkdownContainer"] h4 {
            color: #bfdbfe !important;
        }
        div[data-testid="stTabs"] button p {
            color: #cbd5e1 !important;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] p {
            color: #bfdbfe !important;
        }
        .risk-low {
            background: #10233f !important;
            color: #dbeafe !important;
            border-left-color: #60a5fa !important;
        }
        .risk-medium {
            background: #2d2211 !important;
            color: #fde68a !important;
            border-left-color: #f59e0b !important;
        }
        .risk-high {
            background: #2a1113 !important;
            color: #fecaca !important;
            border-left-color: #ef4444 !important;
        }

        .visual-card {
            background: #111827 !important;
            border-color: #334155 !important;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.22) !important;
        }
        .visual-card-title {
            color: #bfdbfe !important;
        }
        .visual-card-text {
            color: #cbd5e1 !important;
        }
        .sidebar-logo {
            background: linear-gradient(135deg, #172554 0%, #1d4ed8 100%) !important;
        }

        .light-table-wrap {
            background: #111827 !important;
            border-color: #334155 !important;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.22) !important;
        }
        table.light-data-table {
            background: #111827 !important;
            color: #e5e7eb !important;
        }
        table.light-data-table thead tr,
        table.light-data-table th {
            background: #1e3a8a !important;
            color: #ffffff !important;
            border-bottom-color: #334155 !important;
        }
        table.light-data-table td {
            background: #111827 !important;
            color: #e5e7eb !important;
            border-bottom-color: #334155 !important;
        }
        table.light-data-table tbody tr:nth-child(even) td {
            background: #172033 !important;
        }
        table.light-data-table tbody tr:hover td {
            background: #1e293b !important;
        }
        div.stDownloadButton > button {
            background: #3b82f6 !important;
            border-color: #3b82f6 !important;
            color: #ffffff !important;
        }
        div.stDownloadButton > button:hover {
            background: #2563eb !important;
            border-color: #2563eb !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


selected_subregions = subregions if subregions else subregion_options
selected_cuisines = cuisines if cuisines else cuisine_options
selected_segments = segments if segments else segment_options

filtered_df = df[
    df["Subregion"].isin(selected_subregions)
    & df["CuisineType"].isin(selected_cuisines)
    & df["Segment"].isin(selected_segments)
].copy()

if filtered_df.empty:
    st.warning("No restaurants match the selected filters.")
    st.stop()

filtered_df["SingleAggregatorRisk"] = filtered_df["SingleAggregatorReliance"] >= risk_threshold
active_channels = selected_channel_names(channel_view)
channel_summary = build_channel_summary(filtered_df, active_channels)
validated_df, validation_summary = validate_data(filtered_df)

total_orders = filtered_df["MonthlyOrders"].sum()
delivery_orders = filtered_df["TotalDeliveryOrders"].sum()
aggregator_orders = filtered_df["AggregatorOrders"].sum()
in_store_orders = filtered_df["InStoreOrders"].sum()
total_profit = filtered_df["TotalNetProfit"].sum()
total_revenue = filtered_df["TotalRevenue"].sum()
avg_aggregator_dependence = aggregator_orders / total_orders if total_orders else 0
in_store_reliance = in_store_orders / total_orders if total_orders else 0
delivery_share = delivery_orders / total_orders if total_orders else 0
diversification_score = filtered_df["ChannelDiversificationScore"].mean()
single_agg_risk_count = int(filtered_df["SingleAggregatorRisk"].sum())
balanced_count = int(filtered_df["BalancedProfile"].sum())
dominant_channel = channel_summary.iloc[0]["Channel"] if not channel_summary.empty else "N/A"


st.markdown(
    """
    <div class="hero">
        <h1>SkyCity Auckland Channel Performance Dashboard</h1>
        <p>
            Executive view of order-channel mix, geographic behavior, cuisine and segment patterns,
            dependency risk, and validation checks for performance-based reporting.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="visual-grid">
        <div class="visual-card">
            <img src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=900&q=80" alt="Restaurant interior">
            <div class="visual-card-body">
                <div class="visual-card-title">Restaurant Channel View</div>
                <div class="visual-card-text">Compare in-store ordering strength with delivery-platform performance across Auckland restaurants.</div>
            </div>
        </div>
        <div class="visual-card">
            <img src="https://images.unsplash.com/photo-1526367790999-0150786686a2?auto=format&fit=crop&w=900&q=80" alt="Food delivery package">
            <div class="visual-card-body">
                <div class="visual-card-title">Delivery Platform Insights</div>
                <div class="visual-card-text">Track Uber Eats, DoorDash, and self-delivery contribution to orders, revenue, and risk.</div>
            </div>
        </div>
        <div class="visual-card">
            <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=80" alt="Analytics dashboard">
            <div class="visual-card-body">
                <div class="visual-card-title">Executive Analytics</div>
                <div class="visual-card-text">Use KPI cards, heatmaps, validation checks, and recommendations for internship presentation.</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Channel Order Share</div>
            <div class="metric-value">{fmt_pct(channel_summary.iloc[0]["Order Share"])}</div>
            <div class="metric-note">Dominant channel: {dominant_channel}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Aggregator Dependence</div>
            <div class="metric-value">{fmt_pct(avg_aggregator_dependence)}</div>
            <div class="metric-note">Uber Eats + DoorDash order share</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with k3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">In-Store Reliance Ratio</div>
            <div class="metric-value">{fmt_pct(in_store_reliance)}</div>
            <div class="metric-note">Walk-in ordering strength</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with k4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Diversification Score</div>
            <div class="metric-value">{fmt_pct(diversification_score)}</div>
            <div class="metric-note">Higher means less channel concentration</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with k5:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total Net Profit</div>
            <div class="metric-value">{fmt_money(total_profit)}</div>
            <div class="metric-note">{fmt_num(total_orders)} orders, {fmt_pct(delivery_share)} delivery</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


tabs = st.tabs(
    [
        "Channel Mix",
        "Subregion Heatmaps",
        "Cuisine & Segment",
        "Dependency Risk",
        "Validation",
        "Recommendations",
    ]
)


with tabs[0]:
    st.subheader("Channel Mix Overview")
    left, right = st.columns([1.25, 1])

    with left:
        fig = px.bar(
            channel_summary,
            x="Channel",
            y="Orders",
            color="Channel Type",
            text=channel_summary["Orders"].map(lambda v: f"{v:,.0f}"),
            title="Orders by Channel",
            color_discrete_map={"In-Store": "#2563eb", "Delivery": "#64748b"},
        )
        fig.update_layout(yaxis_title="Orders", xaxis_title="", showlegend=True)
        show_chart(fig)

    with right:
        fig = px.pie(
            channel_summary,
            names="Channel",
            values="Orders",
            hole=0.52,
            title="Channel Market Share",
            color_discrete_map=CHANNEL_COLORS,
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        show_chart(fig)

    c1, c2 = st.columns(2)
    with c1:
        ranked = channel_summary.copy()
        ranked["Market Share"] = ranked["Order Share"].map(fmt_pct)
        ranked["Profit per Order"] = ranked["Profit per Order"].map(lambda v: f"${v:,.2f}")
        show_table(
            ranked[["Channel", "Channel Type", "Orders", "Market Share", "Revenue", "Net Profit", "Profit per Order"]],
        )
    with c2:
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=avg_aggregator_dependence * 100,
            title={"text": "Aggregator Dependence Index"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563eb"},
                "steps": [
                    {"range": [0, 50], "color": "#eff6ff"},
                    {"range": [50, 70], "color": "#fef3c7"},
                    {"range": [70, 100], "color": "#fee2e2"},
                ],
                "threshold": {"line": {"color": "#b42318", "width": 4}, "value": risk_threshold * 100},
            },
        ))
        fig.update_layout(height=330, margin=dict(l=20, r=20, t=50, b=20))
        show_chart(fig)


with tabs[1]:
    st.subheader("Subregion-Wise Channel Heatmaps")
    subregion_long = channel_long(filtered_df, ["Subregion"], active_channels)

    heat_orders = subregion_long.pivot(index="Subregion", columns="Channel", values="Orders").fillna(0)
    fig = px.imshow(
        heat_orders,
        text_auto=".0f",
        aspect="auto",
        color_continuous_scale="Blues",
        title="Order Volume Heatmap by Subregion and Channel",
    )
    fig.update_layout(xaxis_title="Channel", yaxis_title="Subregion")
    show_chart(fig)

    heat_share = subregion_long.pivot(index="Subregion", columns="Channel", values="Share").fillna(0)
    fig = px.imshow(
        heat_share,
        text_auto=".1%",
        aspect="auto",
        color_continuous_scale="Cividis",
        title="Channel Share Heatmap by Subregion",
    )
    fig.update_layout(xaxis_title="Channel", yaxis_title="Subregion")
    show_chart(fig)

    dominance = subregion_long.loc[subregion_long.groupby("Subregion")["Orders"].idxmax()].copy()
    dominance["Share"] = dominance["Share"].map(fmt_pct)
    show_table(
        dominance.rename(columns={"Channel": "Dominant Channel", "Share": "Dominance Share"})[
            ["Subregion", "Dominant Channel", "Orders", "Dominance Share"]
        ],
    )


with tabs[2]:
    st.subheader("Cuisine vs Channel Distribution")
    cuisine_long = channel_long(filtered_df, ["CuisineType"], active_channels)
    segment_long = channel_long(filtered_df, ["Segment"], active_channels)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(
            cuisine_long,
            x="CuisineType",
            y="Share",
            color="Channel",
            title="Cuisine Channel Mix",
            barmode="stack",
            color_discrete_map=CHANNEL_COLORS,
        )
        fig.update_layout(yaxis_tickformat=".0%", xaxis_title="", yaxis_title="Order Share")
        show_chart(fig)

    with c2:
        fig = px.bar(
            segment_long,
            x="Segment",
            y="Share",
            color="Channel",
            title="Segment Channel Mix",
            barmode="stack",
            color_discrete_map=CHANNEL_COLORS,
        )
        fig.update_layout(yaxis_tickformat=".0%", xaxis_title="", yaxis_title="Order Share")
        show_chart(fig)

    aggregator_by_cuisine = (
        filtered_df.groupby("CuisineType", dropna=False)
        .agg(
            Orders=("MonthlyOrders", "sum"),
            AggregatorOrders=("AggregatorOrders", "sum"),
            AvgDependence=("AggregatorDependence", "mean"),
            NetProfit=("TotalNetProfit", "sum"),
        )
        .reset_index()
    )
    aggregator_by_cuisine["Aggregator Share"] = np.where(
        aggregator_by_cuisine["Orders"] > 0,
        aggregator_by_cuisine["AggregatorOrders"] / aggregator_by_cuisine["Orders"],
        0,
    )
    aggregator_by_cuisine = aggregator_by_cuisine.sort_values("Aggregator Share", ascending=False)

    fig = px.bar(
        aggregator_by_cuisine,
        x="CuisineType",
        y="Aggregator Share",
        color="NetProfit",
        title="Aggregator-Heavy Cuisine Categories",
        text=aggregator_by_cuisine["Aggregator Share"].map(fmt_pct),
        color_continuous_scale="Blues",
    )
    fig.update_layout(yaxis_tickformat=".0%", xaxis_title="", yaxis_title="Aggregator Order Share")
    show_chart(fig)


with tabs[3]:
    st.subheader("Dependency Risk Indicator Panels")

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Single Aggregator Risk", single_agg_risk_count, f">= {fmt_pct(risk_threshold)} on Uber Eats or DoorDash")
    r2.metric("Balanced Profiles", balanced_count, "Max channel share <= 45%")
    r3.metric("High-Risk Category", int((filtered_df["AggregatorRiskCategory"] == "High Risk").sum()))
    r4.metric("Median Diversification", fmt_pct(filtered_df["ChannelDiversificationScore"].median()))

    risk_class = "risk-low"
    risk_title = "Low portfolio concentration"
    if avg_aggregator_dependence >= risk_threshold:
        risk_class = "risk-high"
        risk_title = "High aggregator concentration"
    elif avg_aggregator_dependence >= 0.50:
        risk_class = "risk-medium"
        risk_title = "Moderate aggregator concentration"

    st.markdown(
        f"""
        <div class="panel {risk_class}">
            <strong>{risk_title}</strong><br>
            Current aggregator dependence is {fmt_pct(avg_aggregator_dependence)}.
            Diversification benchmark: keep any one aggregator below {fmt_pct(risk_threshold)}
            and keep the strongest single channel below 45% where operationally possible.
        </div>
        """,
        unsafe_allow_html=True,
    )

    risk_table = filtered_df[
        [
            "RestaurantName",
            "Subregion",
            "CuisineType",
            "Segment",
            "DominantChannel",
            "SingleAggregatorReliance",
            "AggregatorDependence",
            "ChannelDiversificationScore",
            "AggregatorRiskCategory",
            "TotalNetProfit",
        ]
    ].sort_values(["SingleAggregatorReliance", "AggregatorDependence"], ascending=False)

    display_risk = risk_table.head(20).copy()
    for col in ["SingleAggregatorReliance", "AggregatorDependence", "ChannelDiversificationScore"]:
        display_risk[col] = display_risk[col].map(fmt_pct)
    display_risk["TotalNetProfit"] = display_risk["TotalNetProfit"].map(fmt_money)
    show_table(display_risk, height=460)

    fig = px.scatter(
        filtered_df,
        x="AggregatorDependence",
        y="ChannelDiversificationScore",
        size="MonthlyOrders",
        color="AggregatorRiskCategory",
        hover_data=["RestaurantName", "Subregion", "CuisineType", "Segment", "DominantChannel"],
        title="Risk Map: Aggregator Dependence vs Diversification",
        color_discrete_map=RISK_COLORS,
    )
    fig.add_vline(x=risk_threshold, line_dash="dash", line_color="#b42318")
    fig.update_layout(xaxis_tickformat=".0%", yaxis_tickformat=".0%")
    show_chart(fig)


with tabs[4]:
    st.subheader("Data Validation & Consistency Checks")
    v1, v2, v3 = st.columns(3)
    v1.metric("Order Count Mismatches", validation_summary["order_mismatches"])
    v2.metric("Share Total Mismatches", validation_summary["share_mismatches"])
    v3.metric("Monthly Order Outliers", validation_summary["outliers"])

    st.markdown(
        f"""
        <div class="panel risk-low">
            <strong>Validation status</strong><br>
            Channel order totals are compared with MonthlyOrders, final channel shares are checked against
            100%, and unusual monthly order volumes are flagged with an IQR outlier rule.
            Current filtered view has {validation_summary["order_mismatches"]} order mismatches and
            {validation_summary["share_mismatches"]} share mismatches.
        </div>
        """,
        unsafe_allow_html=True,
    )

    validation_view = validated_df[
        [
            "RestaurantName",
            "Subregion",
            "CuisineType",
            "Segment",
            "MonthlyOrders",
            "ChannelOrderTotal",
            "OrderCountGap",
            "ShareTotal",
            "ShareGap",
            "OrderOutlier",
        ]
    ].copy()
    validation_view["ShareTotal"] = validation_view["ShareTotal"].map(fmt_pct)
    validation_view["ShareGap"] = validation_view["ShareGap"].map(lambda v: f"{v:+.2%}")
    show_table(validation_view, height=460)


with tabs[5]:
    st.subheader("Performance Recommendations")
    rec_left, rec_right = st.columns(2)

    with rec_left:
        st.markdown(
            """
            <div class="panel risk-low">
                <strong>What is already strong</strong><br>
                The project already covers channel aggregation, market share ranking, subregion comparison,
                cuisine and segment behavior, and profitability. These match the core analytical direction.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="panel risk-medium">
                <strong>What this version improves</strong><br>
                It adds validation checks, explicit KPI definitions, a required in-store vs delivery toggle,
                single-aggregator 70% risk detection, and clearer executive panels.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with rec_right:
        st.markdown(
            """
            <div class="panel risk-high">
                <strong>Business action</strong><br>
                Restaurants above the single-aggregator threshold should receive direct-ordering, loyalty,
                and self-delivery recommendations before commission exposure weakens margins.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="panel">
                <strong>Portfolio snapshot</strong><br>
                Current filtered view has {single_agg_risk_count} single-aggregator risk restaurants,
                {balanced_count} balanced profiles, and {fmt_pct(avg_aggregator_dependence)}
                overall aggregator dependence.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### Methodology Covered")
    methodology = pd.DataFrame(
        [
            ["Validation", "Order totals, share totals, and outlier transparency"],
            ["Volume Aggregation", "Orders by channel, subregion, cuisine, and segment"],
            ["Market Share", "Overall channel contribution and delivery vs in-store dominance"],
            ["Geography", "Subregion channel heatmaps and dominance table"],
            ["Cuisine & Segment", "Cuisine mix, segment mix, and aggregator-heavy categories"],
            ["Risk", "70% single aggregator reliance, balanced profiles, and diversification score"],
        ],
        columns=["Requirement", "Dashboard Coverage"],
    )
    show_table(methodology)


st.markdown("---")
download_df = filtered_df.copy()
download_df["SelectedChannelView"] = channel_view
st.download_button(
    "Download filtered data",
    data=download_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_skycity_channel_performance.csv",
    mime="text/csv",
)
st.caption("Prepared for SkyCity Auckland restaurant channel performance analysis.")
