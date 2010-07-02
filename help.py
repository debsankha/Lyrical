# Text Widget
#
# The GtkTextView widget displays a GtkTextBuffer. One GtkTextBuffer
# can be displayed by multiple GtkTextViews. This demo has two views
# displaying a single buffer, and shows off the widget's text
# formatting features.
# Ported to python-gtk-2 by Nathan J. Hurst
# still unported: stipple support, parse color code in easter egg

import pygtk
pygtk.require('2.0')
import gtk,gobject,pango

# stipple code unimplemented so far.
#gray50_width = 2
#gray50_height = 2
#gray50_bits = [0x02, 0x01]

PANGO_SCALE=1024 # Where is this defined?

def insert_one_tag_into_buffer(buffer, name, *params):
    tag = gtk.TextTag(name)
    while(params):
        tag.set_property(params[0], params[1])
        params = params[2:]
    table = buffer.get_tag_table()
    table.add(tag)

def create_tags (buffer):
  # Create a bunch of tags. Note that it's also possible to
  # create tags with gtk_text_tag_new() then add them to the
  # tag table for the buffer, gtk_text_buffer_create_tag() is
  # just a convenience function. Also note that you don't have
  # to give tags a name; pass None for the name to create an
  # anonymous tag.
  #
  # In any real app, another useful optimization would be to create
  # a GtkTextTagTable in advance, and reuse the same tag table for
  # all the buffers with the same tag set, instead of creating
  # new copies of the same tags for every buffer.
  #
  # Tags are assigned default priorities in order of addition to the
  # tag table.	 That is, tags created later that affect the same text
  # property affected by an earlier tag will override the earlier
  # tag.  You can modify tag priorities with
  # gtk_text_tag_set_priority().
  
  insert_one_tag_into_buffer(buffer, "heading", "weight", pango.WEIGHT_BOLD,
                     "size", 15 * PANGO_SCALE)
  
  insert_one_tag_into_buffer(buffer, "italic", "style", pango.STYLE_ITALIC)

  insert_one_tag_into_buffer(buffer, "bold", "weight", pango.WEIGHT_BOLD)  
  
  insert_one_tag_into_buffer(buffer, "big", "size", 20 * PANGO_SCALE)
  # points times the PANGO_SCALE factor
  
  insert_one_tag_into_buffer(buffer, "xx-small", "scale", pango.SCALE_XX_SMALL)

  insert_one_tag_into_buffer(buffer, "x-large", "scale", pango.SCALE_X_LARGE)
  
  insert_one_tag_into_buffer(buffer, "monospace", "family", "monospace")
  
  insert_one_tag_into_buffer(buffer, "blue_foreground", "foreground", "blue")  

  insert_one_tag_into_buffer(buffer, "red_background", "background", "red")

  #stipple = gtk.gdk.Pixmap(None,
  #                         gray50_bits, gray50_width,
  #                         gray50_height)
  
  #insert_one_tag_into_buffer(buffer, "background_stipple", "background_stipple", stipple)

  #insert_one_tag_into_buffer(buffer, "foreground_stipple", "foreground_stipple", stipple)

  #stipple = None

  insert_one_tag_into_buffer(buffer, "big_gap_before_line", "pixels_above_lines", 30)

  insert_one_tag_into_buffer(buffer, "big_gap_after_line", "pixels_below_lines", 30)

  insert_one_tag_into_buffer(buffer, "double_spaced_line", "pixels_inside_wrap", 10)

  insert_one_tag_into_buffer(buffer, "not_editable", "editable", gtk.FALSE)
  
  insert_one_tag_into_buffer(buffer, "word_wrap", "wrap_mode", gtk.WRAP_WORD)

  insert_one_tag_into_buffer(buffer, "char_wrap", "wrap_mode", gtk.WRAP_CHAR)

  insert_one_tag_into_buffer(buffer, "no_wrap", "wrap_mode", gtk.WRAP_NONE)
  
  insert_one_tag_into_buffer(buffer, "center", "justification", gtk.JUSTIFY_CENTER)

  insert_one_tag_into_buffer(buffer, "right_justify", "justification", gtk.JUSTIFY_RIGHT)

  insert_one_tag_into_buffer(buffer, "wide_margins", "left_margin", 50, "right_margin", 50)
  
  insert_one_tag_into_buffer(buffer, "strikethrough", "strikethrough", gtk.TRUE)
  
  insert_one_tag_into_buffer(buffer, "underline", "underline", pango.UNDERLINE_SINGLE)

  insert_one_tag_into_buffer(buffer, "double_underline", "underline", pango.UNDERLINE_DOUBLE)

  insert_one_tag_into_buffer(buffer, "superscript", "rise", 10 * PANGO_SCALE, 
			      "size", 8 * PANGO_SCALE)
  
  insert_one_tag_into_buffer(buffer, "subscript", "rise", -10 * PANGO_SCALE,
			      "size", 8 * PANGO_SCALE)

  insert_one_tag_into_buffer(buffer, "rtl_quote",
                             "wrap_mode", gtk.WRAP_WORD,
                             "direction", gtk.TEXT_DIR_RTL,
                             "indent", 30,
                             "left_margin", 20,
                             "right_margin", 20)

