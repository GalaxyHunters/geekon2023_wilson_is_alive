# geekon2023_wilson_is_alive
Bring Wilson from castaway to life

Repo is built for Linux and is designed to run on an RPI4.

Basic installation and first run:

```
git clone https://github.com/GalaxyHunters/geekon2023_wilson_is_alive.git
```

Download pre-requirements
```
sudo apt install libsdl2-dev
```

Build whisper and download the model, we use basic but according to the machine a bigger one might be possible.
```
cd whisper.cpp
make -j stream
./models/download-ggml-model.sh basic.en
```
