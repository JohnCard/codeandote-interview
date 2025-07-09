from openpyxl.styles import Alignment, Font, PatternFill, Border, Side

# Predifined border generic style
DEFAULT_BORDER = Side(style='medium', color='000000')
BORDER = Border(left=DEFAULT_BORDER, right=DEFAULT_BORDER,
                top=DEFAULT_BORDER, bottom=DEFAULT_BORDER)

# Default style settings
DEFAULT_STYLES = {
        'alignment': Alignment(horizontal="center", vertical="center"),
        'font': Font(name="Calibri", size=12, bold=False, italic=False, color="000000"),
        'fill': PatternFill(start_color='17a19f', end_color='17a19f', fill_type='solid'),
        'border': BORDER
    }

DEFAULT_STYLE_DIC = {
    'headers': DEFAULT_STYLES,
    'data': DEFAULT_STYLES
}