def insert_text (buffer):
    # demo_find_file() looks in the the current directory first,
    # so you can run gtk-demo without installing GTK, then looks
    # in the location where the file is installed.
    
    #filename = demo_find_file ("gtk-logo-rgb.gif", None)
    #if (filename):
    #    pixbuf = gdk_pixbuf_new_from_file (filename, None)
    #   
    #if (pixbuf == None):
    #    g_printerr ("Failed to load image file gtk-logo-rgb.gif\n")
    #    exit (1)
    
    #scaled = gdk_pixbuf_scale_simple (pixbuf, 32, 32, GDK_INTERP_BILINEAR)
    #pixbuf = scaled
    
    # get start of buffer each insertion will revalidate the
    # iterator to point to just after the inserted text.
    
    iter = buffer.get_iter_at_offset (0)
    
    buffer.insert (iter, "The text widget can display text with all kinds of nifty attributes. It also supports multiple views of the same buffer this demo is showing the same buffer in two places.\n\n")
    
    buffer.insert_with_tags_by_name (iter, "Font styles. ", "heading")
    
    buffer.insert (iter, "For example, you can have ")
    buffer.insert_with_tags_by_name (iter,
                                     "italic",
                                     "italic")
    buffer.insert (iter, ", ")  
    buffer.insert_with_tags_by_name (iter,
                                     "bold",
                                     "bold")
    buffer.insert (iter, ", or ")
    buffer.insert_with_tags_by_name (iter,
                                     "monospace (typewriter)",
                                     "monospace")
    buffer.insert (iter, ", or ")
    buffer.insert_with_tags_by_name (iter,
                                     "big",
                                     "big")
    buffer.insert (iter, " text. ")
    buffer.insert (iter, "It's best not to hardcode specific text sizes you can use relative sizes as with CSS, such as ")
    buffer.insert_with_tags_by_name (iter,
                                     "xx-small",
                                     "xx-small")
    buffer.insert (iter, " or ")
    buffer.insert_with_tags_by_name (iter,
                                     "x-large",
                                     "x-large")
    buffer.insert (iter, " to ensure that your program properly adapts if the user changes the default font size.\n\n")
    
    buffer.insert_with_tags_by_name (iter, "Colors. ",
                                     "heading")
    
    buffer.insert (iter, "Colors such as ")  
    buffer.insert_with_tags_by_name (iter,
                                     "a blue foreground",
                                     "blue_foreground")
    buffer.insert (iter, " or ")  
    buffer.insert_with_tags_by_name (iter,
                                     "a red background",
                                     "red_background")
    #buffer.insert (iter, " or even ")  
    #buffer.insert_with_tags_by_name (iter,
    #                                 "a stippled red background",
    #                                 "red_background",
    #                                 "background_stipple")
    
    #buffer.insert (iter, " or ")  
    #buffer.insert_with_tags_by_name (iter,
    #                                 "a stippled blue foreground on solid red background",
    #                                 "blue_foreground",
    #                                 "red_background",
    #                                 "foreground_stipple")
    #buffer.insert (iter, " (select that to read it) can be used.\n\n")  
    
    buffer.insert_with_tags_by_name (iter, "Underline, strikethrough, and rise. ",
                                     "heading")
    
    buffer.insert_with_tags_by_name (iter,
                                     "Strikethrough",
                                     "strikethrough")
    buffer.insert (iter, ", ")
    buffer.insert_with_tags_by_name (iter,
                                     "underline",
                                     "underline")
    buffer.insert (iter, ", ")
    buffer.insert_with_tags_by_name (iter,
                                     "double underline", 
                                     "double_underline")
    buffer.insert (iter, ", ")
    buffer.insert_with_tags_by_name (iter,
                                     "superscript",
                                     "superscript")
    buffer.insert (iter, ", and ")
    buffer.insert_with_tags_by_name (iter,
                                     "subscript",
                                     "subscript")
    buffer.insert (iter, " are all supported.\n\n")
    
    buffer.insert_with_tags_by_name (iter, "Images. ",
                                     "heading")
    
    buffer.insert (iter, "The buffer can have images in it: ")
    #buffer.insert_pixbuf (iter, pixbuf)
    #buffer.insert_pixbuf (iter, pixbuf)
    #buffer.insert_pixbuf (iter, pixbuf)
    buffer.insert (iter, " for example.\n\n")
    
    buffer.insert_with_tags_by_name (iter, "Spacing. ",
                                     "heading")
    
    buffer.insert (iter, "You can adjust the amount of space before each line.\n")
    
    buffer.insert_with_tags_by_name (iter,
                                     "This line has a whole lot of space before it.\n",
                                     "big_gap_before_line", "wide_margins")
    buffer.insert_with_tags_by_name (iter,
                                     "You can also adjust the amount of space after each line this line has a whole lot of space after it.\n",
                                     "big_gap_after_line", "wide_margins")
    
    buffer.insert_with_tags_by_name (iter,
                                     "You can also adjust the amount of space between wrapped lines; this line has extra space between each wrapped line in the same paragraph. To show off wrapping, some filler text: the quick brown fox jumped over the lazy dog. Blah blah blah blah blah blah blah blah blah.\n",
                                     "double_spaced_line", "wide_margins")
    
    buffer.insert (iter, "Also note that those lines have extra-wide margins.\n\n")
    
    buffer.insert_with_tags_by_name (iter, "Editability. ",
                                     "heading")
    
    buffer.insert_with_tags_by_name (iter,
                                     "This line is 'locked down' and can't be edited by the user - just try it! You can't delete this line.\n\n",
                                     "not_editable")
    
    buffer.insert_with_tags_by_name (iter, "Wrapping. ",
                                     "heading")
    
    buffer.insert (iter,
                   "This line (and most of the others in this buffer) is word-wrapped, using the proper Unicode algorithm. Word wrap should work in all scripts and languages that GTK+ supports. Let's make this a long paragraph to demonstrate: blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah\n\n")  
    
    buffer.insert_with_tags_by_name (iter,
                                     "This line has character-based wrapping, and can wrap between any two character glyphs. Let's make this a long paragraph to demonstrate: blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah\n\n",
                                     "char_wrap")
    
    buffer.insert_with_tags_by_name (iter,
                                     "This line has all wrapping turned off, so it makes the horizontal scrollbar appear.\n\n\n",
                                     "no_wrap")
    
    buffer.insert_with_tags_by_name (iter, "Justification. ",
                                     "heading")  
    
    buffer.insert_with_tags_by_name (iter,
                                     "\nThis line has center justification.\n",
                                     "center")
    
    buffer.insert_with_tags_by_name (iter,
                                     "This line has right justification.\n",
                                     "right_justify")
    
    buffer.insert_with_tags_by_name (iter,
                                     "\nThis line has big wide margins. Text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text.\n",
                                     "wide_margins")  
    
    buffer.insert_with_tags_by_name (iter, "Internationalization. ",
                                     "heading")
    
    buffer.insert (iter,
                   "You can put all sorts of Unicode text in the buffer.\n\nGerman (Deutsch S\303\274d) Gr\303\274\303\237 Gott\nGreek (\316\225\316\273\316\273\316\267\316\275\316\271\316\272\316\254) \316\223\316\265\316\271\316\254 \317\203\316\261\317\202\nHebrew	\327\251\327\234\327\225\327\235\nJapanese (\346\227\245\346\234\254\350\252\236)\n\nThe widget properly handles bidirectional text, word wrapping, DOS/UNIX/Unicode paragraph separators, grapheme boundaries, and so on using the Pango internationalization framework.\n")  
    
    buffer.insert (iter, "Here's a word-wrapped quote in a right-to-left language:\n")
    buffer.insert_with_tags_by_name (iter, "\331\210\331\202\330\257 \330\250\330\257\330\243 \330\253\331\204\330\247\330\253 \331\205\331\206 \330\243\331\203\330\253\330\261 \330\247\331\204\331\205\330\244\330\263\330\263\330\247\330\252 \330\252\331\202\330\257\331\205\330\247 \331\201\331\212 \330\264\330\250\331\203\330\251 \330\247\331\203\330\263\331\212\331\210\331\206 \330\250\330\261\330\247\331\205\330\254\331\207\330\247 \331\203\331\205\331\206\330\270\331\205\330\247\330\252 \331\204\330\247 \330\252\330\263\330\271\331\211 \331\204\331\204\330\261\330\250\330\255\330\214 \330\253\331\205 \330\252\330\255\331\210\331\204\330\252 \331\201\331\212 \330\247\331\204\330\263\331\206\331\210\330\247\330\252 \330\247\331\204\330\256\331\205\330\263 \330\247\331\204\331\205\330\247\330\266\331\212\330\251 \330\245\331\204\331\211 \331\205\330\244\330\263\330\263\330\247\330\252 \331\205\330\247\331\204\331\212\330\251 \331\205\331\206\330\270\331\205\330\251\330\214 \331\210\330\250\330\247\330\252\330\252 \330\254\330\262\330\241\330\247 \331\205\331\206 \330\247\331\204\331\206\330\270\330\247\331\205 \330\247\331\204\331\205\330\247\331\204\331\212 \331\201\331\212 \330\250\331\204\330\257\330\247\331\206\331\207\330\247\330\214 \331\210\331\204\331\203\331\206\331\207\330\247 \330\252\330\252\330\256\330\265\330\265 \331\201\331\212 \330\256\330\257\331\205\330\251 \331\202\330\267\330\247\330\271 \330\247\331\204\331\205\330\264\330\261\331\210\330\271\330\247\330\252 \330\247\331\204\330\265\330\272\331\212\330\261\330\251. \331\210\330\243\330\255\330\257 \330\243\331\203\330\253\330\261 \331\207\330\260\331\207 \330\247\331\204\331\205\330\244\330\263\330\263\330\247\330\252 \331\206\330\254\330\247\330\255\330\247 \331\207\331\210 \302\273\330\250\330\247\331\206\331\203\331\210\330\263\331\210\331\204\302\253 \331\201\331\212 \330\250\331\210\331\204\331\212\331\201\331\212\330\247.\n\n",
                                     "rtl_quote")
    
    buffer.insert (iter, "You can put widgets in the buffer: Here's a button: ")
    anchor = buffer.create_child_anchor (iter)
    buffer.insert (iter, " and a menu: ")
    anchor = buffer.create_child_anchor (iter)
    buffer.insert (iter, " and a scale: ")
    anchor = buffer.create_child_anchor (iter)
    buffer.insert (iter, " and an animation: ")
    anchor = buffer.create_child_anchor (iter)
    buffer.insert (iter, " finally a text entry: ")
    anchor = buffer.create_child_anchor (iter)
    buffer.insert (iter, ".\n")
    
    buffer.insert (iter, "\n\nThis demo doesn't demonstrate all the GtkTextBuffer features; it leaves out, for example: invisible/hidden text (doesn't work in GTK 2, but planned), tab stops, application-drawn areas on the sides of the widget for displaying breakpoints and such...")
    
    # Apply word_wrap tag to whole buffer#/
    (start, end) = buffer.get_bounds ()
    buffer.apply_tag_by_name ("word_wrap", start, end)
    
    
