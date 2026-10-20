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
# dpkg-shlibdeps cannot follow the dependency chain.
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

# Every ELF we shipped (the app and the web process extensions).
# NOTE: detect ELF from the file header, not with `file`, which is not
# guaranteed to be installed in a minimal container.
is_elf() {
    [ "$(head -c 4 "$1" 2>/dev/null | od -An -tx1 | tr -d ' \n')" = "7f454c46" ]
}

BIN=""
for cand in $(find "$PKG/usr/bin" "$PKG/usr/libexec" "$PKG/usr/lib/x86_64-linux-gnu" -type f 2>/dev/null); do
    if is_elf "$cand"; then
        BIN="$BIN -e $cand"
    fi
done

if [ -z "$BIN" ]; then
    echo "ERROR: found no ELF binaries to analyse" >&2
    exit 1
fi

echo "Analysing: $BIN"

DEPS=""
dpkg-shlibdeps -O $BIN > /tmp/shlibdeps.out 2> /tmp/shlibdeps.err || true
sed -n '1,25p' /tmp/shlibdeps.err || true
DEPS=$(sed -n 's/^shlibs:Depends=//p' /tmp/shlibdeps.out | tr '\n' ' ')

if [ -z "$DEPS" ]; then
    # Never ship a guessed dependency list: a wrong package name makes the
    # whole package uninstallable. Fail instead.
    echo "ERROR: dpkg-shlibdeps produced no dependencies" >&2
    exit 1
fi

echo "Depends: $DEPS"

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
echo "----- control -----"
dpkg-deb --info "$OUT" | sed -n '1,14p'
