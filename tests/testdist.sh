# This script allows you to test the package
# Run with . ./testdist (should be sourced so that cd works)

rm -r dist
pip uninstall SAPsim -y
python3 setup.py sdist
# There will be only one file
for file in dist/*; do
    pip install $file;
done

# Need to test from directory that isn't SAPsim/
# Importing SAPsim stuff from SAPsim directory will import from the SAPsim directory
# Not the pip package
cd ..