def find_anchor (iter):
    while iter.forward_char ():
        if (iter.get_child_anchor ()):
            return gtk.TRUE
    return gtk.FALSE

def attach_widgets (text_view):
    buffer = text_view.get_buffer()
    
    iter = buffer.get_start_iter ()
    i = 0
    while (find_anchor (iter)):
        anchor = iter.get_child_anchor ()
        
        if (i == 0):
            widget = gtk.Button("Click Me")
            
            widget.connect("clicked", easter_egg_callback)
        elif (i == 1):
            menu = gtk.Menu()
            
            widget = gtk.OptionMenu()
            
            menu_item = gtk.MenuItem("Option 1")
            menu.append (menu_item)
            menu_item = gtk.MenuItem("Option 2")
            menu.append(menu_item)
            menu_item = gtk.MenuItem("Option 3")
            menu.append (menu_item)
            
            widget.set_menu (menu)
        elif (i == 2):
            widget = gtk.HScale (None)
            widget.set_range (0, 100)
            widget.set_size_request (70, -1)
        elif (i == 3):
            filename = "floppybuddy.gif"
            widget = gtk.Image()
            widget.set_from_file(filename)
        elif (i == 4):
            widget = gtk.Entry ()
            
        text_view.add_child_at_anchor (widget, anchor)
        
        widget.show_all ()
        
        i = i + 1 
    


