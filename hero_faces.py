# Faces in the hero "Built by verified investors" stack (96px JPEG, base64, one file per face in hero/).
# Order matters: Max first, Shay second — Max, Nov 8.
import os
_d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hero')
HERO = [(n, open(os.path.join(_d, n + '.b64')).read().strip()) for n in ['max', 'shay', 'f1', 'f2', 'zac', 'f3']]
