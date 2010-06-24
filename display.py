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

try:
	import pygtk
	pygtk.require("2.0")
except:
	pass

try:
	import gtk
	import gtk.glade
except:
	sys.exit(1)

class Gui_display:
	global GoogleSearch
	def __init__(self):
		
		self.bus=dbus.SessionBus()
		print 'bus created\t',repr(self.bus)
		self.gladefile="/home/nofrills/Lyrical/gui2.glade"
		self.wTree = gtk.glade.XML(self.gladefile)
		self.wTree.get_widget("combobox1").append_text('Rhythmbox')
		self.wTree.get_widget("combobox1").append_text('Amarok 1.x')
		
		try:
			last_used=((get("cat /var/log/Lyrical.log | grep last_playing")).split('\t')[1]).strip()
		except:
			last_used=''

		dic={"on_combobox1_changed" : self.on_changed,
		     "on_Next_clicked" : self.next_show,
		     "on_Prev_clicked" : self.prev_show,
		     "on_mainwin_destroy" : gtk.main_quit,
		     "on_initiation" : self.on_initiation}

		
		self.wTree.signal_autoconnect(dic)
		self.wTree.get_widget("mainwin").show()


	def find_lyric(self,title,artist,num=0):
		searchstr='''"'''+title+'''"'''+' '+artist+' lyrics -search'
		gs=GoogleSearch(searchstr)
		print 'Googling for ',searchstr
	
		self.result_no=num
		self.page_no=1
		gs.results_per_page=10
	
		while 1==1:
			if self.result_no==0:
				try:
					self.results[2]
				except :
					gs.page=self.page_no
					self.results=gs.get_results()

			elif self.result_no>=gs.results_per_page:
				self.page_no+=1
				self.result_no-=gs.results_per_page
				gs.page=self.page_no
				self.results=gs.get_results()
			else :
				pass

			lyric=getlyric(self.results[self.result_no].url.encode('utf8'))
			
			if lyric=='':
				self.result_no+=1
			else :
				self.result_no+=1
				print 'the lyric is:\n%s'%lyric
				break
			
		return lyric


	def on_changed(self,*args, **kwargs):
		self.last_used=self.wTree.get_widget("combobox1").get_active_text()
		self.result_no=0
		self.page_no=1
		self.update_for_rhythmbox()

	def next_show(self,*args, **kwargs):
		lyric=self.find_lyric(self.title,self.artist,num=self.result_no+1)
		text=gtk.TextBuffer()
		text.set_text(lyric)
		self.wTree.get_widget("lyric_box").set_buffer(text)
		self.bus.add_signal_receiver(self.job_for_rhythmbox,dbus_interface="org.gnome.Rhythmbox.Player",signal_name="playingChanged")
		loop=gobject.MainLoop()
		print 'starting gobject.MainLoop()'
		loop.run()
	
	def prev_show(self,*args, **kwargs):
		text=gtk.TextBuffer()
		text.set_text(self.oldlyric)
		self.wTree.get_widget("lyric_box").set_buffer(text)


	def on_initiation(self,*args, **kwargs):
		if self.last_used=='Rhythmbox':
			self.wTree.get_widget("combobox1").set_active(0)
			self.update_for_rhythmbox()
	
		elif self.last_used=='Amarok 1.x':
			self.wTree.get_widget("combobox1").set_active(1) 
		
		else :
			self.last_used='Rhythmbox'
			self.wTree.get_widget("combobox1").set_active(0)
			self.update_for_rhythmbox()

	

	def job_for_rhythmbox(self,*args, **kwargs):
		rhythm_obj=self.bus.get_object("org.gnome.Rhythmbox", "/org/gnome/Rhythmbox/Player")
		rhythmshell_obj=self.bus.get_object("org.gnome.Rhythmbox", "/org/gnome/Rhythmbox/Shell")
		rhythm=dbus.Interface(rhythm_obj, "org.gnome.Rhythmbox.Player")
		rhythmshell=dbus.Interface(rhythmshell_obj, "org.gnome.Rhythmbox.Shell")	
		try:
			self.artist=str(rhythmshell.getSongProperties(rhythm.getPlayingUri())['artist'])
		except:
			print 'No song is playing right now'
			return ''
		self.title=str(rhythmshell.getSongProperties(rhythm.getPlayingUri())['title'])
		lyric=self.find_lyric(self.title,self.artist)
		print lyric
		self.oldlyric=lyric
		text=gtk.TextBuffer()
		text.set_text(lyric)
		self.wTree.get_widget("lyric_box").set_buffer(text)

	def update_for_rhythmbox(self,*args,**kwargs):
		print "showing_for_rhythmbox"
		self.job_for_rhythmbox()
		self.bus.add_signal_receiver(self.job_for_rhythmbox,dbus_interface="org.gnome.Rhythmbox.Player",signal_name="playingChanged")
		loop=gobject.MainLoop()
		print 'starting gobject.MainLoop()'
		loop.run()

	

gui=Gui_display()
gtk.main()


