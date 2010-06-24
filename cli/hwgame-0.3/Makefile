DESTDIR=

compile:	hwevolve.c
	gcc -O3 hwevolve.c -o hwevolve

install:
	install -D -m755 hwgame ${DESTDIR}/usr/bin/hwgame
	install -D -m644 hwgame.png ${DESTDIR}/usr/share/pixmaps/hwgame.png
	install -D -m644 hwgame_large.png ${DESTDIR}/usr/share/pixmaps/hwgame_large.png
	install -D -m644 hwplot.gnu ${DESTDIR}/usr/share/hwgame/hwplot.gnu
	install -D -m755 hwevolve ${DESTDIR}/usr/bin/hwevolve
	install -D -m644 gui.glade ${DESTDIR}/usr/share/hwgame/gui.glade
	install -D -m644 hwgame.desktop ${DESTDIR}/usr/share/applications/hwgame.desktop

uninstall:
	rm ${DESTDIR}/usr/bin/hwgame
	rm ${DESTDIR}/usr/share/pixmaps/hwgame.png
	rm ${DESTDIR}/usr/share/pixmaps/hwgame_large.png
	rm -rf ${DESTDIR}/usr/share/hwgame/
	rm ${DESTDIR}/usr/bin/hwevolve
	rm ${DESTDIR}/usr/share/applications/hwgame.desktop

clean:
	rm hwevolve
