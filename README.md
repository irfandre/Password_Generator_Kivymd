# update ubuntu
sudo apt-get update
# install pre-requisuites
sudo apt-get install python3-dev
#create virtualenv
python3 -m venv env

# install all requirements 
pip install -r buildozer-requirement.txt