window = None
def do_textview ():
    global window
    if (not window):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_default_size (450, 450)
        
        window.connect("destroy", gtk.mainquit)
        
        window.set_title("TextView")
        window.set_border_width(0)
        
        vpaned = gtk.VPaned()
        vpaned.set_border_width (5)
        #vpaned.add (vpaned)
        
        # For convenience, we just use the autocreated buffer from
        # the first text view you could also create the buffer
        # by itself with gtk_text_buffer_new(), then later create
        # a view widget.
        
        view1 = gtk.TextView()
        buffer = view1.get_buffer ()
        view2 = gtk.TextView()
        view2.set_buffer(buffer)
        
        sw = gtk.ScrolledWindow(None, None)
        sw.set_policy (gtk.POLICY_AUTOMATIC,
                       gtk.POLICY_AUTOMATIC)
        vpaned.add1(sw)
        
        sw.add (view1)
        
        sw = gtk.ScrolledWindow()
        sw.set_policy (gtk.POLICY_AUTOMATIC,
                       gtk.POLICY_AUTOMATIC)
        vpaned.add2(sw)
        
        sw.add (view2)
        
        create_tags (buffer)
        insert_text (buffer)
        
        attach_widgets (view1)
        attach_widgets (view2)
        window.add(vpaned)
        window.show_all()
        
    return window


