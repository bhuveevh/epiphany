#!/usr/bin/env python3
"""Polecat: the New Tab page (hero + wallpaper) and the "this is a fork" note.

Run from the Epiphany source root:  python3 apply-polecat-newtab.py .

  * New Tab page (ephy-about:newtab): a big live clock, a greeting with the
    system user name, a search box, and the user's wallpaper behind it. The
    most-visited grid that Epiphany already renders stays below it.
  * The About dialog gets a note saying this is an unofficial fork.
  * The distributor shown in About > Troubleshooting becomes "Polecat".

Written without backslashes: BS is a literal backslash and NL a newline, and
the C string literal is escaped at run time by c_literal().
"""
import os
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."

BS = chr(92)
NL = chr(10)

WALL_LIGHT = """<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 1920 1080"
     preserveAspectRatio="xMidYMid slice"
     >
  <rect width="1920" height="1080" fill="#c7e8df"/>
  <circle cx="1510" cy="205" r="66" fill="#ffe9ae"/>
  <path d="M0 640 Q280 420 560 620 T1120 580 T1680 590 T2240 620
           V1080 H0Z" fill="#93c2a4"/>
  <path d="M0 750 Q300 560 610 700 T1240 670 T1840 680 T2300 720
           V1080 H0Z" fill="#659779"/>
  <path d="M0 820 Q440 730 850 810 T1640 790 T2300 820 V1080 H0Z"
        fill="#3f7058"/>
  <g fill="#4c805f">
    <path d="M200 750 250 620l50 130h-31l48 75H183l48-75Z"/>
    <path d="M385 755 430 640l45 115h-28l43 68H370l43-68Z"/>
    <path d="M1480 750 1530 620l50 130h-31l48 75h-134l48-75Z"/>
    <path d="M1680 760 1725 645l45 115h-28l43 68h-120l43-68Z"/>
  </g>
  <g fill="#315d4b">
    <path d="M-60 1000 65 690l125 310h-78l115 175H-102l115-175Z"/>
    <path d="M195 1030 300 770l105 260h-65l98 145H162l98-145Z"/>
    <path d="M1650 1020 1760 745l110 275h-68l103 155h-290l103-155Z"/>
    <path d="M1870 1000 1985 710l115 290h-72l108 165h-287l108-165Z"/>
  </g>
  <g fill="none" stroke="#244f40" stroke-width="7" stroke-linecap="round">
    <path d="M530 900q-5-55 8-108m-5 75q-30-24-47-19m50-14q27-23 45-19"/>
    <path d="M720 930q-7-48 4-91m-3 60q-24-18-39-14m41-13q22-19 38-15"/>
    <path d="M1345 910q-4-50 7-96m-4 66q-25-20-42-16m44-14q23-20 40-16"/>
  </g>
  <g fill="#6ba17a">
    <ellipse cx="486" cy="848" rx="23" ry="10" transform="rotate(28 486 848)"/>
    <ellipse cx="581" cy="834" rx="23" ry="10" transform="rotate(-28 581 834)"/>
    <ellipse cx="682" cy="885" rx="19" ry="8" transform="rotate(28 682 885)"/>
    <ellipse cx="762" cy="870" rx="19" ry="8" transform="rotate(-28 762 870)"/>
    <ellipse cx="1309" cy="851" rx="21" ry="9" transform="rotate(28 1309 851)"/>
    <ellipse cx="1377" cy="837" rx="21" ry="9" transform="rotate(-28 1377 837)"/>
  </g>
  <g>
    <g transform="translate(538 784)">
      <circle cx="0" cy="-15" r="10" fill="#fff7e8"/>
      <circle cx="14" cy="-5" r="10" fill="#fff7e8"/>
      <circle cx="9" cy="12" r="10" fill="#fff7e8"/>
      <circle cx="-9" cy="12" r="10" fill="#fff7e8"/>
      <circle cx="-14" cy="-5" r="10" fill="#fff7e8"/>
      <circle r="7" fill="#f2bd66"/>
    </g>
    <g transform="translate(724 824)">
      <circle cx="0" cy="-13" r="8" fill="#f8d9e3"/>
      <circle cx="12" cy="-4" r="8" fill="#f8d9e3"/>
      <circle cx="7" cy="10" r="8" fill="#f8d9e3"/>
      <circle cx="-7" cy="10" r="8" fill="#f8d9e3"/>
      <circle cx="-12" cy="-4" r="8" fill="#f8d9e3"/>
      <circle r="6" fill="#f2bd66"/>
    </g>
    <g transform="translate(1350 768)">
      <circle cx="0" cy="-14" r="9" fill="#fff7e8"/>
      <circle cx="13" cy="-4" r="9" fill="#fff7e8"/>
      <circle cx="8" cy="11" r="9" fill="#fff7e8"/>
      <circle cx="-8" cy="11" r="9" fill="#fff7e8"/>
      <circle cx="-13" cy="-4" r="9" fill="#fff7e8"/>
      <circle r="6" fill="#f2bd66"/>
    </g>
  </g>
  </svg>
"""

