import os
import subprocess
import sys

from bs4 import BeautifulSoup
from PySide6 import QtCore, QtWidgets

rp = os.path.dirname(os.path.realpath(__file__))
hkxCliJar = os.path.join(rp, "hkxpack-cli.jar")
havokToFbx = os.path.join(rp, "havok2fbx.exe")

if not os.path.exists(hkxCliJar):
	print("ERROR! Could not find hkxpack-cli.jar file. You need to drop this gui file in the same folder as hkxpack-cli.jar file! Otherwise it won't work.")

if not os.path.exists(havokToFbx):
	print("ERROR! Could not find havok2fbx.exe file. You need to drop this gui file in the same folder as havok2fbx.exe file! Otherwise it won't work. Or you can drop all havok2fbx.exe files into the folder with this gui.")

css = """
"""

class TestListView(QtWidgets.QListWidget):

	fileDropped = QtCore.Signal(list)

	def __init__(self, parent=None) -> None:
		super().__init__(parent)
		self.setAcceptDrops(True)
		self.setIconSize(QtCore.QSize(72, 72))

	def dragEnterEvent(self, event) -> None:
		if event.mimeData().hasUrls:
			event.accept()
		else:
			event.ignore()

	def dragMoveEvent(self, event) -> None:
		if event.mimeData().hasUrls:
			event.setDropAction(QtCore.Qt.DropAction.CopyAction)
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event) -> None:
		if event.mimeData().hasUrls:
			event.setDropAction(QtCore.Qt.DropAction.CopyAction)
			event.accept()
			links = []
			for url in event.mimeData().urls():
				links.append(str(url.toLocalFile()))
			self.fileDropped.emit(links)
		else:
			event.ignore()

class inputBoxWithBrowse(QtWidgets.QWidget):
	def __init__(self, parent=None, label="", placeholderText="", defaultPath = "") -> None:
		super().__init__(parent)
		self.placeholderText = placeholderText
		self.mainLayout = QtWidgets.QHBoxLayout()
		self.setLayout(self.mainLayout)

		self.lineEdit = QtWidgets.QLineEdit()
		self.lineEdit.setPlaceholderText(placeholderText)
		self.lineEdit.setText(defaultPath)

		self.browseBtn = QtWidgets.QPushButton("Browse")
		self.browseBtn.clicked.connect(self.browse)
		self.label = QtWidgets.QLabel(label)

		self.mainLayout.addWidget(self.label)
		self.mainLayout.addWidget(self.lineEdit)
		self.mainLayout.addWidget(self.browseBtn)

	def text(self) -> str:
		return self.lineEdit.text()

	def browse(self) -> None:
		fileName = QtWidgets.QFileDialog.getOpenFileName(self, caption=self.placeholderText, filter="*.hkx")
		self.lineEdit.setText(str(fileName[0]))

