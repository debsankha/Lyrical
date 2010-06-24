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

def main(*args, **kwargs):
	rhythm_obj=bus.get_object("org.gnome.Rhythmbox", "/org/gnome/Rhythmbox/Player")
	rhythmshell_obj=bus.get_object("org.gnome.Rhythmbox", "/org/gnome/Rhythmbox/Shell")
	rhythm=dbus.Interface(rhythm_obj, "org.gnome.Rhythmbox.Player")
	rhythmshell=dbus.Interface(rhythmshell_obj, "org.gnome.Rhythmbox.Shell")	
	artist=str(rhythmshell.getSongProperties(rhythm.getPlayingUri())['artist'])
	title=str(rhythmshell.getSongProperties(rhythm.getPlayingUri())['title'])

	searchstr='''"'''+title+'''"'''+' '+artist+' lyrics -search'
	
	gs=GoogleSearch(searchstr)
	print 'Googling for ',searchstr
	gs.results_per_page=10

	results=gs.get_results()

#	try:
#		results=gs.get_results()
#	except:
#		print 'google.com is not accessible'
#		return ''

	for res in results:
		lyric=getlyric(res.url.encode('utf8'),title)
		if lyric=='':
			pass
		else :
			print 'the lyric is:\n%s'%lyric
			break

bus=dbus.SessionBus()
main()

bus.add_signal_receiver(main,dbus_interface="org.gnome.Rhythmbox.Player",signal_name="playingChanged")
loop=gobject.MainLoop()
loop.run()


