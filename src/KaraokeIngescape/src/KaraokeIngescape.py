#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  KaraokeIngescape.py
#  KaraokeIngescape
#  Created by Ingenuity i/o on 2024/11/15
#
# <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
# <html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">
# p, li { white-space: pre-wrap; }
# hr { height: 1px; border-width: 0; }
# li.unchecked::marker { content: "\2610"; }
# li.checked::marker { content: "\2612"; }
# </style></head><body style=" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;">
# <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:13px; color:#2a2a2a;">WhiteBoard interface setter, Interface for selection  and linking hub</span></p></body></html>
#
import ingescape as igs
from  graphicalKaraoke import *
from whiteBordUtils import *

elementID_list={}
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class KaraokeIngescape(metaclass=Singleton):
    def __init__(self):
        # outputs
        self._backgroungColorO = None
        self._titleO = None
        self._hideLabelsO = None

        self.graphical_interface = None

        # atributes
        current_file = os.path.abspath(__file__)
        dir = current_file.replace(os.path.basename(current_file), "")
        root_dir = os.path.join(dir, "../../../")
        os.chdir(root_dir)
        print(root_dir, os.getcwd())


    # outputs
    @property
    def backgroungColorO(self):
        return self._backgroungColorO

    @backgroungColorO.setter
    def backgroungColorO(self, value):
        self._backgroungColorO = value
        if self._backgroungColorO is not None:
            igs.output_set_string("backgroungColor", self._backgroungColorO)
    @property
    def titleO(self):
        return self._titleO

    @titleO.setter
    def titleO(self, value):
        self._titleO = value
        if self._titleO is not None:
            igs.output_set_string("title", self._titleO)
    @property
    def hideLabelsO(self):
        return self._hideLabelsO

    @hideLabelsO.setter
    def hideLabelsO(self, value):
        self._hideLabelsO = value
        if self._hideLabelsO is not None:
            igs.output_set_bool("hideLabels", self._hideLabelsO)
    def set_clearO(self):
        igs.output_set_impulsion("clear")


    # services
    def elementCreated(self, sender_agent_name, sender_agent_uuid, token, elementId):
        if token not in elementID_list:
            elementID_list[token] = []
        elementID_list[token].append(elementId)
        print (elementID_list)

    def launchInterface(self, tretor):

        init_whiteboard_interface()

        self.graphical_interface = Application(tretor)
        self.graphical_interface.mainloop()


