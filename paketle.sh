#!/bin/bash

# Değişkenler
APP_NAME="iman-ahlak-ilmihali"
VERSION="1.0.0"
DEB_DIR="iman_ilmihali_paket"
INSTALL_DIR="/opt/$APP_NAME"

echo "📦 Paketleme işlemi başlıyor: $APP_NAME..."

# 1. Temizlik ve Klasör Yapısı Oluşturma
rm -rf $DEB_DIR
mkdir -p $DEB_DIR$INSTALL_DIR
mkdir -p $DEB_DIR/usr/share/applications
mkdir -p $DEB_DIR/DEBIAN

# 2. Dosyaları Kopyalama
cp iman.py $DEB_DIR$INSTALL_DIR/
cp iman.png $DEB_DIR$INSTALL_DIR/
cp -r konular $DEB_DIR$INSTALL_DIR/

# 3. Control Dosyası Oluşturma
cat <<EOF > $DEB_DIR/DEBIAN/control
Package: $APP_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Maintainer: mobilturka
Depends: python3, python3-pyqt6
Description: İman ve Ahlak İlmihali Uygulaması.
 PyQt6 tabanlı ilmihal okuyucu.
EOF

# 4. Masaüstü Başlatıcı (.desktop) Oluşturma
cat <<EOF > $DEB_DIR/usr/share/applications/$APP_NAME.desktop
[Desktop Entry]
Name=İman ve Ahlak İlmihali
Exec=python3 $INSTALL_DIR/iman.py
Icon=$INSTALL_DIR/iman.png
Terminal=false
Type=Application
Categories=Education;
Comment=İman ve Ahlak İlmihali uygulaması
EOF

# 5. İzinleri Ayarlama
chmod -R 755 $DEB_DIR/DEBIAN
chmod -R 755 $DEB_DIR/opt/$APP_NAME
chmod 644 $DEB_DIR/usr/share/applications/$APP_NAME.desktop

# 6. Paketleme
dpkg-deb --build $DEB_DIR

# 7. Sonuç
mv $DEB_DIR.deb ${APP_NAME}_${VERSION}_all.deb
rm -rf $DEB_DIR

echo "✅ Paket başarıyla oluşturuldu: ${APP_NAME}_${VERSION}_all.deb"
echo "🚀 Kurmak için: sudo apt install ./${APP_NAME}_${VERSION}_all.deb"