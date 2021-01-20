#!/usr/bin/env python3

__author__ = "Team B"
__status__ = "Working Module"
__version__ = "1.0"

""" This module creates a GUI to be used in combination with the main script. 
Can be both run the main script locally or trough ssh."""

import sys
import random
import os
import json
import time
import subprocess
import string
import datetime
from shutil import copy2
from typing import Optional

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSlot, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QPushButton, QLabel, QGroupBox, QWidget, QHBoxLayout, \
    QScrollArea, \
    QMessageBox, QInputDialog

from jinja2 import Environment, FileSystemLoader, Template

from ssh_connection import Session


class Worker(QRunnable):
    """
    Worker thread which handles execution of jobs.
    """

    def __init__(self, session_ssh, queue_label):
        super(Worker, self).__init__()
        self.session: Session = session_ssh
        self.queue: dict = {}
        self.queue_label: QObject = queue_label

    @pyqtSlot()
    def run(self):
        """
        Queue function that checks for jobs every n seconds
        """
        seconds_between_checks: int = 1
        while True:
            time.sleep(seconds_between_checks)
            self.update_label_queue()
            if self.queue:
                jobs_this_itteration: list[dict] = []
                queue_copy: dict = dict.copy(self.queue)
                for job in queue_copy:
                    jobs_this_itteration.append(job)
                    self.process_job(job_id=job, data=queue_copy[job])

                for job in jobs_this_itteration:
                    self.queue.pop(job)

    def add_job(self, job_id: str, data: dict):
        """
        Add a job to the current queue
        """
        self.queue[job_id] = data

    def update_label_queue(self):
        """
        Change the text of the label queue_label
        """
        self.queue_label.setText(str(len(self.queue)))

    def process_job(self, job_id: str, data: dict):
        """
        Processes a job from the queue.
        """
        # Basic param
        output: str = data["output"] + "/" + job_id
        filenames: str = data["filenames"]
        widget_obj: QObject = data["widget"]
        mode: bool = data["mode"]
        tools: dict = data["tools"]
        threads: int = data["threads"]
        console: QObject = data["console"]

        # Get tools
        pipeline: str = tools["pipeline"]
        refseq: str = tools["refseq"]
        gtf: str = tools["gtf"]
        trimgalore: str = tools["trimgalore"]
        cutadapt: str = tools["cutadapt"]
        minimap: str = tools["minimap"]
        fastqc: str = tools["fastqc"]
        featurecounts: str = tools["feature"]

        # Select GUI compontents
        groupbox: QObject = widget_obj.findChild(QScrollArea).findChild(QGroupBox, job_id)
        file_status_label: QObject = widget_obj.findChild(QScrollArea).findChild(QGroupBox,
                                                                                 job_id).findChild(
            QLabel,
            "file_status")
        save_button: QObject = widget_obj.findChild(QScrollArea).findChild(QGroupBox,
                                                                           job_id).findChild(
            QPushButton,
            "save_file")
        log_button: QObject = widget_obj.findChild(QScrollArea).findChild(QGroupBox,
                                                                          job_id).findChild(
            QPushButton,
            "get_error")
        failed_job: QObject = widget_obj.findChild(QLabel, "label_failed_nr")

        # file_status
        file_status_label.setText("In progress...")

        # Create string
        command: str = f"python3 {pipeline} --files {' '.join(filenames)} --out {output}" \
                       f" --threads {threads} --refseq {refseq} --gtf {gtf} " \
                       f"--trimgalore {trimgalore} --cutadapt {cutadapt} " \
                       f"--minimap2 {minimap} --fastqc {fastqc} --featurecounts {featurecounts} "

        if mode:
            stdout, stderr = run_local_script(command=command, label=file_status_label,
                                              console=console)
            groupbox.stdout = stdout
            groupbox.stderr = stderr
        else:
            # Run tool trough ssh
            stdin, stdout, stderr = run_ssh_script(self.session, command=command,
                                                   label=file_status_label,
                                                   console=console)

        # Redeclare values
        groupbox.stdout = stdout
        groupbox.stderr = stderr
        groupbox.run_output = output
        groupbox.run_mode = mode
        groupbox.job_id = job_id
        groupbox.output = data["output"]
        groupbox.filenames = data["filenames"]
        groupbox.widget_obj = data["widget"]
        groupbox.mode = data["mode"]
        groupbox.jobname = data["jobname"]
        groupbox.tools = data["tools"]
        data["stderr"] = groupbox.stderr
        data["stdout"] = groupbox.stdout
        groupbox.data = data

        # Check if job failed or was run successfully
        if not groupbox.stderr:
            file_status_label.setText("Finished succesfully!")
            save_button.setHidden(False)
            groupbox.success = 1
            data["success"] = 1
        else:
            failed_job.setText(str(int(failed_job.text()) + 1))
            groupbox.success = 0
            data["success"] = 0
            file_status_label.setText("Job failed!")

        # Show the log button. So user can check log files
        log_button.setHidden(False)


