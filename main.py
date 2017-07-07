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
from PyQt5.QtWidgets import (QFrame, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QApplication, QFileDialog, QProgressBar)
from os.path import isfile
from WormholeService import WormholeService

class RespondError(Exception):
    def __init__(self, response):
        self.response = response

class App(QFrame):
    APPID = "wormhole-qt.com"
    codeUpdatePrefix = "Wormhole code is: "

    def __init__(self):
        super().__init__()
        self.initUI()
        self.wormholeService = WormholeService(self.sending_callback, self.receving_callback)


    def sending_callback(self, update):
        print(update)
        infos = update.get("data")
        progress = update.get("progress")
        if progress:
            self.send_progress_bar.setProperty("value", progress)
            return

        for info in infos:
            if info.startswith(self.codeUpdatePrefix):
                print("helo")
                code = info[len(self.codeUpdatePrefix):]
                print(code)
                self.send_status_label.setText(code)


    def receving_callback(self, update):
        print(update)
        progress = update.get("progress")
        if progress:
            self.receive_progress_bar.setProperty("value", progress)



    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasUrls:
            file_path = e.mimeData().urls()[0].toLocalFile()
            self.path_field.setText(file_path)

    def initUI(self):
        title = QLabel("Wormhole", self)
        self.setStyleSheet("background-color: rgb(200,200,200); margin:5px; border:1px solid rgb(0, 0, 0); ")

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
        file_path = self.path_field.displayText()
        if isfile(file_path):
            t = Thread(target=lambda: self.wormholeService.send(file_path))
            t.daemon = True
            t.start()


    def handleReceive(self):
        t = Thread(target=lambda: self.wormholeService.receive(self.code_field.displayText()))
        t.daemon = True
        t.start()


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
        self.send_path = pathField
        browseButton = QPushButton("Browse")
        browseButton.clicked.connect(self.handleBrowse)
        self.path_field = pathField

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

        progressBar = QProgressBar()
        progressBar.setTextVisible(False)
        self.send_progress_bar = progressBar

        statusLable = QLabel("")
        self.send_status_label = statusLable
        statusRow = QHBoxLayout()
        statusRow.addStretch(1)
        statusRow.addWidget(statusLable)
        statusRow.addStretch(1)

        progressRow = QHBoxLayout()
        progressRow.addStretch(1)
        progressRow.addWidget(progressBar)
        progressRow.addStretch(1)

        box.addLayout(headerRow)
        box.addLayout(firstRow)
        box.addLayout(secondRow)
        box.addLayout(statusRow)
        box.addLayout(progressRow)

        return box

    def initReceiveBox(self):
        box = QVBoxLayout()

        headerText = QLabel("Receive")

        headerRow = QHBoxLayout()
        headerRow.addStretch(1)
        headerRow.addWidget(headerText)
        headerRow.addStretch(1)

        label = QLabel("Path:")
        code_field = QLineEdit()
        self.code_field = code_field

        browseButton = QPushButton("Browse")

        firstRow = QHBoxLayout()
        firstRow.addStretch(1)
        firstRow.addWidget(label)
        firstRow.addWidget(code_field)
        firstRow.addWidget(browseButton)
        firstRow.addStretch(1)

        receiveButton = QPushButton("Receive")
        receiveButton.clicked.connect(self.handleReceive)

        secondRow = QHBoxLayout()
        secondRow.addStretch(1)
        secondRow.addWidget(receiveButton)
        secondRow.addStretch(1)

        receiveStatusLabel = QLabel("")
        self.receive_status_label = receiveStatusLabel
        statusRow = QHBoxLayout()
        statusRow.addStretch(1)
        statusRow.addWidget(receiveStatusLabel)
        statusRow.addStretch(1)

        progressBar = QProgressBar()
        progressBar.setTextVisible(False)
        self.receive_progress_bar = progressBar

        receiveProgressRow = QHBoxLayout()
        receiveProgressRow.addStretch(1)
        receiveProgressRow.addWidget(progressBar)
        receiveProgressRow.addStretch(1)

        box.addLayout(headerRow)
        box.addLayout(firstRow)
        box.addLayout(secondRow)
        box.addLayout(statusRow)
        box.addLayout(receiveProgressRow)

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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

