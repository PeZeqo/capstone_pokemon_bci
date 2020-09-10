#!/bin/sh
echo "Please ensure that you have python 3.8.* installed."

# In case you are currently in an env, we deactivate it.
set +e
./capstone-env/Scripts/deactivate.bat
set -e

# Create and enter the environment
pwd
./crypto_env/Scripts/activate.bat


cleanup() {
  echo "========== PYTHON CODE COMPLETED =========="
  ./crypto_env/Scripts/deactivate.bat
}

# Launch the script, and then deactivate the env.
echo "========== LAUNCHING PYTHON CODE =========="
# We want -u (unbuffered mode) so that output is generated as the tool runs, not only on completion.
trap cleanup 2
python -u testing_window.py