WALL_DARK = """<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 1920 1080"
     preserveAspectRatio="xMidYMid slice"
     >
    <rect width="1920" height="1080" fill="#18283b"/>
    <circle cx="1510" cy="205" r="60" fill="#e4eaff"/>
    <path d="M0 640 Q280 420 560 620 T1120 580 T1680 590 T2240 620
             V1080 H0Z" fill="#354e5a"/>
    <path d="M0 750 Q300 560 610 700 T1240 670 T1840 680 T2300 720
             V1080 H0Z" fill="#293f49"/>
    <path d="M0 820 Q440 730 850 810 T1640 790 T2300 820 V1080 H0Z"
          fill="#1b3435"/>
    <g fill="#294744">
      <path d="M200 750 250 620l50 130h-31l48 75H183l48-75Z"/>
      <path d="M385 755 430 640l45 115h-28l43 68H370l43-68Z"/>
      <path d="M1480 750 1530 620l50 130h-31l48 75h-134l48-75Z"/>
      <path d="M1680 760 1725 645l45 115h-28l43 68h-120l43-68Z"/>
    </g>
    <g fill="#142d30">
      <path d="M-60 1000 65 690l125 310h-78l115 175H-102l115-175Z"/>
      <path d="M195 1030 300 770l105 260h-65l98 145H162l98-145Z"/>
      <path d="M1650 1020 1760 745l110 275h-68l103 155h-290l103-155Z"/>
      <path d="M1870 1000 1985 710l115 290h-72l108 165h-287l108-165Z"/>
    </g>
    <g fill="none" stroke="#9ab99a" stroke-width="7" stroke-linecap="round">
      <path d="M530 900q-5-55 8-108m-5 75q-30-24-47-19m50-14q27-23 45-19"/>
      <path d="M720 930q-7-48 4-91m-3 60q-24-18-39-14m41-13q22-19 38-15"/>
      <path d="M1345 910q-4-50 7-96m-4 66q-25-20-42-16m44-14q23-20 40-16"/>
    </g>
    <g fill="#8eaf8a">
      <ellipse cx="486" cy="848" rx="23" ry="10" transform="rotate(28 486 848)"/>
      <ellipse cx="581" cy="834" rx="23" ry="10" transform="rotate(-28 581 834)"/>
      <ellipse cx="682" cy="885" rx="19" ry="8" transform="rotate(28 682 885)"/>
      <ellipse cx="762" cy="870" rx="19" ry="8" transform="rotate(-28 762 870)"/>
      <ellipse cx="1309" cy="851" rx="21" ry="9" transform="rotate(28 1309 851)"/>
      <ellipse cx="1377" cy="837" rx="21" ry="9" transform="rotate(-28 1377 837)"/>
    </g>
    <g>
      <g transform="translate(538 784)">
        <circle cy="-15" r="10" fill="#fff2d8"/><circle cx="14" cy="-5" r="10" fill="#fff2d8"/>
        <circle cx="9" cy="12" r="10" fill="#fff2d8"/><circle cx="-9" cy="12" r="10" fill="#fff2d8"/>
        <circle cx="-14" cy="-5" r="10" fill="#fff2d8"/><circle r="7" fill="#e7b966"/>
      </g>
      <g transform="translate(724 824)">
        <circle cy="-13" r="8" fill="#eabacb"/><circle cx="12" cy="-4" r="8" fill="#eabacb"/>
        <circle cx="7" cy="10" r="8" fill="#eabacb"/><circle cx="-7" cy="10" r="8" fill="#eabacb"/>
        <circle cx="-12" cy="-4" r="8" fill="#eabacb"/><circle r="6" fill="#e7b966"/>
      </g>
      <g transform="translate(1350 768)">
        <circle cy="-14" r="9" fill="#fff2d8"/><circle cx="13" cy="-4" r="9" fill="#fff2d8"/>
        <circle cx="8" cy="11" r="9" fill="#fff2d8"/><circle cx="-8" cy="11" r="9" fill="#fff2d8"/>
        <circle cx="-13" cy="-4" r="9" fill="#fff2d8"/><circle r="6" fill="#e7b966"/>
      </g>
    </g>
  </svg>
"""

HERO_HEAD = """<style>
#polecat-hero{text-align:center;margin:26px auto 6px;max-width:720px;padding:0 16px}
#polecat-clock{font-size:clamp(44px,7vw,76px);font-weight:700;letter-spacing:-2px;line-height:1;color:#fff;text-shadow:0 2px 18px rgba(0,0,0,.45)}
#polecat-date{font-size:13px;color:#fff;opacity:.92;margin-top:4px;text-shadow:0 1px 10px rgba(0,0,0,.55)}
#polecat-welcome{font-size:15px;color:#fff;margin:12px 0 14px;text-shadow:0 1px 10px rgba(0,0,0,.55)}
#polecat-search{width:100%;box-sizing:border-box;height:50px;padding:0 22px;border-radius:25px;border:1px solid rgba(255,255,255,.65);background:rgba(255,255,255,.9);color:#202124;font-size:15px;outline:none;box-shadow:0 6px 22px rgba(0,0,0,.22)}
#polecat-search:focus{background:#fff}
body{background-image:url("ephy-resource:///org/gnome/epiphany/page-templates/wallpaper-light.svg");background-size:cover;background-position:center center;background-repeat:no-repeat;background-attachment:fixed}
@media (prefers-color-scheme:dark){
body{background-image:url("ephy-resource:///org/gnome/epiphany/page-templates/wallpaper-dark.svg")}
#polecat-search{background:rgba(28,34,44,.82);color:#eaeaea;border-color:rgba(255,255,255,.16)}
}
</style>
<div id="polecat-hero">
<div id="polecat-clock">--:--</div>
<div id="polecat-date"></div>
<div id="polecat-welcome">Welcome, """