def run_local_script(command: str, label: QObject, console: QObject) -> tuple[list[str], str]:
    """
    Runs a command on local machine. and checks stdin, stout and sterr constantly
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    list_stdout: list = []
    while True:
        output: bytes = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            line: str = output.strip().decode('utf-8')
            console.append(line)
            list_stdout.append(line + "\n")
    stderr: str = process.stderr.read().decode("utf-8")
    return list_stdout, stderr


def run_ssh_script(session: Session, command: str, label: QObject, console: QObject) -> \
        tuple[str, list[str], list[str]]:
    """
    Runs a command on the ssh machine. Checks constantly for stdout, stdout, stderr change.
    """
    stdin, stdout, stderr = session.client.exec_command(command, get_pty=True)
    list_stdout: list = []
    list_stderr: list = []
    while not stdout.channel.exit_status_ready():
        for line in iter(lambda: stdout.readline(2048), ""):
            console.append(line)
            list_stdout.append(line)
        for line in iter(lambda: stderr.readline(2048), ""):
            list_stderr.append(line)
    if stdout.channel.recv_exit_status() != 0:
        list_stderr.append("See Stdout for error")
    for channel in [stdin, stdout, stderr]:
        channel.channel.close()
    return stdin, list_stdout, list_stderr


def generate_log(data: dict) -> list:
    """Generates the log from template and from the provided data"""
    env: Environment = Environment(loader=FileSystemLoader("ui_views/resources"))
    template: Template = env.get_template('log_template.html')
    timestamp: str = datetime.datetime.now().strftime("%d-%B-%y at %T")
    output_from_parsed_template: bytes = template.render(data=data, timestamp=timestamp)
    return [output_from_parsed_template]


class LogWindow(QtWidgets.QDialog):
    """
    A dialog that is created for every job. This uses a html template to populate the texbrowser
    """
    def __init__(self):
        super(LogWindow, self).__init__()
        uic.loadUi("ui_views/logwindow.ui", self)
        self.pushButton_close.clicked.connect(lambda: self.close())

    def print_to_browser(self, data: list):
        """Add the lines in data to the textbrowser"""
        for line in data:
            self.textBrowser.append(line)
        self.exec()


def _generate_job_id():
    """Generates a random string containing 20 characters"""
    pool: list[str] = string.ascii_uppercase + string.digits
    return "".join(random.sample(pool, 20))


def open_log_dialog(sender):
    """Opens the log dialog"""
    groupbox: QObject = sender.parent()
    log: QObject = sender.parent().log
    data: dict = log.generate_log(groupbox.data)
    log.print_to_browser(data)


def openFileNamesDialog(defaultdir="/") -> Optional[list[str]]:
    """Opens a filenames dialog"""
    files, _ = QFileDialog.getOpenFileNames(None, 'Open file(s)', defaultdir,
                                            "Fasta file (*.fasta *.fastq);;all files(*.*)")
    if files:
        return files
    return None


def saveFileDialog(filename="output.pdf") -> Optional[str]:
    """Create a new popup save dialog"""
    defaultdir = f"/{filename}"
    files, _ = QFileDialog.getSaveFileName(None, 'Save file', defaultdir,
                                           "PDF file(*.pdf);;all files(*.*)")
    if files:
        return files
    return None


class MainWindow(QtWidgets.QMainWindow):
    """Main class that contains all object to generate the GUI"""

    def __init__(self):
        super(MainWindow, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("ui_views/mainwindow.ui", self)

        # Default values:
        self.mode_isLocal: bool = False
        self.session: Session = Session()
        self.file_list: list = []

        self.active_jobs: int = 0
        self.current_jobs: int = 0
        self.failed_jobs: int = 0

        # Start subprocess
        self.threadpool: QThreadPool = QThreadPool()
        self.worker: Worker = Worker(session_ssh=self.session,
                                     queue_label=self.label_active_jobs_nr)
        self.threadpool.start(self.worker)
        # Load defaults:
        self.set_default_ssh()
        self.set_default_tools()
        self.set_default_run()

        # Init buttons navigation
        self.update_mode()
        self.radioButton_mode_local.toggled.connect(self.update_mode)
        self.radioButton_mode_ssh.toggled.connect(self.update_mode)

        self.pushButton_nav_ssh.clicked.connect(lambda: self.change_view(0))
        self.pushButton_nav_tools.clicked.connect(lambda: self.change_view(1))
        self.pushButton_nav_run.clicked.connect(lambda: self.change_view(2))

        self.pushButton_nav_jobs.clicked.connect(lambda: self.change_view(4))

        # Init SSH buttons
        self.pushButton_connect.clicked.connect(self.ssh_connect)
        self.pushButton_drop_connection.clicked.connect(self.ssh_disconnect)
        self.pushButton_saveconnection.clicked.connect(
            lambda: set_default(path="saved_data/default_ssh.json",
                                data=self.get_fields_ssh(
                                    self.checkBox_save_password.isChecked())))
        self.pushButton_save_paths.clicked.connect(
            lambda: set_default(
                path=f"saved_data/default_tools_{'local' if self.mode_isLocal else 'ssh'}.json",
                data=self.get_fields_tools()))

        # Run buttons
        self.pushButton_addfiles.clicked.connect(self.get_files)
        self.pushButton_save_output.clicked.connect(
            lambda: set_default(
                path=f"saved_data/default_run_{'local' if self.mode_isLocal else 'ssh'}.json",
                data=self.get_fields_run()))
        self.pushButton_run_pipeline.clicked.connect(self.run_pipe)

        # SSH file selection
        self.pushButton_search_path.clicked.connect(self.ssh_file_selector)
        self.pushButton_ssh_file_continue.clicked.connect(self.populate_main_file)

        self.show()

    def update_mode(self):
        """Set mode to local or ssh"""
        if self.radioButton_mode_local.isChecked() and not self.radioButton_mode_ssh.isChecked():
            self.mode_isLocal: bool = True
            self.set_default_run()
            self.set_default_tools()
            return True
        else:
            self.mode_isLocal: bool = False
            self.set_default_run()
            self.set_default_tools()
            return False

    def change_view(self, index):
        """Change view of the stackedWidget"""
        self.stackedWidget_pages.setCurrentIndex(index)

    def get_files(self):
        """Get (fasta) files"""
        self.update_mode()
        files: list = []
        if self.mode_isLocal:
            files: list[str] = openFileNamesDialog()

        else:
            self.clear_files_ssh()
            self.get_files_ssh()

        if files:
            for file in files:
                self.file_list.append(file)
                self._populate_file_list(file)

    def get_files_ssh(self):
        """Checks if there is an active session and then changes view to index for ssh files"""
        if self.session.isActive:
            self.stackedWidget_pages.setCurrentIndex(3)
        else:
            create_message_box(msg_type="warning", text="No active SSH connection",
                               informative="Connect to ssh trough 'SSH Setup'")

    def populate_main_file(self):
        """Creates label + button for every file"""
        for file in self.file_list:
            self._populate_file_list(file)
        self.change_view(2)

    def get_fields_ssh(self, password=True) -> dict[str, str]:
        """
        Gets all values from the lineEdit classes from ssh page.
        :param password: if False, changes string with password to empty string
        :return: data as dict
        """
        field_values = {self.label_hostname.text(): self.lineEdit_host.text(),
                        self.label_username.text(): self.lineEdit_username.text(),
                        self.label_port.text(): self.lineEdit_port.text(),

                        self.label_publickey.text(): self.lineEdit_publickey.text() if
                        self.lineEdit_publickey.text() else None,

                        self.label_password.text(): self.lineEdit_password.text() if password
                        else ''}
        return field_values

    def get_fields_tools(self) -> dict[str, str]:
        """
        Gets all values from the lineEdit classes from tools page.
        :return: data as dict
        """
        data = {'pipeline': self.lineEdit_pipeline_script_path.text(),
                'trimgalore': self.lineEdit_trimgalore_path.text(),
                'cutadapt': self.lineEdit_cutadapt_path.text(),
                'minimap': self.lineEdit_minimap_path.text(),
                'fastqc': self.lineEdit_fastqc_path.text(),
                'refseq': self.lineEdit_refseq.text(),
                'gtf': self.lineEdit_gtf_path.text(),
                'feature': self.lineEdit_feature.text()}
        return data

    def get_fields_run(self) -> dict[str, str]:
        """
        Gets all values from the lineEdit classes from run page.
        :return: data as dict
        """
        data = {self.label_threads.text(): self.spinBox_threads.value(),
                self.label_skip.text(): self.checkBox_skip_files.isChecked(),
                self.label_pipeline_output_path.text(): self.lineEdit_pipeline_output.text()}
        return data

    def ssh_connect(self):
        """
        Sets up a ssh connection
        """
        fields: dict[str, str] = self.get_fields_ssh()
        try:
            self.session.client.load_system_host_keys()
            self.session.client.connect(hostname=fields[self.label_hostname.text()],
                                        username=fields[self.label_username.text()],
                                        port=fields[self.label_port.text()],
                                        password=fields[self.label_password.text()])
            self.session.isActive = True
            informative = '\n'.join(
                [f"{x}: {fields[x]}" if x != "Password" else '' for x in fields])
            self.ssh_connection_label_update()
            create_message_box(text="Connection established!",
                               informative=f"Connected to:\n{informative}")
        except Exception as e:
            self.ssh_connection_label_update()
            create_message_box(msg_type='critical', text=str(e),
                               informative=f"Please check your provided parameters.")

    def ssh_disconnect(self, message=True):
        """
        Disconnects the connection to ssh
        """
        self.session.client.close()
        self.session.isActive = False
        self.ssh_connection_label_update()
        if message:
            create_message_box(text="Connection closed!")

    def set_default_ssh(self):
        """Changes the text in ssh page to saved strings"""
        data: dict[str, str] = load_default("saved_data/default_ssh.json")
        if data:
            self.lineEdit_host.setText(data[self.label_hostname.text()])
            self.lineEdit_username.setText(data[self.label_username.text()])
            self.lineEdit_password.setText(data[self.label_password.text()])
            self.lineEdit_publickey.setText(data[self.label_publickey.text()])
            self.lineEdit_port.setText(data[self.label_port.text()])

    def set_default_tools(self):
        """Changes the text in tools page to saved strings"""
        if self.mode_isLocal:
            data: dict[str, str] = load_default("saved_data/default_tools_local.json")
        else:
            data: dict[str, str] = load_default("saved_data/default_tools_ssh.json")
        if data:
            self.lineEdit_pipeline_script_path.setText(data['pipeline'])
            self.lineEdit_trimgalore_path.setText(data['trimgalore'])
            self.lineEdit_cutadapt_path.setText(data['cutadapt'])
            self.lineEdit_minimap_path.setText(data['minimap'])
            self.lineEdit_fastqc_path.setText(data['fastqc'])
            self.lineEdit_refseq.setText(data['refseq'])
            self.lineEdit_gtf_path.setText(data['gtf'])
            self.lineEdit_feature.setText(data['feature'])

    def set_default_run(self):
        """Changes the text in run page to saved strings"""
        if self.mode_isLocal:
            data: dict[str, str] = load_default("saved_data/default_run_local.json")
        else:
            data: dict[str, str] = load_default("saved_data/default_run_ssh.json")
        if data:
            self.spinBox_threads.setValue(data[self.label_threads.text()])
            self.checkBox_skip_files.setChecked(bool(self.label_skip.text()))
            self.lineEdit_pipeline_output.setText(data[self.label_pipeline_output_path.text()])

    def ssh_connection_label_update(self):
        """Updates the connection_label to the correct string"""
        if self.session.isActive:
            self.label_ssh_connection.setText("SSH: Connected")
            self.label_ssh_connection.setStyleSheet("background-color: lightgreen")
        else:
            self.label_ssh_connection.setText("SSH: No Connection")
            self.label_ssh_connection.setStyleSheet("background-color: red")

    def ssh_file_selector(self):
        """Function that handles the file selection if SSH protocol is used"""
        path: str = self.lineEdit_file_path_ssh.text()
        filenames_filtered: list = []
        if path:
            filenames: list[str] = self.session.probe_dir(path)

            if filenames:
                for name in filenames:
                    if name.endswith(".fastq") or name.endswith(".fastq.gz"):
                        filenames_filtered.append(name)

            if filenames_filtered:
                filenames_filtered = [os.path.join(path, x) for x in filenames_filtered]
                self._populate_file_ssh_left(files=filenames_filtered)
            else:
                found: str = "Files / folders found:\n"
                if type(filenames) == list:
                    found += "\n".join(filenames)
                elif type(filenames) == str:
                    found += filenames

                create_message_box(msg_type="critical",
                                   text="Could not find any (supported) files in provided path",
                                   informative="fastq and fastq.gz are only supported",
                                   details=found)
        else:
            create_message_box(msg_type="warning", text="Path can't be empty")

    # Populate file list. Underlying functions create new widgets.
    def _populate_file_list(self, file):
        """Creates individual file objects in the files widgets on the run page"""
        filename: str = file.split("/")[-1]
        file_label: QObject = QLabel(filename)

        # Create delete button
        delete_btn: QObject = QPushButton("Remove")
        delete_btn.setIcon(QIcon('ui_views/resources/delete.png'))
        delete_btn.setMinimumWidth(20)
        delete_btn.setMaximumWidth(100)
        delete_btn.setFlat(False)
        delete_btn.setObjectName(file)
        delete_btn.clicked.connect(lambda: self.delete_file(self.sender()))

        # Create file box
        file_box: QObject = QGroupBox()
        file_box.setObjectName(file)
        file_box.setMaximumHeight(25)

        # Create layout box
        layout_file_box: QObject = QHBoxLayout(file_box)
        layout_file_box.addWidget(file_label)
        layout_file_box.addWidget(delete_btn)
        layout_file_box.setContentsMargins(0, 0, 0, 0)

        # Create Groupbox
        group: QObject = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        group.setObjectName(file)
        group.setLayout(layout_file_box)

        # Assign layouts
        self.verticalLayout_files.addWidget(group)
        self.label_files.setHidden(True)

    def _populate_file_ssh_left(self, files):
        """Creates individual file objects in the left column on the SSH file selector page"""
        for file in files:
            filename = file.split("/")[-1]
            file_label = QLabel(filename)

            # Create move button
            move_btn: QObject = QPushButton()
            move_btn.setIcon(QIcon('ui_views/resources/arrow_right.svg'))
            move_btn.setMinimumWidth(20)
            move_btn.setMaximumWidth(20)
            move_btn.setFlat(True)
            move_btn.setObjectName(file)
            move_btn.clicked.connect(lambda: self._populate_file_ssh_right(self.sender()))

            # Create file box
            file_box: QObject = QGroupBox()
            file_box.setObjectName(file)

            # Create layout box
            layout_file_box = QHBoxLayout(file_box)
            layout_file_box.addWidget(file_label)
            layout_file_box.addWidget(move_btn)

            # Create groupbox
            group = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_left)
            group.setObjectName(file)
            group.setLayout(layout_file_box)

            # Assign layout
            self.verticalLayout_left_ssh.addWidget(group)
            self.label_ssh_left.setHidden(True)

    def _populate_file_ssh_right(self, sender: QObject):
        """Creates individual file objects in the right column on the SSH file selector page"""

        # Delete file from the right file list
        self.delete_file(sender)
        sender.parent().setHidden(True)
        sender.parent().deleteLater()

        # Get parameters
        file: str = sender.objectName()
        filename: str = file.split("/")[-1]
        file_label: QObject = QLabel(filename)

        # Create move button
        move_btn: QObject = QPushButton()
        move_btn.setIcon(QIcon('ui_views/resources/delete.png'))
        move_btn.setMinimumWidth(20)
        move_btn.setMaximumWidth(20)
        move_btn.setFlat(True)
        move_btn.setObjectName(file)
        move_btn.clicked.connect(lambda: self.delete_file(self.sender()))

        # Create file box
        file_box: QObject = QGroupBox()
        file_box.setObjectName(file)

        # Create layout
        layout_file_box: QObject = QHBoxLayout(file_box)
        layout_file_box.addWidget(file_label)
        layout_file_box.addWidget(move_btn)

        # Create groupbox
        group: QObject = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_right)
        group.setObjectName(file)
        group.setLayout(layout_file_box)

        # Set layouts
        self.verticalLayout_ssh_right.addWidget(group)
        self.label_ssh_right.setHidden(True)
        self.file_list.append(file)

    def delete_file(self, sender):
        """Remove file from list"""

        # Delete parent Qobject
        sender.parent().setHidden(True)
        sender.parent().deleteLater()
        try:
            self.file_list.remove(sender.parent().objectName())
        except ValueError:
            pass
        if not sender.parent().parent().findChildren(QGroupBox):
            sender.parent().parent().findChild(QLabel).setHidden(False)

    def clear_files_ssh(self):
        """Deletes all labels + buttons for filenames"""
        data: list[QObject] = self.findChild(QWidget,
                                             'scrollAreaWidgetContents_right').findChildren(
            QGroupBox)
        data += self.findChild(QWidget, 'scrollAreaWidgetContents_left').findChildren(QGroupBox)
        if data:
            for file in data:
                file.deleteLater()
                file.parent().findChild(QLabel).setHidden(False)

    def gettext(self) -> Optional[str]:
        """Creates a Inputdialog and asks for a jobname"""
        text, ok = QInputDialog.getText(self, 'Job name', 'Enter a job name:')
        if ok:
            if text == "":
                create_message_box(msg_type="warning", text="Job name not allowed to be empty")
                return None
            else:
                return text
        else:
            return None

    def run_pipe(self):
        files: list[str] = self.file_list
        output: str = self.lineEdit_pipeline_output.text()
        job_id: str = _generate_job_id()
        jobname: str = self.gettext()

        # Check if all prerequisites are fulfilled
        if not jobname or not files or not output:
            ready = False
        else:
            ready = True

        if ready:
            self.create_job_widget(jobname=jobname, job_id=job_id)
            self.label_files_jobs.setHidden(True)
            self.change_view(4)
            widget = self.findChild(QGroupBox, 'groupBox_jobs')
            self.add_job(job_id=job_id, jobname=jobname, output=output, filenames=files,
                         widget=widget,
                         mode=self.mode_isLocal, tools=self.get_fields_tools(),
                         threads=self.spinBox_threads.value(),
                         skip=self.checkBox_skip_files.isChecked())
        else:
            create_message_box(msg_type="warning", text="Can't start job!",
                               informative="not all prerequisistes are fullfilled. Check details "
                                           "for more info.",
                               details=f"Jobname provided: {bool(jobname)}\n"
                                       f"Output provided: {bool(output)}\nFiles "
                                       f"provided: {bool(files)}")

    def add_job(self, job_id, jobname, output, filenames, widget, mode, tools, threads, skip):
        """Gets parameters and runs the add_job method from Worker class"""
        data: dict = {"output": output, "filenames": filenames, "widget": widget, "mode": mode,
                      "jobname": jobname,
                      "job_id": job_id, "tools": tools, "threads": threads, "skip": skip,
                      "console": self.textBrowser_console}
        self.worker.add_job(job_id=job_id, data=data)

    def create_job_widget(self, jobname, job_id):
        """Creates a new widget which will be added to the job area"""
        # Create label
        file_label: QObject = QLabel(f"Name: {jobname}")
        file_label_status: QObject = QLabel("In queue...")
        file_label_status.setObjectName("file_status")
        file_label_status.setMaximumHeight(25)

        # Create button get file
        btn_get_file: QObject = QPushButton("Save report (PDF)")
        btn_get_file.setObjectName("save_file")
        btn_get_file.setHidden(True)
        btn_get_file.clicked.connect(lambda: self.save_finished_file(self.sender()))

        # Create button get log
        btn_log: QObject = QPushButton("Get log")
        btn_log.setObjectName("get_error")
        btn_log.setMaximumWidth(100)
        btn_log.setHidden(True)
        btn_log.clicked.connect(lambda: open_log_dialog(self.sender()))

        # Create groupbox
        file_box: QObject = QGroupBox()
        file_box.setObjectName(job_id)
        file_box.setMaximumHeight(25)

        # Extra data
        file_box.stderr = None
        file_box.stdout = None
        file_box.run_output = None
        file_box.run_pdf_location = None
        file_box.run_mode = None
        file_box.success = None

        # Add widgets
        layout_file_box: QObject = QHBoxLayout(file_box)
        layout_file_box.addWidget(file_label)
        layout_file_box.addWidget(file_label_status)
        layout_file_box.addWidget(btn_get_file)
        layout_file_box.addWidget(btn_log)

        # Set margins
        layout_file_box.setContentsMargins(0, 0, 0, 0)

        # Create Qgroupbox
        group: QObject = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        group.setObjectName(job_id)
        group.setLayout(layout_file_box)
        group.log = LogWindow()

        # Set layout
        self.verticalLayout_jobs.addWidget(group)

    def save_finished_file(self, sender):
        groupbox: QObject = sender.parent()

        save_location: str = saveFileDialog(filename=groupbox.jobname)
        remote_path: str = f"{groupbox.run_output}/MultiQC/multiqc_report.pdf"
        if groupbox.run_mode:
            try:
                print("Local")
                copy2(remote_path, save_location)
            except Exception as exception:
                create_message_box(msg_type="critical", title="Error",
                                   text="Error while saving PDF",
                                   informative=f"Something went wrong while getting pdf.\n"
                                               f"File can also be found on host at: {remote_path}",
                                   details=str(exception))
        else:

            try:
                self.session.sftp.get(remote_path, save_location)
                create_message_box(title="Save file", text=f"Saved file successfully!",
                                   informative=save_location)
            except Exception as e:
                create_message_box(msg_type="critical", title="Error", text="Error while saving PDF"
                                   , informative=f"Something went wrong while getting pdf from your"
                                                 f" SSH host.\n "
                                                 f"File can also be found on host at: {remote_path}"
                                   , details=str(e))


def set_default(path: str, data: dict[str: str]):
    """
    Creates a json file with name according to provided path
    :param path: filename
    :param data: data containing the values of the individual editLine objects
    :return: nothing
    """
    # Notify user with message box
    informative: str = "\n".join([f"{x}:\t{data[x] if x != 'password' else ''}" for x in data])
    create_message_box(text="Set default",
                       informative=informative)

    # Save data as json
    with open(path, "w") as stream:
        stream.write(json.dumps(data, indent=4))


def load_default(path: str) -> Optional[dict]:
    """
    Opens json file and returns as dicts
    :param path: path of json file
    :return: dictionary
    """
    if os.path.exists(path):
        with open(path, "r") as stream:
            data: dict = json.load(stream)
        return data


def create_message_box(text="no text provided", informative=None, title="popup", details=None,
                       msg_type="info"):
    """
    Creates and shows a popup notification
    :param text: primary text
    :param informative: extra information
    :param title: title of the popup
    :param details: extra details
    :param msg_type: str that determines the displayed icon
    """
    msg: QObject = QMessageBox()
    icon: dict[str, QMessageBox.icon] = {"info": QMessageBox.Information,
                                         "warning": QMessageBox.Warning,
                                         "critical": QMessageBox.Critical,
                                         "question": QMessageBox.Question}
    msg.setIcon(icon[msg_type])
    msg.setWindowTitle(title)
    msg.setText(text)
    if informative:
        msg.setInformativeText(informative)
    if details:
        msg.setDetailedText(details)
    msg.exec()


if __name__ == '__main__':
    app: QtWidgets.QApplication = QtWidgets.QApplication(
        sys.argv)  # Create an instance of QtWidgets.QApplication
    main_window: MainWindow = MainWindow()
    app.exec_()  # Start the application
