from random import random


def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


BLACK = hex_to_rgb("#000000")
WHITE = hex_to_rgb("#FFFFFF")

SLATE = {
    "50": hex_to_rgb("#f8fafc"),
    "100": hex_to_rgb("#f1f5f9"),
    "200": hex_to_rgb("#e2e8f0"),
    "300": hex_to_rgb("#cbd5e1"),
    "400": hex_to_rgb("#94a3b8"),
    "500": hex_to_rgb("#64748b"),
    "600": hex_to_rgb("#475569"),
    "700": hex_to_rgb("#334155"),
    "800": hex_to_rgb("#1e293b"),
    "900": hex_to_rgb("#0f172a"),
    "950": hex_to_rgb("#020617"),
}

GRAY = {
    "50": hex_to_rgb("#f9fafb"),
    "100": hex_to_rgb("#f3f4f6"),
    "200": hex_to_rgb("#e5e7eb"),
    "300": hex_to_rgb("#d1d5db"),
    "400": hex_to_rgb("#9ca3af"),
    "500": hex_to_rgb("#6b7280"),
    "600": hex_to_rgb("#4b5563"),
    "700": hex_to_rgb("#374151"),
    "800": hex_to_rgb("#1f2937"),
    "900": hex_to_rgb("#111827"),
    "950": hex_to_rgb("#030712"),
}

ZINC = {
    "50": hex_to_rgb("#fafafa"),
    "100": hex_to_rgb("#f4f4f5"),
    "200": hex_to_rgb("#e4e4e7"),
    "300": hex_to_rgb("#d4d4d8"),
    "400": hex_to_rgb("#a1a1aa"),
    "500": hex_to_rgb("#71717a"),
    "600": hex_to_rgb("#52525b"),
    "700": hex_to_rgb("#3f3f46"),
    "800": hex_to_rgb("#27272a"),
    "900": hex_to_rgb("#18181b"),
    "950": hex_to_rgb("#09090b"),
}

NEUTRAL = {
    "50": hex_to_rgb("#fafafa"),
    "100": hex_to_rgb("#f5f5f5"),
    "200": hex_to_rgb("#e5e5e5"),
    "300": hex_to_rgb("#d4d4d4"),
    "400": hex_to_rgb("#a3a3a3"),
    "500": hex_to_rgb("#737373"),
    "600": hex_to_rgb("#525252"),
    "700": hex_to_rgb("#404040"),
    "800": hex_to_rgb("#262626"),
    "900": hex_to_rgb("#171717"),
    "950": hex_to_rgb("#0a0a0a"),
}

STONE = {
    "50": hex_to_rgb("#fafaf9"),
    "100": hex_to_rgb("#f5f5f4"),
    "200": hex_to_rgb("#e7e5e4"),
    "300": hex_to_rgb("#d6d3d1"),
    "400": hex_to_rgb("#a8a29e"),
    "500": hex_to_rgb("#78716c"),
    "600": hex_to_rgb("#57534e"),
    "700": hex_to_rgb("#44403c"),
    "800": hex_to_rgb("#292524"),
    "900": hex_to_rgb("#1c1917"),
    "950": hex_to_rgb("#0c0a09"),
}

RED = {
    "50": hex_to_rgb("#fef2f2"),
    "100": hex_to_rgb("#fee2e2"),
    "200": hex_to_rgb("#fecaca"),
    "300": hex_to_rgb("#fca5a5"),
    "400": hex_to_rgb("#f87171"),
    "500": hex_to_rgb("#ef4444"),
    "600": hex_to_rgb("#dc2626"),
    "700": hex_to_rgb("#b91c1c"),
    "800": hex_to_rgb("#991b1b"),
    "900": hex_to_rgb("#7f1d1d"),
    "950": hex_to_rgb("#450a0a"),
}

