def get_print_styles() -> str:
    return """
    <style>
    @media print {
        .stSidebar, [data-testid="stSidebar"], .stDownloadButton, .stMultiSelect, .stDateInput, .stSelectbox, .stButton, .stTextInput, .stCheckbox, .stRadio, .stTabs, .stExpander, .stToolbar, .stDeployButton {
            display:none !important;
        }

        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }

        body {
            font-size: 11pt;
        }
    }
    </style>
    """
