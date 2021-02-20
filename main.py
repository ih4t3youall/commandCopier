import urwid
import pyperclip

#vars
headers = []
bracketOpen = False
commands = []
comDict = {}
header = ""
previousLine = ""

file1 = open('notes.txt', 'r')
lines = file1.readlines()
for line in lines:
    line = line.strip()
    if len(line) == 0:
        continue
    if not bracketOpen:
        result = line.find('{')

        if result == 0:
            header = previousLine

        if result != -1:
            bracketOpen = True
            if header != previousLine:
                header = line[0:result]
            headers.append(header)
    else:
        result = line.find('}')
        if result == -1:
            commands.append(line)
        else:
            bracketOpen = False
            comDict[header]=commands
            commands = []

    previousLine = line.strip()

def print_dictionary():
    for k,v in comDict.items(): 
        print('clave', k)
        for val in v:
            print('--->',val)


class ActionButton(urwid.Button):
    def __init__(self, caption, callback, selected):
        super(ActionButton, self).__init__("")
        self.selection = selected
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(caption, 1),
                                None, focus_map='reversed')

    def get_selection(self):
        return self.selection

def exit_program(button):
    raise urwid.ExitMainLoop()

class Main(urwid.WidgetWrap):
    def __init__(self):
        super(Main, self)
        self.heading = urwid.Text([u"\nLocation: ", 'Main', "\n"])
        self.interactions = []

    def get_interactions(self):
        self.interactions = []

        for header, values in comDict.items():
            self.interactions.append(urwid.Text(header))
            for value in values:
                self.interactions.append(ActionButton("-->"+value, self.copy_to_clipboard,value))

        self.interactions.append(ActionButton('Exit', exit_program,''))
        return self.interactions

    def copy_to_clipboard(self, button):
        toClipboard = button.get_selection()
        pyperclip.copy(toClipboard)

class Start(object):
    def __init__(self):
        self.log = urwid.SimpleFocusListWalker([], wrap_around=False)
        self.top = urwid.ListBox(self.log)
        self.update_place(Main())

    def update_place(self, place):
        self.log.clear()
        self.log.append(urwid.Pile([place.heading]))
        if place.get_interactions():
            for i in place.get_interactions():
                self.log.append(i)
        #setea el menu seleccionado
        self.top.focus_position = 1




game = Start()
urwid.MainLoop(game.top, palette=[('reversed', 'standout', '')]).run()