HERO_TAIL = """</div>
<form id="polecat-searchform" autocomplete="off">
<input id="polecat-search" type="text" placeholder="Search anything with Polecat Browser&#8230;   Type Here">
</form>
</div>
<script>
(function () {
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function tick() {
    var d = new Date();
    var c = document.getElementById('polecat-clock');
    if (c) { c.textContent = pad(d.getHours()) + ':' + pad(d.getMinutes()); }
    var e = document.getElementById('polecat-date');
    if (e) {
      try { e.textContent = d.toLocaleDateString(undefined, { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }); }
      catch (x) { e.textContent = d.toDateString(); }
    }
  }
  tick();
  setInterval(tick, 1000);
  var f = document.getElementById('polecat-searchform');
  if (f) {
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var v = document.getElementById('polecat-search').value.trim();
      if (!v) { return; }
      var isUrl = /^(https?:[//]|about:|file:|ftp:)/i.test(v) || (/^[^ ]+[.][^ ]{2,}/.test(v) && v.indexOf(' ') === -1);
      location.href = isUrl ? (/^[a-z]+:/i.test(v) ? v : ('https://' + v)) : ('https://duckduckgo.com/?q=' + encodeURIComponent(v));
    });
  }
})();
</script>
"""


def path(rel):
    return os.path.join(ROOT, rel)


def write(rel, text):
    with open(path(rel), "w", encoding="utf-8") as fh:
        fh.write(text)


def c_literal(text):
    """Escape a chunk of HTML/CSS/JS into a C string literal."""
    out = text.replace(BS, BS + BS).replace('"', BS + '"').replace(NL, BS + 'n')
    return '"' + out + '"'


def sub(rel, pairs):
    if not os.path.exists(path(rel)):
        sys.exit("ERROR: missing file " + rel)
    text = open(path(rel), encoding="utf-8").read()
    for old, new in pairs:
        if old not in text:
            sys.exit("ERROR: anchor not found in %s: %r" % (rel, old[:70]))
        text = text.replace(old, new)
    write(rel, text)
    print("  patched " + rel)


print("Polecat New Tab page + fork notice")

# --- the wallpaper, as page-template resources ------------------------------
write("src/resources/wallpaper-light.svg", WALL_LIGHT)
write("src/resources/wallpaper-dark.svg", WALL_DARK)
print("  wrote the wallpapers")

sub("src/resources/epiphany.gresource.xml", [
    ('<file compressed="true">about.css</file>',
     '<file compressed="true">about.css</file>' + NL +
     '    <file compressed="true">wallpaper-light.svg</file>' + NL +
     '    <file compressed="true">wallpaper-dark.svg</file>'),
])

# --- the New Tab page -------------------------------------------------------
HERO_C = (
    "  /* ---- Polecat new tab hero --------------------------------------- */" + NL +
    "  {" + NL +
    "    g_autofree char *polecat_user = g_markup_escape_text (g_get_user_name (), -1);" + NL +
    "" + NL +
    "    g_string_append (data_str," + NL +
    "                     " + c_literal(HERO_HEAD) + ");" + NL +
    "    g_string_append (data_str, polecat_user);" + NL +
    "    g_string_append (data_str," + NL +
    "                     " + c_literal(HERO_TAIL) + ");" + NL +
    "  }" + NL
)

sub("embed/ephy-about-handler.c", [
    ("  g_free (lang);" + NL, "  g_free (lang);" + NL + NL + HERO_C),
    ('_("Welcome to Web")', '_("Welcome to Polecat")'),
])

# --- the About dialog: say plainly that this is a fork ----------------------
sub("src/window-commands.c", [
    ("  adw_about_dialog_set_version (dialog, ",
     "  adw_about_dialog_set_comments (dialog," + NL +
     "                                 _(" + '"Polecat is an unofficial fork of GNOME Web (Epiphany).' + BS + 'n"' + NL +
     '                                   "Not affiliated with, or endorsed by, the GNOME Project."));' + NL +
     "  adw_about_dialog_set_version (dialog, "),
])

sub("meson.build", [
    ("  distributor_name = r.stdout().strip()",
     "  distributor_name = 'Polecat (fork of GNOME Web)'"),
])

print("Polecat New Tab page + fork notice applied.")
