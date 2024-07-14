import os
import csv
import imageio

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--visualize', action="store_true")
args = parser.parse_args()


# Frame path
video_frames_dir = './raw_videos/videoplayback-opencv'
video_clipping_result = './raw_videos/videoplayback.mp4.scenes.txt'

# Saving path
save_clip_dir = '/work/u5351147/Video2Clip/clip_videos'
save_dataset_dir = './raw_videos'
save_visualize_dir = './raw_videos/visualize'


def read_files(frames_pth, clipping_pth):
    # frame list
    frame_names = os.listdir(frames_pth)
    frame_names.sort()

    # clipping result file
    clipping_result = []
    with open(clipping_pth, 'r') as csv_in:
        csv_reader = csv.reader(csv_in, delimiter=' ')
        for line in csv_reader:
            clipping_result.append([int(line[0]), int(line[1])])
    
    frame_names = [os.path.join(frames_pth, frame_name) for frame_name in frame_names]
    
    return frame_names, clipping_result


# demo gif
def frames_to_video(frame_names, clipping_result, video_frames_dir, save_clip_dir):
    kargs = {'duration': 0.025}
    for clip_id, line in enumerate(clipping_result):
        start_id, end_id = line
        clip_lst = frame_names[start_id:end_id+1]
        clip_name = 'clip_{}.gif'.format(clip_id)
        frames = []
        for frame_name in clip_lst:
            file_path = os.path.join(video_frames_dir, frame_name)
            frames.append(imageio.imread(file_path))
        
        # Make it pause at the end so that the viewers can ponder
        for _ in range(10):
            frames.append(imageio.imread(file_path))
        
        imageio.mimsave(os.path.join(save_clip_dir, clip_name), frames, **kargs)


# Frames to clips
def frames_to_clips(frame_names, clipping_result):
    clip_set = []
    for line in clipping_result:
        start_id, end_id = line
        clip_lst = frame_names[start_id:end_id+1]
        clip_set.append(clip_lst)
    
    return clip_set


# Set hyper-parameters & prepare dataset
def create_dataset(clip_set, clip_length, step=5):
    dataset = []
    for clip_lst in clip_set:
        clip_len = len(clip_lst)

        # Rules to prepare the dataset
        if clip_len < clip_length:
            continue
        
        pointer = 0
        while (pointer + clip_length) <= clip_len:
            subclip_lst = clip_lst[pointer:pointer+clip_length]
            dataset.append(subclip_lst)
            pointer += step
    
    return dataset


def save_dataset(dataset, filename):
    with open(filename, 'w') as csv_out:
        csv_writer = csv.writer(csv_out, delimiter=',')
        for clip_lst in dataset:
            csv_writer.writerow(clip_lst)


def visualize_clip(dataset, save_visualize_dir):
    os.makedirs(save_visualize_dir, exist_ok=True)

    kargs = {'duration': 0.1}
    for clip_id, fnames in enumerate(dataset):
        clip_name = 'clip_{}.gif'.format(clip_id)
        frames = []
        for fname in fnames:
            frames.append(imageio.imread(fname))
        
        # Make it pause at the end so that the viewers can ponder
        for _ in range(10):
            frames.append(imageio.imread(fname))
        
        imageio.mimsave(os.path.join(save_visualize_dir, clip_name), frames, **kargs)




if __name__ == '__main__':
    # Read frame names & clipping results
    frame_names, clipping_result = read_files(video_frames_dir, video_clipping_result)

    # Convert frames to clips
    clip_set = frames_to_clips(frame_names, clipping_result)

    # Prepare dataset
    clip_set = create_dataset(clip_set, clip_length=32, step=5)

    # Save dataset
    save_dataset(clip_set, '{}/{}'.format(save_dataset_dir, 'clip.csv'))

    # visualize clips
    if args.visualize:
        visualize_clip(clip_set, save_visualize_dir)
