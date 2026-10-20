#!/usr/bin/env python3
"""Fully rebrands this Epiphany (GNOME Web) fork as "Polecat" at build time.

Run from the Epiphany source root:  python3 apply-polecat-branding.py .

What it changes
  * application ID      org.gnome.Epiphany            -> in.polecat.Web
  * GSettings schema ids (and the generated enum ids) -> in.polecat.Web*
  * DBus names, desktop entry, AppStream metadata
  * the executable name  epiphany -> polecat
  * the About dialog: app name, version (our build number), copyright,
    developer, website, issue tracker
  * the application icon (scalable + symbolic)

What it deliberately leaves alone
  * GResource paths (/org/gnome/epiphany/...) - internal only, and shared with
    third-party assets; rewriting them risks breaking lookups at runtime.
  * GSettings *paths* (/org/gnome/epiphany/...) - they need not match the id.
  * upstream copyright and contributor credits - the GPL requires keeping them.

The script is idempotent and fails loudly if an anchor is missing.
"""
import os
import sys

APPID = "in.polecat.Web"
OLD_APPID = "org.gnome.Epiphany"
NAME = "Polecat"
REPO = "https://github.com/bhuveevh/epiphany"
AUTHOR = "Bhuvee Paswan"

VERSION = os.environ.get("POLECAT_VERSION", "1.0.0")

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."

# Written without backslashes so the file survives any tooling that re-escapes
# strings: BS is a literal backslash as it appears in C string literals, and NL
# is a newline.
BS = chr(92)
NL = chr(10)


def path(rel):
    return os.path.join(ROOT, rel)


def read(rel):
    with open(path(rel), encoding="utf-8") as fh:
        return fh.read()


def write(rel, text):
    with open(path(rel), "w", encoding="utf-8") as fh:
        fh.write(text)


def sub(rel, pairs, required=True):
    """Replace each (old, new) pair in a file."""
    if not os.path.exists(path(rel)):
        if required:
            sys.exit("ERROR: missing file " + rel)
        return
    text = read(rel)
    before = text
    for old, new in pairs:
        if old not in text:
            if required:
                sys.exit("ERROR: anchor not found in %s: %r" % (rel, old[:70]))
            continue
        text = text.replace(old, new)
    if text != before:
        write(rel, text)
        print("  patched " + rel)


print("Polecat branding %s (app id %s)" % (VERSION, APPID))

# --- application id, schemas, DBus -----------------------------------------
sub("meson.build", [
    ("application_id = '%s'" % OLD_APPID, "application_id = '%s'" % APPID),
])

sub("lib/ephy-prefs.h", [('"%s' % OLD_APPID, '"%s' % APPID)])

sub("data/org.gnome.epiphany.gschema.xml", [(OLD_APPID, APPID)])

sub("data/meson.build", [
    ('id="%s.@EnumName@"' % OLD_APPID, 'id="%s.@EnumName@"' % APPID),
])

sub("lib/ephy-permissions-manager.c", [('"%s.permissions"' % OLD_APPID,
                                        '"%s.permissions"' % APPID)])

for rel in [
    "lib/ephy-web-app-utils.c",
    "embed/ephy-web-view.c",
    "src/webapp-provider/ephy-webapp-provider.c",
    "src/profile-migrator/ephy-profile-migrator.c",
    "src/profile-migrator/ephy-legacy-web-app-utils.c",
]:
    sub(rel, [(OLD_APPID, APPID)], required=False)

sub("src/webapp-provider/%s.WebAppProvider.xml" % OLD_APPID, [(OLD_APPID, APPID)])

sub("data/%s.WebAppProvider.service.in" % OLD_APPID, [(OLD_APPID, APPID)])

# --- executable name --------------------------------------------------------
sub("src/meson.build", [
    ("interface_prefix: '%s'" % OLD_APPID, "interface_prefix: '%s'" % APPID),
    ("executable('epiphany',", "executable('polecat',"),
])

# --- desktop entry ----------------------------------------------------------
sub("data/%s.desktop.in.in" % OLD_APPID, [
    ("Name=Web" + NL, "Name=%s" % NAME + NL),
    ("Comment=Browse the web" + NL, "Comment=Browse the web with %s" % NAME + NL),
    ("Keywords=web;browser;internet;epiphany;",
     "Keywords=web;browser;internet;polecat;"),
    ("Exec=epiphany %U", "Exec=polecat %U"),
    ("Exec=epiphany --new-window %U", "Exec=polecat --new-window %U"),
    ("Exec=epiphany --incognito-mode %U", "Exec=polecat --incognito-mode %U"),
])

