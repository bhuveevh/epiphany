#!/bin/sh
# Packages a staged Meson install tree into an installable .deb.
# Usage: sh .github/make-deb.sh <version>
set -e

VERSION="${1:-1.0.0}"
PKGNAME="polecat-web"
STAGE="$PWD/stage"
PKG="$PWD/pkg"

if [ ! -d "$STAGE/usr" ]; then
    echo "ERROR: nothing staged in $STAGE" >&2
    exit 1
fi

rm -rf "$PKG"
mkdir -p "$PKG/DEBIAN"
cp -a "$STAGE/." "$PKG/"

# Make every staged shared library visible to the linker, otherwise
# dpkg-shlibdeps cannot follow the dependency chain and the Depends line comes
# out far too short.
if [ -d "$PKG/usr/lib/x86_64-linux-gnu" ]; then
    cp -a "$PKG/usr/lib/x86_64-linux-gnu/." /usr/lib/x86_64-linux-gnu/ 2>/dev/null || true
    ldconfig 2>/dev/null || true
fi

mkdir -p debian
cat > debian/control <<EOF
Source: $PKGNAME
Section: gnome
Priority: optional
Maintainer: Bhuvee Paswan <bhuveepaswan@gmail.com>
Standards-Version: 4.7.0
Build-Depends: debhelper-compat (= 13)

Package: $PKGNAME
Architecture: any
Depends: \${shlibs:Depends}, \${misc:Depends}
Description: GNOME Web (Epiphany) based browser with a custom interface
EOF

# Every ELF we shipped (the app, and the web process extensions).
BIN=""
for cand in $(find "$PKG/usr/bin" "$PKG/usr/libexec" "$PKG/usr/lib/x86_64-linux-gnu" -type f 2>/dev/null); do
    case "$(file -b "$cand" 2>/dev/null)" in
        *ELF*) BIN="$BIN -e $cand" ;;
    esac
done

DEPS=""
if command -v dpkg-shlibdeps >/dev/null 2>&1; then
    dpkg-shlibdeps -O $BIN > /tmp/shlibdeps.out 2> /tmp/shlibdeps.err || true
    sed -n '1,15p' /tmp/shlibdeps.err || true
    DEPS=$(sed -n 's/^shlibs:Depends=//p' /tmp/shlibdeps.out | tr '\n' ' ')
fi

if [ -z "$DEPS" ]; then
    echo "NOTE: dpkg-shlibdeps produced nothing, using the fallback list"
    DEPS="libc6, libglib2.0-0t64, libgtk-4-1, libadwaita-1-0, libwebkitgtk-6.0-4, libsoup-3.0-0, libjson-glib-1.0-0, libsecret-1-0, libgcr-4-4, libgdk-pixbuf-2.0-0, libportal-gtk4-1, libarchive13t64, libnettle8t64, libsqlite3-0, libxml2, libxslt1.1, libgstreamer1.0-0"
fi

cat > "$PKG/DEBIAN/control" <<EOF
Package: $PKGNAME
Version: $VERSION
Section: gnome
Priority: optional
Architecture: amd64
Maintainer: Bhuvee Paswan <bhuveepaswan@gmail.com>
Installed-Size: $(du -sk "$PKG" | cut -f1)
Depends: $DEPS
Description: GNOME Web (Epiphany) based browser with a custom interface
 A GTK4 / libadwaita web browser derived from GNOME Web (Epiphany),
 using the WebKitGTK engine, with a custom user interface.
EOF

mkdir -p "$PKG/usr/share/doc/$PKGNAME"
if [ -f COPYING ]; then
    cp COPYING "$PKG/usr/share/doc/$PKGNAME/copyright"
fi

OUT="${PKGNAME}_${VERSION}_amd64.deb"
dpkg-deb --build --root-owner-group "$PKG" "$OUT"
echo "Built $OUT"