ORANGE = {
    "50": hex_to_rgb("#fff7ed"),
    "100": hex_to_rgb("#ffedd5"),
    "200": hex_to_rgb("#fed7aa"),
    "300": hex_to_rgb("#fdba74"),
    "400": hex_to_rgb("#fb923c"),
    "500": hex_to_rgb("#f97316"),
    "600": hex_to_rgb("#ea580c"),
    "700": hex_to_rgb("#c2410c"),
    "800": hex_to_rgb("#9a3412"),
    "900": hex_to_rgb("#7c2d12"),
    "950": hex_to_rgb("#431407"),
}

AMBER = {
    "50": hex_to_rgb("#fffbeb"),
    "100": hex_to_rgb("#fef3c7"),
    "200": hex_to_rgb("#fde68a"),
    "300": hex_to_rgb("#fcd34d"),
    "400": hex_to_rgb("#fbbf24"),
    "500": hex_to_rgb("#f59e0b"),
    "600": hex_to_rgb("#d97706"),
    "700": hex_to_rgb("#b45309"),
    "800": hex_to_rgb("#92400e"),
    "900": hex_to_rgb("#78350f"),
    "950": hex_to_rgb("#451a03"),
}

YELLOW = {
    "50": hex_to_rgb("#fefce8"),
    "100": hex_to_rgb("#fef9c3"),
    "200": hex_to_rgb("#fef08a"),
    "300": hex_to_rgb("#fde047"),
    "400": hex_to_rgb("#facc15"),
    "500": hex_to_rgb("#eab308"),
    "600": hex_to_rgb("#ca8a04"),
    "700": hex_to_rgb("#a16207"),
    "800": hex_to_rgb("#854d0e"),
    "900": hex_to_rgb("#713f12"),
    "950": hex_to_rgb("#422006"),
}

LIME = {
    "50": hex_to_rgb("#f7fee7"),
    "100": hex_to_rgb("#ecfccb"),
    "200": hex_to_rgb("#d9f99d"),
    "300": hex_to_rgb("#bef264"),
    "400": hex_to_rgb("#a3e635"),
    "500": hex_to_rgb("#84cc16"),
    "600": hex_to_rgb("#65a30d"),
    "700": hex_to_rgb("#4d7c0f"),
    "800": hex_to_rgb("#3f6212"),
    "900": hex_to_rgb("#365314"),
    "950": hex_to_rgb("#1a2e05"),
}

GREEN = {
    "50": hex_to_rgb("#f0fdf4"),
    "100": hex_to_rgb("#dcfce7"),
    "200": hex_to_rgb("#bbf7d0"),
    "300": hex_to_rgb("#86efac"),
    "400": hex_to_rgb("#4ade80"),
    "500": hex_to_rgb("#22c55e"),
    "600": hex_to_rgb("#16a34a"),
    "700": hex_to_rgb("#15803d"),
    "800": hex_to_rgb("#166534"),
    "900": hex_to_rgb("#14532d"),
    "950": hex_to_rgb("#052e16"),
}

EMERALD = {
    "50": hex_to_rgb("#ecfdf5"),
    "100": hex_to_rgb("#d1fae5"),
    "200": hex_to_rgb("#a7f3d0"),
    "300": hex_to_rgb("#6ee7b7"),
    "400": hex_to_rgb("#34d399"),
    "500": hex_to_rgb("#10b981"),
    "600": hex_to_rgb("#059669"),
    "700": hex_to_rgb("#047857"),
    "800": hex_to_rgb("#065f46"),
    "900": hex_to_rgb("#064e3b"),
    "950": hex_to_rgb("#022c22"),
}

TEAL = {
    "50": hex_to_rgb("#f0fdfa"),
    "100": hex_to_rgb("#ccfbf1"),
    "200": hex_to_rgb("#99f6e4"),
    "300": hex_to_rgb("#5eead4"),
    "400": hex_to_rgb("#2dd4bf"),
    "500": hex_to_rgb("#14b8a6"),
    "600": hex_to_rgb("#0d9488"),
    "700": hex_to_rgb("#0f766e"),
    "800": hex_to_rgb("#115e59"),
    "900": hex_to_rgb("#134e4a"),
    "950": hex_to_rgb("#042f2e"),
}

