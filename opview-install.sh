#!/bin/bash

cd /usr/local/lib
git clone --depth=1 https://github.com/iamdefinitelyahuman/opview
chmod -R 777 /usr/local/lib/opview
cd opview
python3.6 -m venv venv

echo '#!/bin/bash' > /usr/local/bin/opview
echo 'source /usr/local/lib/opview/venv/bin/activate' >> /usr/local/bin/opview
echo 'python /usr/local/lib/opview "$@"' >> /usr/local/bin/opview
chmod +x /usr/local/bin/opview