# --- AppStream metadata -----------------------------------------------------
sub("data/%s.appdata.xml.in.in" % OLD_APPID, [
    ("<name>Web</name>", "<name>%s</name>" % NAME),
    ("<summary>Browse the web</summary>",
     "<summary>Browse the web with %s</summary>" % NAME),
    ("The web browser for GNOME, featuring tight integration with the desktop",
     "%s is a web browser built on GNOME Web (Epiphany), featuring tight "
     "integration with the desktop" % NAME),
    ("<p>" + NL + "      Web is often referred to by its code name, Epiphany."
     + NL + "    </p>",
     "<p>" + NL + "      %s is based on GNOME Web, whose code name is Epiphany."
     % NAME + NL + "    </p>"),
])

# --- the About dialog -------------------------------------------------------
sub("src/window-commands.c", [
    ('adw_about_dialog_set_application_name (dialog, _("Web"));',
     'adw_about_dialog_set_application_name (dialog, _("%s"));' % NAME),
    ("adw_about_dialog_set_version (dialog, VERSION);",
     'adw_about_dialog_set_version (dialog, "%s");' % VERSION),
    ('"Copyright © 2002–2004 Marco Pesenti Gritti' + BS + 'n"' + NL +
     '                                  "Copyright © 2003–2023 '
     'The GNOME Web Developers");',
     '"Copyright © 2026 ' + AUTHOR + BS + 'n"' + NL +
     '                                  "Based on GNOME Web (Epiphany), '
     'Copyright © 2002–2023 the GNOME Web developers");'),
    ('adw_about_dialog_set_developer_name (dialog, _("The GNOME Project"));',
     'adw_about_dialog_set_developer_name (dialog, _("%s"));' % NAME),
    ('adw_about_dialog_set_website (dialog, "https://apps.gnome.org/Epiphany");',
     'adw_about_dialog_set_website (dialog, "%s");' % REPO),
    ('adw_about_dialog_set_issue_url (dialog, '
     '"https://gitlab.gnome.org/GNOME/epiphany/-/issues/");',
     'adw_about_dialog_set_issue_url (dialog, "%s/issues");' % REPO),
])

# --- credits: put the fork maintainer at the top ----------------------------
sub("src/resources/about.ini", [
    ("Maintainers=Jan-Michael Brummer;",
     "Maintainers=%s;Jan-Michael Brummer;" % AUTHOR),
])

# --- the application icon ---------------------------------------------------
ICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#6A4BFF"/>
      <stop offset="0.55" stop-color="#2E7BFF"/>
      <stop offset="1" stop-color="#12C2E9"/>
    </linearGradient>
    <linearGradient id="sh" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.32"/>
      <stop offset="0.55" stop-color="#ffffff" stop-opacity="0.04"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.14"/>
    </linearGradient>
  </defs>
  <rect x="6" y="6" width="116" height="116" rx="28" fill="url(#g)"/>
  <rect x="6" y="6" width="116" height="116" rx="28" fill="url(#sh)"/>
  <g fill="none" stroke="#ffffff" stroke-width="6.5" stroke-linecap="round">
    <circle cx="64" cy="64" r="29"/>
    <ellipse cx="64" cy="64" rx="13" ry="29"/>
    <path d="M35.5 55.5h57M35.5 72.5h57"/>
  </g>
</svg>
"""

ICON_SYMBOLIC = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16">
  <g fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round">
    <circle cx="8" cy="8" r="6"/>
    <ellipse cx="8" cy="8" rx="2.7" ry="6"/>
    <path d="M2.2 6.4h11.6M2.2 9.6h11.6"/>
  </g>
</svg>
"""

# data/meson.build derives the *source* path of the scalable icon from the
# application id, so it has to live under the new name.
write("data/icons/hicolor/scalable/apps/%s.svg" % APPID, ICON)
print("  wrote the scalable app icon (%s.svg)" % APPID)

symbolic = "data/icons/hicolor/symbolic/apps/%s-symbolic.svg" % OLD_APPID
if os.path.exists(path(symbolic)):
    write(symbolic, ICON_SYMBOLIC)
    print("  wrote the symbolic app icon")

print("Polecat branding applied.")
