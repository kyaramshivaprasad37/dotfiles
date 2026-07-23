c.window.transparent = True
# pylint: disable=C0111
c = c  # noqa: F821 pylint: disable=E0602,C0103
config = config  # noqa: F821 pylint: disable=E0602,C0103

import os
import subprocess

# --- GPU / SPEED FIX for older Intel graphics (added for your hardware) ---
c.qt.args = ['disable-gpu', 'disable-gpu-compositing', 'disable-software-rasterizer']

c.qt.force_software_rendering = 'chromium'
c.content.cache.size = 52428800         
c.content.autoplay = False
c.content.notifications.enabled = False

def read_xresources(prefix):
    props = {}
    x = subprocess.run(['xrdb', '-query'], capture_output=True, check=True, text=True)
    lines = x.stdout.split('\n')
    for line in filter(lambda l : l.startswith(prefix), lines):
        prop, _, value = line.partition(':\t')
        props[prop] = value
    return props

xresources = read_xresources("*")

c.colors.statusbar.normal.bg = "#CC000000"
c.colors.statusbar.command.bg = "#CC000000"
c.colors.statusbar.command.fg = xresources["*.foreground"]
c.colors.statusbar.normal.fg = xresources["*.color14"]
c.colors.statusbar.passthrough.fg = xresources["*.color14"]
c.colors.statusbar.url.fg = xresources["*.color13"]
c.colors.statusbar.url.success.https.fg = xresources["*.color13"]
c.colors.statusbar.url.hover.fg = xresources["*.color12"]

c.colors.tabs.even.bg = "#CC000000"
c.colors.tabs.odd.bg = "#CC000000"
c.colors.tabs.bar.bg = "#CC000000"
c.colors.tabs.even.fg = xresources["*.foreground"]
c.colors.tabs.odd.fg = xresources["*.foreground"]
c.colors.tabs.selected.even.bg = xresources["*.foreground"]
c.colors.tabs.selected.odd.bg = xresources["*.foreground"]
c.colors.tabs.selected.even.fg = xresources["*.background"]
c.colors.tabs.selected.odd.fg = xresources["*.background"]
c.colors.hints.bg = xresources["*.background"]
c.colors.hints.fg = xresources["*.foreground"]
c.tabs.show = "multiple"

c.colors.completion.item.selected.match.fg = xresources["*.color6"]
c.colors.completion.match.fg = xresources["*.color6"]
c.colors.tabs.indicator.start = xresources["*.color10"]
c.colors.tabs.indicator.stop = xresources["*.color8"]
c.colors.completion.odd.bg = xresources["*.background"]
c.colors.completion.even.bg = xresources["*.background"]
c.colors.completion.fg = xresources["*.foreground"]
c.colors.completion.category.bg = xresources["*.background"]
c.colors.completion.category.fg = xresources["*.foreground"]
c.colors.completion.item.selected.bg = xresources["*.background"]
c.colors.completion.item.selected.fg = xresources["*.foreground"]

c.colors.messages.info.bg = xresources["*.background"]
c.colors.messages.info.fg = xresources["*.foreground"]
c.colors.messages.error.bg = xresources["*.background"]
c.colors.messages.error.fg = xresources["*.foreground"]
c.colors.downloads.error.bg = xresources["*.background"]
c.colors.downloads.error.fg = xresources["*.foreground"]
c.colors.downloads.bar.bg = xresources["*.background"]
c.colors.downloads.start.bg = xresources["*.color10"]
c.colors.downloads.start.fg = xresources["*.foreground"]
c.colors.downloads.stop.bg = xresources["*.color8"]
c.colors.downloads.stop.fg = xresources["*.foreground"]

c.colors.tooltip.bg = xresources["*.background"]
c.colors.webpage.bg = xresources["*.background"]
c.hints.border = xresources["*.foreground"]

c.tabs.title.format = "{audio}{current_title}"
c.fonts.web.size.default = 20

c.url.searchengines = {
        'DEFAULT': 'https://duckduckgo.com/?q={}',
        '!aw': 'https://wiki.archlinux.org/?search={}',
        '!gh': 'https://github.com/search?o=desc&q={}&s=stars',
        '!yt': 'https://www.youtube.com/results?search_query={}',
        }

c.completion.open_categories = ['searchengines', 'quickmarks', 'bookmarks', 'history', 'filesystem']

config.load_autoconfig()
c.auto_save.session = True

# keybindings
config.bind('=', 'cmd-set-text -s :open')
config.bind('h', 'history')
config.bind('cs', 'cmd-set-text -s :config-source')
config.bind('tH', 'config-cycle tabs.show multiple never')
config.bind('sH', 'config-cycle statusbar.show always never')
config.bind('T', 'hint links tab')
config.bind('pP', 'open -- {primary}')
config.bind('pp', 'open -- {clipboard}')
config.bind('pt', 'open -t -- {clipboard}')
config.bind('qm', 'macro-record')
config.bind('tT', 'config-cycle tabs.position top left')
config.bind('gJ', 'tab-move +')
config.bind('gK', 'tab-move -')
config.bind('gm', 'tab-move')

# dark mode
c.colors.webpage.darkmode.enabled = True
c.colors.webpage.darkmode.algorithm = 'lightness-cielab'
c.colors.webpage.darkmode.policy.images = 'never'
config.set('colors.webpage.darkmode.enabled', False, 'file://*')

# styles, cosmetics
c.tabs.padding = {'top': 5, 'bottom': 5, 'left': 9, 'right': 9}
c.tabs.indicator.width = 0
c.tabs.width = '7%'

# fonts
c.fonts.default_family = []
c.fonts.default_size = '13pt'
c.fonts.web.family.fixed = 'monospace'
c.fonts.web.family.sans_serif = 'monospace'
c.fonts.web.family.serif = 'monospace'
c.fonts.web.family.standard = 'monospace'

# privacy + performance
# WebGL stays OFF - this avoids the Intel GPU crashes/slowness you hit in Brave
config.set("content.webgl", False, "*")
config.set("content.canvas_reading", False)
config.set("content.geolocation", False)
config.set("content.webrtc_ip_handling_policy", "default-public-interface-only")
config.set("content.cookies.accept", "all")
config.set("content.cookies.store", True)

# --- ADBLOCK: enabled properly since you already have python-adblock installed ---
c.content.blocking.enabled = True
c.content.blocking.method = 'both'
c.content.blocking.adblock.lists = [
        "https://github.com/uBlockOrigin/uAssets/raw/master/filters/legacy.txt",
        "https://github.com/uBlockOrigin/uAssets/raw/master/filters/filters.txt",
        "https://github.com/uBlockOrigin/uAssets/raw/master/filters/badware.txt",
        "https://github.com/uBlockOrigin/uAssets/raw/master/filters/privacy.txt",
        "https://github.com/uBlockOrigin/uAssets/raw/master/filters/annoyances.txt",
        "https://easylist.to/easylist/easylist.txt",
        "https://easylist.to/easylist/easyprivacy.txt",
]
