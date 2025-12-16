# Very easy terrain generation with Perlin noise!

Clone the repo:
```bash
git clone git@github.com:sofyak0zyreva/terrain-generation.git
```
If you don't have virtual environment running: 
```bash
python -m venv venv
source venv/bin/activate
```

Run the following command to install the dependencies:
```bash
pip install pillow perlin-noise
```
To save noise map to an image:
```bash
python noise_drawer.py
```
To save terrain map to an image:
```bash
python world_drawer.py
```
You can change seed in the files themselves, or resolution in `config`