def recursive_attach_view (depth, view, anchor):
    if (depth > 4):
        return
    
    child_view = gtk.TextView()
    child_view.set_buffer(view.get_buffer())
    
    # Event box is to add a black border around each child view */
    event_box = gtk.EventBox()
    #gtk.gdk_color_parse ("black", color)
    #event_box.modify_bg (gtk.STATE_NORMAL, color)
    
    align = gtk.Alignment(0.5, 0.5, 1.0, 1.0)
    align.set_border_width (1)
    
    event_box.add (align)
    align.add (child_view)
    
    view.add_child_at_anchor (event_box, anchor)
    
    recursive_attach_view (depth + 1, (child_view), anchor)

eewindow = None
def easter_egg_callback (button):
    global eewindow
    if (eewindow):
        eewindow.present ()
        return
    
    buffer = gtk.TextBuffer()
    
    iter = buffer.get_start_iter ()
    
    buffer.insert (iter, "This buffer is shared by a set of nested text views.\n Nested view:\n")
    anchor = buffer.create_child_anchor (iter)
    buffer.insert (iter, "\nDon't do this in real applications, please.\n")
    
    view = gtk.TextView()
    view.set_buffer(buffer)
    
    recursive_attach_view (0, view, anchor)
    
    eewindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
    sw = gtk.ScrolledWindow(None, None)
    sw.set_policy (gtk.POLICY_AUTOMATIC,
                   gtk.POLICY_AUTOMATIC)
    
    eewindow.add(sw)
    sw.add(view)
    
    #eewindow.add_weak_pointer (eewindow) # what does this do?
    
    eewindow.set_default_size (300, 400)
    
    eewindow.show_all()

do_textview()
gtk.mainloop()

