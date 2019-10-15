# Create a virtual environment.
virtualenv -p python3 ./visual-questioner-env

# Activate the virtual environment.
source ./visual-questioner-env/bin/activate

# Install libffi.
if [ "$(uname)" == "Darwin" ]; then
  brew install libffi
else
  sudo apt-get install libffi6 libffi-dev
fi

# Upgrade pip.
pip install --upgrade pip

# Install setuptools.
pip install -U pip setuptools
pip install setuptools_scm

# Install requests[security].
pip install requests
pip install 'requests[security]'

# Install correct versions of Python modules.
pip install -r requirements.txt
