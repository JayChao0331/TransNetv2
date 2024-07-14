# TransNetv2

### Download pre-trained weights
- https://drive.google.com/file/d/1SV4wBZq-Tw67qCWdjf0IWtEC17OMnFP3/view?usp=sharing
- Store it in the directory: ./TransNetV2/inference/transnetv2-weights/variables

### Setup Environments
- conda create --name transnet python=3.7
- pip3 install -r requirements.txt

### Step 1: Download a video and store it in the folder 'raw_videos'
- Sample video type: https://www.youtube.com/watch?v=CE0AtYwyU8E

### Step 2: Extract frames from the .mp4 video file
- python3 extract_frames.py

### Step 3: Run Video Clipping Model
- cd TransNetV2/inference/
- python3 transnetv2.py --file ../../raw_videos/yourvideo.mp4 --weights ./transnetv2-weights --visualize

### Step 4: Visualize the clipping results
- python3 frames2clips.py --visualize
- visualize: Save clipping results to .gif files (may include lots of clips, terminate the process when needed)
