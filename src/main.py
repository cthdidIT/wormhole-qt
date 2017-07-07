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
from os.path import isfile
from threading import Thread

from PyQt5.QtWidgets import (QFrame, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QApplication,
                             QFileDialog, QProgressBar)

from WormholeService import WormholeService


class RespondError(Exception):
    def __init__(self, response):
        self.response = response

class App(QFrame):
    APPID = "wormhole-qt.com"
    codeUpdatePrefix = "Wormhole code is: "
    transferErrorUpdatePrefix = "TransferError:"
    errorUpdatePrefix = "ERROR:"

    def __init__(self):
        super().__init__()
        self.initUI()
        self.wormholeService = WormholeService(self.sending_callback, self.receving_callback)

    sendErrorUpdateAccumulator = ""
    def sending_callback(self, update):
        print(update)
        infos = update.get("data")
        progress = update.get("progress")
        if progress:
            self.send_progress_bar.setProperty("value", progress)
            return


        for info in infos:
            if info.startswith(self.codeUpdatePrefix):
                code = info[len(self.codeUpdatePrefix):]
                self.send_status_label.setText(code)
                self.sendErrorUpdateAccumulator = ""

            elif info.startswith(self.transferErrorUpdatePrefix):
                error = info[len(self.transferErrorUpdatePrefix):]
                self.send_status_label.setText(error)
                self.sendErrorUpdateAccumulator = ""

            elif info.startswith(self.errorUpdatePrefix):
                self.sendErrorUpdateAccumulator = info[len(self.errorUpdatePrefix):]

            elif self.sendErrorUpdateAccumulator:
                self.sendErrorUpdateAccumulator += " " + info
                self.send_status_label.setText(self.sendErrorUpdateAccumulator)


    receiveErrorUpdateAccumulator = ""
    def receving_callback(self, update):
        print(update)
        infos = update.get("data")
        progress = update.get("progress")
        if progress:
            self.receive_progress_bar.setProperty("value", progress)
            return

        for info in infos:
            if info.startswith(self.errorUpdatePrefix):
                self.receiveErrorUpdateAccumulator = info[len(self.errorUpdatePrefix):]

            elif self.receiveErrorUpdateAccumulator:
                self.receiveErrorUpdateAccumulator += " " + info
                self.receive_status_label.setText(self.receiveErrorUpdateAccumulator)



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

        vbox = QHBoxLayout()
        vbox.addStretch(5)
        vbox.addWidget(self.initSendBox())
        vbox.addStretch(1)
        vbox.addWidget(self.initReceiveBox())
        vbox.addStretch(5)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('wormhole-qt')
        self.setAcceptDrops(True)
        self.show()

    def handleSend(self):
        file_path = self.path_field.displayText()
        if isfile(file_path):
            t = Thread(target=lambda: self.wormholeService.send(file_path))
            t.daemon = True
            t.start()


    def handleReceive(self):
        t = Thread(target=lambda: self.wormholeService.receive(self.code_field.displayText(), self.receive_path.displayText()))
        t.daemon = True
        t.start()


    def handleBrowse(self, lineEdit, dirsOnly=False):
        self.openFileNameDialog(lineEdit, dirsOnly)

    def initSendBox(self):
        box = QVBoxLayout()


        headerText = QLabel("Send")

        headerRow = QHBoxLayout()
        headerRow.addStretch(1)
        headerRow.addWidget(headerText)
        headerRow.addStretch(1)


        label = QLabel("Path:")
        pathField = QLineEdit()
        pathField.setMinimumWidth(100)
        self.send_path = pathField
        browseButton = QPushButton("Browse")
        browseButton.clicked.connect(lambda: self.handleBrowse(pathField))
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
        progressBar.setProperty("value", 0)
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

        frame = QFrame()
        frame.setLayout(box)
        frame.setLineWidth(10)
        frame.setFrameStyle(QFrame.StyledPanel)
        return frame

    def initReceiveBox(self):
        box = QVBoxLayout()

        headerText = QLabel("Receive")

        headerRow = QHBoxLayout()
        headerRow.addStretch(1)
        headerRow.addWidget(headerText)
        headerRow.addStretch(1)

        browseButton = QPushButton("Browse")
        pathLabel = QLabel("Download:")
        receivePath = QLineEdit("$HOME/Download")
        self.receive_path = receivePath
        browseButton.clicked.connect(lambda: self.handleBrowse(receivePath, dirsOnly=True))
        receivePath.setMinimumWidth(100)
        pathRow = QHBoxLayout()
        pathRow.addStretch(1)
        pathRow.addWidget(pathLabel)
        pathRow.addWidget(receivePath)
        pathRow.addWidget(browseButton)
        pathRow.addStretch(1)

        label = QLabel("Code:")
        code_field = QLineEdit()
        code_field.setMinimumWidth(100)
        self.code_field = code_field


        receiveButton = QPushButton("Receive")
        receiveButton.clicked.connect(self.handleReceive)

        codeRow = QHBoxLayout()
        codeRow.addWidget(label)
        codeRow.addWidget(code_field)
        codeRow.addWidget(receiveButton)



        receiveStatusLabel = QLabel("")
        self.receive_status_label = receiveStatusLabel
        statusRow = QHBoxLayout()
        statusRow.addStretch(1)
        statusRow.addWidget(receiveStatusLabel)
        statusRow.addStretch(1)

        progressBar = QProgressBar()
        progressBar.setProperty("value", 0)
        self.receive_progress_bar = progressBar

        receiveProgressRow = QHBoxLayout()
        receiveProgressRow.addStretch(1)
        receiveProgressRow.addWidget(progressBar)
        receiveProgressRow.addStretch(1)

        box.addLayout(headerRow)
        box.addLayout(pathRow)
        box.addLayout(codeRow)
        box.addLayout(statusRow)
        box.addLayout(receiveProgressRow)

        frame = QFrame()
        frame.setLayout(box)
        frame.setFrameStyle(QFrame.StyledPanel)
        return frame

    def openFileNameDialog(self, lineEdit, dirsOnly = False):
        options = QFileDialog.Options()
        fileName = ""
        if dirsOnly:
            options |= QFileDialog.ShowDirsOnly
            fileName = QFileDialog.getExistingDirectory(self, "Download folder", options=options)
        else:
            fileName, _ = QFileDialog.getOpenFileName(self, "File to send", "", options=options)

        if fileName:
            print(fileName)
            lineEdit.setText(fileName)

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