class MainForm(QtWidgets.QMainWindow):
	def __init__(self, parent=None) -> None:
		super().__init__(parent)

		self.mainWidget = QtWidgets.QWidget()
		self.mainLayout = QtWidgets.QVBoxLayout()
		self.mainWidget.setLayout(self.mainLayout)

		self.view = TestListView(self)
		self.view.fileDropped.connect(self.fileDropped)

		self.byLbl = QtWidgets.QLabel("GUI made by ShadeAnimator.")

		self.viewlabel = QtWidgets.QLabel("Drag and drop files here:")

		#region Pack Unpack Groupbox
		self.groupBox = QtWidgets.QGroupBox("Action")

		self.unpackRB = QtWidgets.QRadioButton("&Unpack")
		self.packRB = QtWidgets.QRadioButton("&Pack")

		self.unpackRB.setChecked(True)


		vbox = QtWidgets.QVBoxLayout()
		vbox.addWidget(self.unpackRB)
		vbox.addWidget(self.packRB)
		vbox.addStretch(1)
		self.groupBox.setLayout(vbox)
		#endregion
		self.pb = QtWidgets.QProgressBar()

		self.button = QtWidgets.QPushButton("HKX <=> XML")
		self.button.clicked.connect(self.convertXmlHkx)
		self.button.setToolTip("Convert HKX to XML and XML to HKX")

		self.getTxtButton = QtWidgets.QPushButton("Generate rig.txt from skeleton.hkx")
		self.getTxtButton.clicked.connect(self.generateRigTxt)
		self.getTxtButton.setToolTip("Given a skeleton.hkx or skeleton.xml file it will generate rig.txt for that skeleton.")

		self.remove = QtWidgets.QPushButton("Remove selected")
		self.remove.clicked.connect(self.removeSelected)

		self.clear = QtWidgets.QPushButton("Clear view")
		self.clear.clicked.connect(self.clearView)

		self.hkxToFbxGrp = QtWidgets.QGroupBox("HKX (32bit) => FBX")

		self.skeletonInput = inputBoxWithBrowse(label="skeleton.hkx", placeholderText="Locate skeleton.hkx file", defaultPath=os.path.join(rp, "skeleton.hkx"))
		self.hkxToFbxBtn = QtWidgets.QPushButton("Convert HKX to FBX")
		self.hkxToFbxBtn.clicked.connect(self.convertHkxToFBXAnimation)

		self.hkxToFbxLayout = QtWidgets.QVBoxLayout()
		self.hkxToFbxLayout.addWidget(self.skeletonInput)
		self.hkxToFbxLayout.addWidget(self.hkxToFbxBtn)

		self.hkxToFbxGrp.setLayout(self.hkxToFbxLayout)

		self.mainLayout.addWidget(self.viewlabel)
		self.mainLayout.addWidget(self.view)
		#self.mainLayout.addWidget(self.groupBox)
		self.mainLayout.addWidget(self.button)
		self.mainLayout.addWidget(self.getTxtButton)
		self.mainLayout.addWidget(self.remove)
		self.mainLayout.addWidget(self.clear)
		self.mainLayout.addWidget(self.hkxToFbxGrp)
		self.mainLayout.addWidget(self.pb)

		self.setCentralWidget(self.mainWidget)

		self.setWindowTitle("hkxpack GUI")
		if not os.path.exists(hkxCliJar):
			self.button.setEnabled(False)
			self.getTxtButton.setEnabled(False)

		if not os.path.exists(havokToFbx):
			self.hkxToFbxGrp.setEnabled(False)

		self.setStyleSheet(css)

	def fileDropped(self, l) -> None:
		for url in l:
			if os.path.exists(url):
				item = QtWidgets.QListWidgetItem(url, self.view)
				item.setStatusTip(url)

	def convertHkxToFBXAnimation(self) -> None:
		skeleton = self.skeletonInput.text()
		self.pb.setMaximum(self.view.count())
		self.pb.setValue(0)
		for i in range (self.view.count()):
			file = self.view.item(i).text()
			fileRaw, fileExtension = os.path.splitext(file)
			#fileExtension = file.split('.')[-1]
			print(file, fileRaw, fileExtension)

			if fileExtension in {".hkx", ".HKX"}:
				fileto = fileRaw+".fbx"
				print("Converting", file, "to", fileto)
				subprocess.call([havokToFbx, "-hk_skeleton", skeleton, "-hk_anim", file, "-fbx" , fileto])
			self.pb.setValue(i+1)
		print("Done")

	def convertXmlHkx (self) -> None:
		self.pb.setMaximum(self.view.count())
		self.pb.setValue(0)
		for i in range (self.view.count()):
			file = self.view.item(i).text()
			fileExtension = file.split(".")[-1]

			if fileExtension in {"hkx", "HKX"}:
				print(">>> Converting", file, "to xml")
				subprocess.call(["java", "-jar", hkxCliJar, "unpack", file])

			elif fileExtension in {"xml", "XML"}:
				print("<<< Converting", file, "to hkx")
				subprocess.call(["java", "-jar", hkxCliJar, "pack", file])

			else:
				print("File", file, "is not hkx or xml. Skipped.")

			self.pb.setValue(i+1)

	def generateRigTxt(self) -> None:
		self.pb.setMaximum(self.view.count())
		self.pb.setValue(0)
		for i in range (self.view.count()):
			file = self.view.item(i).text()
			fileExtension = file.split(".")[-1]

			#if the file is hkx, we need to convert it to xml first.
			if fileExtension in {"hkx", "HKX"}:
				print(">>> Converting", file, "to xml")
				subprocess.call(["java", "-jar", hkxCliJar, "unpack", file])
				file = file.replace(".hkx", ".xml").replace(".HKX", ".XML")

			#read xml and extract data
			print("Reading file...")
			with open(file, "r") as fileData:
				soup = BeautifulSoup(fileData.read(), "xml")

			skeleton = soup.find("hkparam", {"name":"bones"})
			bones = []
			for child in skeleton.contents:
				childSoup = BeautifulSoup(str(child), "xml")
				boneNameParam = childSoup.find("hkparam", {"name":"name"})
				if boneNameParam is not None:
					bone = str(boneNameParam).split('"name">')[1].split("</hkparam>")[0]
					bones.append(bone)

			#generate txt
			output = "[HAVOK SKELETON DEFINITION FILE]\n\n[BONES START]"
			for bone in bones:
				output += "\n"+str(bone)

			output += "\n[END]"

			with open(file.replace(".xml", ".txt").replace(".XML", ".TXT"), "w") as newFile:
				newFile.write(output)

			self.pb.setValue(i+1)

	def clearView(self) -> None:
		self.view.clear()

	def removeSelected(self) -> None:
		for item in self.view.selectedItems():
			self.view.takeItem(self.view.row(item))

def main() -> None:
	app = QtWidgets.QApplication(sys.argv)
	form = MainForm()
	form.show()
	app.exec_()

if __name__ == "__main__":
	main()
