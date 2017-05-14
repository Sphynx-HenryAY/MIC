import cv2
import subprocess
from os import stat as file_stat
from math import ceil as math_ceil

__all__ = ['VideoAccess', 'turn2clips_byfilesize', 'resize_byfilesize']


class VideoAccess:
	#wrap common ffmpeg function in a dict
	op_head = {'input': '-i',
			   'frame_size': '-s',
			   'fps' : '-r',
			   'start_time' : '-ss',
			   'duration' : '-t',
			   'end_time' : '-to',
			   'stop_size' : '-fs',
			   'copy' : '-c'
			  }
	
	#set parameter order using a list
	output_order = ['input', 'frame_size', 'fps', 'start_time', 'duration', 'end_time', 'stop_size', 'copy']
	
	def __init__(self, input_name=None, input_setting=None):
		self.new_prop = dict()
		
		#setting is used for automation
		try:
			if input_name:
				self.new_prop['input'] = input_name
				self.vid_prop = self.get_video_prop(input_name)
			#input url for manual access
			elif input_setting:
				self.new_prop = input_setting
				self.vid_prop = self.get_video_prop(input_setting['input'])
		except Exception as e:
			raise Exception(e, input_name, input_setting)
			
		print(self.vid_prop)
		print(self.new_prop)
				
	def set_output_prop(self, key, value):
		self.new_prop[key] = value
		
	def set_output_time(self, start_time=0.0, end_time=None, duration=None):
		self.new_prop['start_time'] = start_time
		
		if end_time and end_time < self.vid_prop['duration']:
			self.new_prop['end_time'] = end_time
		elif duration and duration + start_time < self.vid_prop['duration']:
			self.new_prop['duration'] = duration
	
	#calculate corresponding time of given frame based on fps
	def set_output_frame(self, start_frame=0, end_frame=None, frames=None):
		fps = self.vid_prop['fps']
		frame_count = self.vid_prop['frame_count']
		
		self.new_prop['start_time'] = start_frame/fps
		
		if end_frame and end_frame < frame_count:
			self.new_prop['end_time'] = end_frame/fps
		elif frames and frames + start_frame < frame_count:
			self.new_prop['duration'] = frames/fps

	def output(self, output_url, overwrite=True):
		cmd = ['ffmpeg']
		for e in VideoAccess.output_order:
			if e in self.new_prop:
				cmd += [VideoAccess.op_head[e], str(self.new_prop[e])]
				
		if overwrite:
			cmd.append('-y')
		
		cmd.append(output_url)
		
		self.cmd_result = subprocess.run(' '.join(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		if self.cmd_result.returncode:
			raise Exception('output error with:', cmd, self.cmd_result.stderr)
			
	def clear_setting(self):
		self.vid_prop = self.new_prop = dict()
	
	@staticmethod
	def get_video_prop(vid_url):
		vid = cv2.VideoCapture(vid_url)
		
		vid_prop = dict()
		vid_prop['width'] = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
		vid_prop['height'] = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
		vid_prop['frame_size'] = '%sx%s'%(vid_prop['width'], vid_prop['height'])
		vid_prop['fps'] = vid.get(cv2.CAP_PROP_FPS)
		vid_prop['frame_count'] = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
		vid_prop['duration'] = vid_prop['frame_count']/vid_prop['fps']
		vid_prop['file_size'] = file_stat(vid_url).st_size
		
		vid.release()
		
		return vid_prop
	
	#code finished but not added yet
	@staticmethod
	def frame_chooser(vid_url):
	    pass

#keep bitrate unchange to keep file size in scale
def resize_byfilesize(input_name, target_filesize=20*1024*1024):
	if not isinstance(input_name, str):
		raise TypeError('input file_name as vid_input')
		
	vid_prop = VideoAccess.get_video_prop(input_name)
	vid_size = vid_prop['file_size']
	
	if vid_size < target_filesize:
		return False
	
	#takes first two decimal point number as ratio
	scale = (int((target_filesize/vid_size) * 100) / 100) ** 0.5
	
	target_frame_width = int(vid_prop['width']*scale)
	target_frame_height = int(vid_prop['height']*scale)
	target_frame_size = '%dx%d'%(target_frame_width, target_frame_height)
	
	input_setting = dict()
	input_setting['input'] = input_name
	input_setting['frame_size'] = target_frame_size
	
	output_url = input_name.replace('.mp4', '.resize.mp4')
	
	vid = VideoAccess(input_setting=input_setting)
	
	try: 
		vid.output(output_url)
	except Exception as e: 
		print('ERROR occurs when', output_url, e.args)


#sample input_setting:
#input_setting = {'input':r'C:/Users/HAY/Desktop/GettingStarted/replay-full_20170507_01_chi_700kbps.mp4', 'stop_size':'20M', 'copy':'copy'}
def turn2clips_byfilesize(vid_setting):
	vid = VideoAccess(input_setting=vid_setting)
	output_pattern = vid_setting['input'].replace('.mp4', '.%02d.mp4')
	
	sample_url = output_pattern%0
	vid.output(sample_url)
	
	vid_prop = vid.vid_prop
	sample_prop = VideoAccess.get_video_prop(sample_url)
	
	# 20<<20 = 20 * 1024**2, file size limit of wechat
	if int(sample_prop['file_size']) > 20<<20:
		raise Exception('please change target file size and try again later')
	
	start_frame = 0
	total_frame = vid_prop['frame_count']
	frames = sample_prop['frame_count']
	number_of_clips = math_ceil(total_frame / frames)
	clips_produced = [output_pattern%0]
	
	if number_of_clips < 2:
		return
	
	for i in range(1, number_of_clips):
		start_frame += frames
		if start_frame > total_frame:
			start_frame -= frames
			frames = total_frame - start_frame
			
		print('total_frame %d, start_frame %d, frames %d'%(total_frame, start_frame, frames))
		
		vid.set_output_frame(start_frame=start_frame, frames=frames)
		
		try: 
			vid.output(output_pattern%i)
			clips_produced.append(output_pattern%i)
		except: 
			print('ERROR occurs when', i)