CYAN = {
    "50": hex_to_rgb("#ecfeff"),
    "100": hex_to_rgb("#cffafe"),
    "200": hex_to_rgb("#a5f3fc"),
    "300": hex_to_rgb("#67e8f9"),
    "400": hex_to_rgb("#22d3ee"),
    "500": hex_to_rgb("#06b6d4"),
    "600": hex_to_rgb("#0891b2"),
    "700": hex_to_rgb("#0e7490"),
    "800": hex_to_rgb("#155e75"),
    "900": hex_to_rgb("#164e63"),
    "950": hex_to_rgb("#083344"),
}

SKY = {
    "50": hex_to_rgb("#f0f9ff"),
    "100": hex_to_rgb("#e0f2fe"),
    "200": hex_to_rgb("#bae6fd"),
    "300": hex_to_rgb("#7dd3fc"),
    "400": hex_to_rgb("#38bdf8"),
    "500": hex_to_rgb("#0ea5e9"),
    "600": hex_to_rgb("#0284c7"),
    "700": hex_to_rgb("#0369a1"),
    "800": hex_to_rgb("#075985"),
    "900": hex_to_rgb("#0c4a6e"),
    "950": hex_to_rgb("#083344"),
}

BLUE = {
    "50": hex_to_rgb("#eff6ff"),
    "100": hex_to_rgb("#dbeafe"),
    "200": hex_to_rgb("#bfdbfe"),
    "300": hex_to_rgb("#93c5fd"),
    "400": hex_to_rgb("#60a5fa"),
    "500": hex_to_rgb("#3b82f6"),
    "600": hex_to_rgb("#2563eb"),
    "700": hex_to_rgb("#1d4ed8"),
    "800": hex_to_rgb("#1e40af"),
    "900": hex_to_rgb("#1e3a8a"),
    "950": hex_to_rgb("#172554"),
}

INDIGO = {
    "50": hex_to_rgb("#eef2ff"),
    "100": hex_to_rgb("#e0e7ff"),
    "200": hex_to_rgb("#c7d2fe"),
    "300": hex_to_rgb("#a5b4fc"),
    "400": hex_to_rgb("#818cf8"),
    "500": hex_to_rgb("#6366f1"),
    "600": hex_to_rgb("#4f46e5"),
    "700": hex_to_rgb("#4338ca"),
    "800": hex_to_rgb("#3730a3"),
    "900": hex_to_rgb("#312e81"),
    "950": hex_to_rgb("#1e1b4b"),
}

VIOLET = {
    "50": hex_to_rgb("#f5f3ff"),
    "100": hex_to_rgb("#ede9fe"),
    "200": hex_to_rgb("#ddd6fe"),
    "300": hex_to_rgb("#c4b5fd"),
    "400": hex_to_rgb("#a78bfa"),
    "500": hex_to_rgb("#8b5cf6"),
    "600": hex_to_rgb("#7c3aed"),
    "700": hex_to_rgb("#6d28d9"),
    "800": hex_to_rgb("#5b21b6"),
    "900": hex_to_rgb("#4c1d95"),
    "950": hex_to_rgb("#2e1065"),
}

PURPLE = {
    "50": hex_to_rgb("#faf5ff"),
    "100": hex_to_rgb("#f3e8ff"),
    "200": hex_to_rgb("#e9d5ff"),
    "300": hex_to_rgb("#d8b4fe"),
    "400": hex_to_rgb("#c084fc"),
    "500": hex_to_rgb("#a855f7"),
    "600": hex_to_rgb("#9333ea"),
    "700": hex_to_rgb("#7e22ce"),
    "800": hex_to_rgb("#6b21a8"),
    "900": hex_to_rgb("#581c87"),
    "950": hex_to_rgb("#3b0764"),
}

