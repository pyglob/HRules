# color_utils.py
from typing import Optional, Dict
from docx.enum.dml import MSO_THEME_COLOR

CONTRAST_THRESHOLD = 4.5

THEME_MAP = {
    MSO_THEME_COLOR.BACKGROUND_1: "#ffffff",
    MSO_THEME_COLOR.TEXT_1: "#000000",
    MSO_THEME_COLOR.BACKGROUND_2: "#e7e6e6",
    MSO_THEME_COLOR.TEXT_2: "#44546a",
    MSO_THEME_COLOR.ACCENT_1: "#5b9bd5",
    MSO_THEME_COLOR.ACCENT_2: "#ed7d31",
    MSO_THEME_COLOR.ACCENT_3: "#a5a5a5",
    MSO_THEME_COLOR.ACCENT_4: "#ffc000",
    MSO_THEME_COLOR.ACCENT_5: "#4472c4",
    MSO_THEME_COLOR.ACCENT_6: "#70ad47",
    MSO_THEME_COLOR.HYPERLINK: "#0563c1",
    MSO_THEME_COLOR.FOLLOWED_HYPERLINK: "#954f72",
}


def contrast_ratio(fg_hex, bg_hex):
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

    def rel_luminance(rgb):
        def channel(c):
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        r, g, b = rgb
        return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

    fg_rgb = hex_to_rgb(fg_hex)
    bg_rgb = hex_to_rgb(bg_hex)
    L1 = rel_luminance(fg_rgb)
    L2 = rel_luminance(bg_rgb)
    return round((max(L1, L2) + 0.05) / (min(L1, L2) + 0.05), 2)


def resolve_docx_color(font_color):
    """Return #rrggbb for a python-docx font color, or None."""
    if not font_color:
        return None
    if font_color.rgb:
        return f"#{str(font_color.rgb).lower()}"
    if font_color.theme_color in THEME_MAP:
        return THEME_MAP[font_color.theme_color]
    if isinstance(font_color, int):
        r = (font_color >> 16) & 255
        g = (font_color >> 8) & 255
        b = font_color & 255
        return f"#{r:02x}{g:02x}{b:02x}"
    return None


def theme_hex(theme_map: Dict, theme_color: Optional[MSO_THEME_COLOR]) -> Optional[str]:
    """Look up a theme colour in THEME_MAP whether keyed by enum or string."""
    if not theme_color:
        return None
    if theme_color in theme_map:
        return theme_map[theme_color]
    name = getattr(theme_color, "name", None)
    if not name:
        return None
    candidates = [
        name,
        name.lower(),
        name.replace("_", "").lower(),
    ]
    for c in candidates:
        if c in theme_map:
            return theme_map[c]
    return None


def hex_from_rgbcolor(rgb_obj) -> Optional[str]:
    """python-docx RGBColor -> '#rrggbb' or None."""
    if not rgb_obj:
        return None
    try:
        return f"#{str(rgb_obj).lower()}"
    except (AttributeError, TypeError, ValueError):
        return None


def hex_from_int(int_color: int) -> str:
    r = (int_color >> 16) & 255
    g = (int_color >> 8) & 255
    b = int_color & 255
    return f"#{r:02x}{g:02x}{b:02x}"


def resolve_font_color_hex(color_obj, theme_map: Dict) -> Optional[str]:
    """
    Resolve a docx font colour object to '#rrggbb'
    """
    if not color_obj:
        return None

    rgb_val = getattr(color_obj, "rgb", None)
    # rgb_val is an RGBColor or None
    if rgb_val:
        # python-docx RGBColor prints as 'FFFFFF'
        rgb_str = str(rgb_val).strip().lower()
        if not rgb_str.startswith("#"):
            rgb_str = "#" + rgb_str
        return rgb_str

    theme_color = getattr(color_obj, "theme_color", None)
    if theme_color is not None:
        hex_theme = theme_hex(theme_map, theme_color)
        if hex_theme:
            return hex_theme

    if isinstance(color_obj, int):
        return hex_from_int(color_obj)
    return None


def resolve_run_fg_hex(run, theme_map: Dict) -> Optional[str]:
    # Direct on run
    fg = resolve_font_color_hex(getattr(run.font, "color", None), theme_map)
    if fg:
        return fg
    # From character style
    try:
        if run.style and run.style.font:
            fg = resolve_font_color_hex(run.style.font.color, theme_map)
            if fg:
                return fg
    except (AttributeError, TypeError):
        pass
    # From paragraph style
    try:
        pstyle = getattr(run.paragraph, "style", None)
        if pstyle and pstyle.font:
            fg = resolve_font_color_hex(pstyle.font.color, theme_map)
            if fg:
                return fg
    except (AttributeError, TypeError):
        pass

    return None
