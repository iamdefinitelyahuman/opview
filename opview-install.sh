#!/bin/bash

OS="`uname`"
PY="python3"

cd /usr/local/lib
git clone --depth=1 https://github.com/HyperLink-Technology/opview

case "$OS" in 'Linux')
    chown "$USER:$USER" opview -R
    case "`which python3.6`" in "") ;; *) PY="python3.6";; esac
    case "`which python3.7`" in "") ;; *) PY="python3.7";; esac
;; esac

PY_VER=`$PY -c 'import sys; print(sys.version_info[1])'`

if (( $PY_VER < 6 ))
then
echo "ERROR: Opview requires python3.6 or greater."
exit 1
fi

cd opview
$PY -m venv venv

echo '#!/bin/bash' > /usr/local/bin/opview
echo 'source /usr/local/lib/opview/venv/bin/activate' >> /usr/local/bin/opview
echo 'python /usr/local/lib/opview "$@"' >> /usr/local/bin/opview
chmod +x /usr/local/bin/opview
