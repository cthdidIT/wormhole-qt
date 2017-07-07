#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this example, we position two push
buttons in the bottom-right corner
of the window.

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""

import sys
from threading import Thread
from PyQt5.QtWidgets import (QWidget, QFrame, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QApplication, QFileDialog)
from wormhole import (create, util)
from twisted.internet import reactor

from wormhole.transit import (TransitSender, TransitReceiver)

from wormhole.cli.public_relay import RENDEZVOUS_RELAY

class RespondError(Exception):
    def __init__(self, response):
        self.response = response

class App(QFrame):
    APPID = "wormhole-qt.com"
    relay_url = RENDEZVOUS_RELAY
    _tor = None
    _timing = {}
    _reactor = reactor

    def __init__(self):
        super().__init__()

        self.initUI()

        self.wormhole = create(self.APPID, self.relay_url,
                   self._reactor,
                   tor=self._tor,
                   timing=self._timing)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasUrls:
            print(e.mimeData().urls()[0].toString())
            self.pathField.setText(e.mimeData().urls()[0].toString())
            for url in e.mimeData().urls():
                print(url)

    def initUI(self):
        title = QLabel("Wormhole", self)
        #self.setStyleSheet("background-color: rgb(200,200,200); margin:5px; border:1px solid rgb(0, 0, 0); ")

        vbox = QVBoxLayout()
        vbox.addStretch(5)
        vbox.addWidget(title)
        vbox.addLayout(self.initSendBox())
        vbox.addStretch(1)
        vbox.addLayout(self.initReceiveBox())
        vbox.addStretch(5)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.setAcceptDrops(True)
        self.show()


    def handleSend(self):
        print("Send")
        # s = TransitSender(RENDEZVOUS_RELAY)
        # my_direct_hints = yield s.get_connection_hints()
        # print(my_direct_hints)
        # b = util.dict_to_bytes(my_direct_hints)

        #self.wormhole.allocate_code()
        self.wormhole.set_code("wit")
        #code = yield w.get_code()
        #print("code:", code)
        self.wormhole.send_message(b"send helo")
        inbound = yield self.wormhole.get_message()
        print(inbound)
        yield self.wormhole.close()
        #dump = util.bytes_to_dict(inbound)

        # s.add_connection_hints(dump)
        # s.set_transit_key(self.APPID + "/tjoptawoo")
        # rp = yield s.connect()
        # rp.send_record(b"Sender sends")
        # them = yield rp.receive_record()
        # print("Sender" + them)
        # yield rp.close()



    def handleReceive(self):
        print("Receive")
        # s = TransitReceiver(RENDEZVOUS_RELAY)
        # my_direct_hints = yield s.get_connection_hints()
        # print(my_direct_hints)
        # b = util.dict_to_bytes(my_direct_hints)

        # self.wormhole.allocate_code()
        self.wormhole.set_code("wit")
        # code = yield w.get_code()
        # print("code:", code)
        self.wormhole.send_message(b"receive helo")
        inbound = yield self.wormhole.get_message()
        print(inbound)
        yield self.wormhole.close()
        #dump = util.bytes_to_dict(inbound)

        # s.add_connection_hints(dump)
        # s.set_transit_key(self.APPID + "/tjoptawoo")
        # rp = yield s.connect()
        # rp.send_record(b"receiver send")
        # them = yield rp.receive_record()
        # print("Receiver" + them)
        # yield rp.close()


    def handleBrowse(self):
        self.openFileNameDialog()

    def initSendBox(self):
        box = QVBoxLayout()

        headerText = QLabel("Send")

        headerRow = QHBoxLayout()
        headerRow.addStretch(1)
        headerRow.addWidget(headerText)
        headerRow.addStretch(1)


        label = QLabel("Path:")
        pathField = QLineEdit()
        self.pathField = pathField
        browseButton = QPushButton("Browse")
        browseButton.clicked.connect(self.handleBrowse)

        firstRow = QHBoxLayout()
        firstRow.addStretch(1)
        firstRow.addWidget(label)
        firstRow.addWidget(pathField)
        firstRow.addWidget(browseButton)
        firstRow.addStretch(1)

        sendButton = QPushButton("Send")
        sendButton.clicked.connect(self.handleSend)

        secondRow = QHBoxLayout()
        secondRow.addStretch(1)
        secondRow.addWidget(sendButton)
        secondRow.addStretch(1)


        box.addLayout(headerRow)
        box.addLayout(firstRow)
        box.addLayout(secondRow)

        return box

    def initReceiveBox(self):
        box = QVBoxLayout()

        headerText = QLabel("Receive")

        headerRow = QHBoxLayout()
        headerRow.addStretch(1)
        headerRow.addWidget(headerText)
        headerRow.addStretch(1)

        label = QLabel("Path:")
        pathField = QLineEdit()

        browseButton = QPushButton("Browse")

        firstRow = QHBoxLayout()
        firstRow.addStretch(1)
        firstRow.addWidget(label)
        firstRow.addWidget(pathField)
        firstRow.addWidget(browseButton)
        firstRow.addStretch(1)

        receiveButton = QPushButton("Receive")
        receiveButton.clicked.connect(self.handleReceive)

        secondRow = QHBoxLayout()
        secondRow.addStretch(1)
        secondRow.addWidget(receiveButton)
        secondRow.addStretch(1)

        box.addLayout(headerRow)
        box.addLayout(firstRow)
        box.addLayout(secondRow)

        return box

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

def run_QTApp():
    app = QApplication(sys.argv)
    ex = App()
    ex.handleSend()
    sys.exit(app.exec_())



if __name__ == '__main__':
    thread = Thread(target=run_QTApp)
    thread.start()
    print("Runnig reactor")
    reactor.run()