FUCHSIA = {
    "50": hex_to_rgb("#fdf4ff"),
    "100": hex_to_rgb("#fae8ff"),
    "200": hex_to_rgb("#f5d0fe"),
    "300": hex_to_rgb("#f0abfc"),
    "400": hex_to_rgb("#e879f9"),
    "500": hex_to_rgb("#d946ef"),
    "600": hex_to_rgb("#c026d3"),
    "700": hex_to_rgb("#a21caf"),
    "800": hex_to_rgb("#86198f"),
    "900": hex_to_rgb("#701a75"),
    "950": hex_to_rgb("#4a044e"),
}

PINK = {
    "50": hex_to_rgb("#fdf2f8"),
    "100": hex_to_rgb("#fce7f3"),
    "200": hex_to_rgb("#fbcfe8"),
    "300": hex_to_rgb("#f9a8d4"),
    "400": hex_to_rgb("#f472b6"),
    "500": hex_to_rgb("#ec4899"),
    "600": hex_to_rgb("#db2777"),
    "700": hex_to_rgb("#be185d"),
    "800": hex_to_rgb("#9d174d"),
    "900": hex_to_rgb("#831843"),
    "950": hex_to_rgb("#500724"),
}

ROSE = {
    "50": hex_to_rgb("#fff1f2"),
    "100": hex_to_rgb("#ffe4e6"),
    "200": hex_to_rgb("#fecdd3"),
    "300": hex_to_rgb("#fda4af"),
    "400": hex_to_rgb("#fb7185"),
    "500": hex_to_rgb("#f43f5e"),
    "600": hex_to_rgb("#e11d48"),
    "700": hex_to_rgb("#be123c"),
    "800": hex_to_rgb("#9f1239"),
    "900": hex_to_rgb("#881337"),
    "950": hex_to_rgb("#4c0519"),
}


COLORS = {
    "black": BLACK,
    "white": WHITE,
    "slate": SLATE,
    "gray": GRAY,
    "zinc": ZINC,
    "neutral": NEUTRAL,
    "stone": STONE,
    "red": RED,
    "orange": ORANGE,
    "amber": AMBER,
    "yellow": YELLOW,
    "lime": LIME,
    "green": GREEN,
    "emerald": EMERALD,
    "teal": TEAL,
    "cyan": CYAN,
    "sky": SKY,
    "blue": BLUE,
    "indigo": INDIGO,
    "violet": VIOLET,
    "purple": PURPLE,
    "fuchsia": FUCHSIA,
    "pink": PINK,
    "rose": ROSE,
}


def get_color_names():
    """Retrieve a list of available color names."""
    return list(COLORS.keys())


def get_color_group(name):
    """Retrieve a color group by name."""
    return COLORS.get(name.lower())


def get_color(name: str, shade=500):
    """Retrieve a color by name and shade."""
    color_group = COLORS.get(name.lower())
    if isinstance(color_group, tuple):
        return color_group
    if color_group:
        return color_group[str(shade)]
    return BLACK


def get_color_hex(name: str, shade=500):
    """Retrieve a color in hex format by name and shade."""
    rgb = get_color(name, shade)
    return rgb_to_hex(rgb)


def lighten_color(rgb: tuple[int, int, int], factor: float):
    """Lighten a color by a given factor."""
    r, g, b = rgb
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return (r, g, b)


def darken_color(rgb: tuple[int, int, int], factor: float):
    """Darken a color by a given factor."""
    r, g, b = rgb
    r = int(r * (1 - factor))
    g = int(g * (1 - factor))
    b = int(b * (1 - factor))
    return (r, g, b)


def get_random_color():
    """Retrieve a random color from the COLORS dictionary."""
    color_name = random.choice(list(COLORS.keys()))
    color_group = COLORS[color_name]
    if isinstance(color_group, tuple):
        return color_group
    shade = random.choice(list(color_group.keys()))
    return color_group[shade]
