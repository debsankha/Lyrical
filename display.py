#!/usr/bin/env python

from commands import getoutput as get
from search import GoogleSearch
from urllib import urlopen
import user
import re
from getlyric import xmlcorrect,ascii_to_char,bylength,getlyric
import gobject
import dbus
import dbus.glib
import sys,os
import pango

try:
	import gtk
	import gtk.glade
except:
	sys.exit(1)


class Gui_display:
	global GoogleSearch
	def __init__(self):
		
		self.bus=dbus.SessionBus()
		self.gladefile="./Lyrical.glade"
		self.wTree = gtk.glade.XML(self.gladefile)
		self.wTree.get_widget("combobox1").append_text('Rhythmbox')
		self.wTree.get_widget("combobox1").append_text('Amarok 1.x')	
		try:
			self.last_used=((get("cat /var/log/Lyrical.log | grep last_playing")).split('\t')[1]).strip()
		except:
			self.last_used='Rhythmbox'

		
		dic={"on_combobox1_changed" : self.on_changed,
		     "on_mainwin_destroy" : gtk.main_quit}
		
		self.wTree.signal_autoconnect(dic)
		self.wTree.get_widget("mainwin").show()


	def find_lyric(self,title,artist,is_first=False,is_next=False,is_prev=False):
		if is_first==True:
			self.result_no=-1
			self.all_lyrics=[]
			searchstr='''"'''+title+'''"'''+' '+artist+' lyrics -search'
			gs=GoogleSearch(searchstr)
			print 'Googling for ',searchstr
			self.results=gs.get_results()
			print "the search results are: "
			for i in self.results:
				print i

		if is_prev==True:
			if self.result_no>=1:
				self.result_no-=1
				print "returning the lyric no %d"%self.result_no
				return self.all_lyrics[self.result_no]
			else:
				return "This is the first one"
		
		if is_next==True:
			if len(self.all_lyrics)>self.result_no+1:
				self.result_no+=1
				return self.all_lyrics[self.result_no]

		while self.result_no+1<len(self.results):
			self.result_no+=1
			lyric=getlyric(self.results[self.result_no].encode('utf8'))
			self.all_lyrics.append(lyric)
		
			if lyric=='':
				pass
			else :
				print "result_no is %d"%self.result_no
				return lyric
		else:
			return "this is the last lyric I could find"
	
	def set_lyric(self,text,title,artist):
		text=re.sub("(<br|BR)([^>]*?)(>)","\n",text)
		text=re.sub("(<[^>]*>)+(\n)+","\n",text)
		text=re.sub("(<[^>]*>)+",'',text)
		text=re.sub("(\n)+(\s)*",'\n',text)
		buffertext=gtk.TextBuffer()
		buffertext.set_text(text)
		boldTag=gtk.TextTag("Bold")
		boldTag.set_property('weight',pango.WEIGHT_BOLD)
		italicTag=gtk.TextTag("Italic")
		italicTag.set_property('style',pango.STYLE_ITALIC)
		table=buffertext.get_tag_table()
		table.add(boldTag)
		table.add(italicTag)
		iter = buffertext.get_iter_at_offset(0)
		buffertext.insert_with_tags_by_name(iter,title,'Bold')
		buffertext.insert_with_tags_by_name(iter,'\nby '+artist+'\n','Italic')
		self.wTree.get_widget("lyric_box").set_buffer(buffertext)

		

	def on_changed(self,*args, **kwargs):
#		self.last_used=self.wTree.get_widget("combobox1").get_active_text()
#		self.update_for_rhythmbox()
		Rhythmbox_init(self)

	
class Rhythmbox_init:
	def __init__(self,instance):
		self.inst=instance
		dic2={
				"on_Next_clicked" : self.next_show,
				"on_Prev_clicked" : self.prev_show,
				"on_mainwin_activate_default" : self.job_for_rhythmbox,
				"on_combobox1_changed" : self.inst.on_changed,
				"on_mainwin_destroy" : gtk.main_quit,
				"on_initiation" : self.on_initiation,
				}
		
		self.inst.wTree.signal_autoconnect(dic2)

		self.job_for_rhythmbox()



	def next_show(self,*args, **kwargs):
		lyric=self.inst.find_lyric(self.title,self.artist,is_next=True)
		self.inst.set_lyric(lyric,self.title,self.artist)
		self.inst.bus.add_signal_receiver(self.job_for_rhythmbox,dbus_interface="org.gnome.Rhythmbox.Player",signal_name="playingChanged")
		loop=gobject.MainLoop()
		print 'starting gobject.MainLoop()'
		loop.run()
	
	def prev_show(self,*args, **kwargs):
		print " showing prev"
		lyric=self.inst.find_lyric(self.title,self.artist,is_prev=True)
		self.inst.set_lyric(lyric,self.title,self.artist)
		self.inst.bus.add_signal_receiver(self.job_for_rhythmbox,dbus_interface="org.gnome.Rhythmbox.Player",signal_name="playingChanged")
		loop=gobject.MainLoop()
		print 'starting gobject.MainLoop()'
		loop.run()


	def on_initiation(self,*args, **kwargs):
		if self.last_used=='Rhythmbox':
			self.wTree.get_widget("combobox1").set_active(0)
	
		elif self.last_used=='Amarok 1.x':
			self.wTree.get_widget("combobox1").set_active(1) 
		
		else :
			self.last_used='Rhythmbox'
			self.wTree.get_widget("combobox1").set_active(0)

	

	def job_for_rhythmbox(self,*args, **kwargs):
		rhythm_obj=self.inst.bus.get_object("org.gnome.Rhythmbox", "/org/gnome/Rhythmbox/Player")
		rhythmshell_obj=self.inst.bus.get_object("org.gnome.Rhythmbox", "/org/gnome/Rhythmbox/Shell")
		rhythm=dbus.Interface(rhythm_obj, "org.gnome.Rhythmbox.Player")
		rhythmshell=dbus.Interface(rhythmshell_obj, "org.gnome.Rhythmbox.Shell")	
		try:
			self.artist=str(rhythmshell.getSongProperties(rhythm.getPlayingUri())['artist'])
		except:
			print 'No song is playing right now'
			return ''
		self.title=str(rhythmshell.getSongProperties(rhythm.getPlayingUri())['title'])
		lyric=self.inst.find_lyric(self.title,self.artist,is_first=True)
		self.oldlyric=lyric
		self.inst.set_lyric(lyric,self.title,self.artist)
	
	def update_for_rhythmbox(self,*args,**kwargs):
		print "showing_for_rhythmbox"
		self.job_for_rhythmbox()
		self.inst.bus.add_signal_receiver(self.job_for_rhythmbox,dbus_interface="org.gnome.Rhythmbox.Player",signal_name="playingChanged")
		loop=gobject.MainLoop()
		print 'starting gobject.MainLoop()'
		loop.run()



	

gui=Gui_display()
gtk.main()


