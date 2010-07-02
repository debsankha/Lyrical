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
		     "on_Next_clicked" : self.next_show,
		     "on_Prev_clicked" : self.prev_show,
		     "on_mainwin_destroy" : gtk.main_quit,
		     "on_initiation" : self.on_initiation}

		
		self.wTree.signal_autoconnect(dic)
		self.wTree.get_widget("mainwin").show()


	def find_lyric(self,title,artist,num=0):
		return """
		# Copyright 2010 Debsankha Manik
# E-mail: deb5890@gmail.com
# Website: http://debsankha-manik.appspot.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


	def set_lyric(self,text):
		text=re.sub("(<[^>]*>)+(\n)+","\n",text)
		text=re.sub("(<[^>]*>)+",'',text)
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
		buffertext.insert_with_tags_by_name(iter,self.title,'Bold')
		buffertext.insert_with_tags_by_name(iter,'by '+self.artist,'Italic')
		self.wTree.get_widget("lyric_box").set_buffer(buffertext)


	def on_changed(self,*args, **kwargs):
		self.last_used=self.wTree.get_widget("combobox1").get_active_text()
		self.result_no=0
		self.page_no=1
		self.update_for_rhythmbox()

	def next_show(self,*args, **kwargs):
		lyric=self.find_lyric(self.title,self.artist,num=self.result_no+1)
		self.set_lyric(lyric)
		self.bus.add_signal_receiver(self.job_for_rhythmbox,dbus_interface="org.gnome.Rhythmbox.Player",signal_name="playingChanged")
		loop=gobject.MainLoop()
		print 'starting gobject.MainLoop()'
		loop.run()
	
	def prev_show(self,*args, **kwargs):
		self.set_lyric(self.oldlyric)

	def on_initiation(self,*args, **kwargs):
		if self.last_used=='Rhythmbox':
			self.wTree.get_widget("combobox1").set_active(0)
	
		elif self.last_used=='Amarok 1.x':
			self.wTree.get_widget("combobox1").set_active(1) 
		
		else :
			self.last_used='Rhythmbox'
			self.wTree.get_widget("combobox1").set_active(0)

	

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
		self.oldlyric=lyric
		self.set_lyric(lyric)
	
	def update_for_rhythmbox(self,*args,**kwargs):
		print "showing_for_rhythmbox"
		self.job_for_rhythmbox()
		self.bus.add_signal_receiver(self.job_for_rhythmbox,dbus_interface="org.gnome.Rhythmbox.Player",signal_name="playingChanged")
		loop=gobject.MainLoop()
		print 'starting gobject.MainLoop()'
		loop.run()

	

gui=Gui_display()
gtk.main()


