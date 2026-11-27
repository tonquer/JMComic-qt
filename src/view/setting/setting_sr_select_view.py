from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QHeaderView, QTableWidgetItem, QAbstractItemView

from component.dialog.base_mask_dialog import BaseMaskDialog
from interface.ui_sr_select_widget import Ui_SrSelect
from tools.str import Str


class SettingSrSelectView(BaseMaskDialog, Ui_SrSelect):
    Close = Signal(str)

    def __init__(self, parent=None, curModelName=""):
        BaseMaskDialog.__init__(self, parent)
        Ui_SrSelect.__init__(self)
        self.setupUi(self.widget)
        self.curModelName = curModelName or ""

        # 根据父窗口尺寸合理放大弹窗，避免在小屏溢出、大屏过小
        target_w, target_h = 760, 560
        if parent is not None:
            pw, ph = parent.width(), parent.height()
            if pw > 0:
                target_w = max(560, min(target_w, pw - 64))
            if ph > 0:
                target_h = max(420, min(target_h, ph - 64))
        self.widget.setMinimumSize(target_w, target_h)
        self.widget.resize(target_w, target_h)

        self.saveButton.clicked.connect(self._ClickButton)
        self.closeButton.clicked.connect(self.close)
        self.tableWidget.cellDoubleClicked.connect(self._OnDoubleClick)
        self.searchEdit.textChanged.connect(self._FilterRows)
        self.algoFilter.currentIndexChanged.connect(self._FilterRows)

        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(34)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)
        self.tableWidget.setColumnWidth(0, 260)
        self.tableWidget.setColumnWidth(1, 140)
        self.tableWidget.setColumnWidth(2, 100)
        self.Init()

    def _OnDoubleClick(self, row, col):
        self._ClickButton()

    def _FilterRows(self):
        keyword = self.searchEdit.text().strip().lower()
        algo = self.algoFilter.currentText() if self.algoFilter.currentIndex() > 0 else ""
        for row in range(self.tableWidget.rowCount()):
            name_item = self.tableWidget.item(row, 0)
            algo_item = self.tableWidget.item(row, 1)
            cost_item = self.tableWidget.item(row, 2)
            desc_item = self.tableWidget.item(row, 3)
            row_algo = algo_item.text() if algo_item else ""
            if algo and row_algo != algo:
                self.tableWidget.setRowHidden(row, True)
                continue
            if keyword:
                haystack = " ".join([
                    name_item.text() if name_item else "",
                    row_algo,
                    cost_item.text() if cost_item else "",
                    desc_item.text() if desc_item else "",
                ]).lower()
                self.tableWidget.setRowHidden(row, keyword not in haystack)
            else:
                self.tableWidget.setRowHidden(row, False)

    def _ClickButton(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = []
        for index in selected:
            selectRows.append(index.row())
        if not selectRows:
            return
        row = selectRows[0]
        modelName1 = self.tableWidget.item(row, 0).text()
        modelName2 = self.tableWidget.item(row, 1).text().replace("-", "")
        modelName = "MODEL_" + modelName2.upper() + "_" + modelName1.upper()
        self.Close.emit(modelName)
        self.close()

    def Init(self):
        recommended = Str.GetStr(Str.Recommended)
        AllModelNames = [
            ("CUNET_UP1X_DENOISE0X", "Waifu2x", "", "100%"),
            ("CUNET_UP1X_DENOISE1X", "Waifu2x", "", "110%"),
            ("CUNET_UP1X_DENOISE2X", "Waifu2x", "", "110%"),
            ("CUNET_UP1X_DENOISE3X", "Waifu2x", "", "110%"),
            ("CUNET_UP2X", "Waifu2x", "", "300%"),
            ("CUNET_UP2X_DENOISE0X", "Waifu2x", "", "310%"),
            ("CUNET_UP2X_DENOISE1X", "Waifu2x", "", "310%"),
            ("CUNET_UP2X_DENOISE2X", "Waifu2x", "", "310%"),
            ("CUNET_UP2X_DENOISE3X", "Waifu2x", recommended, "310%"),
            ("ANIME_UP2X", "Waifu2x", "", "200%"),
            ("ANIME_UP2X_DENOISE0X", "Waifu2x", "", "210%"),
            ("ANIME_UP2X_DENOISE1X", "Waifu2x", "", "210%"),
            ("ANIME_UP2X_DENOISE2X", "Waifu2x", "", "210%"),
            ("ANIME_UP2X_DENOISE3X", "Waifu2x", recommended, "210%"),
            ("PHOTO_UP2X", "Waifu2x", "", "180%"),
            ("PHOTO_UP2X_DENOISE0X", "Waifu2x", "", "200%"),
            ("PHOTO_UP2X_DENOISE1X", "Waifu2x", "", "200%"),
            ("PHOTO_UP2X_DENOISE2X", "Waifu2x", "", "200%"),
            ("PHOTO_UP2X_DENOISE3X", "Waifu2x", recommended, "200%"),
            ("PRO_UP2X", "Real-CUGAN", "", "350%"),
            ("PRO_UP2X_CONSERVATIVE", "Real-CUGAN", "", "350%"),
            ("PRO_UP2X_DENOISE3X", "Real-CUGAN", recommended, "350%"),
            ("PRO_UP3X", "Real-CUGAN", "", "500%"),
            ("PRO_UP3X_CONSERVATIVE", "Real-CUGAN", "", "500%"),
            ("PRO_UP3X_DENOISE3X", "Real-CUGAN", "", "500%"),
            ("SE_UP2X", "Real-CUGAN", "", "300%"),
            ("SE_UP2X_CONSERVATIVE", "Real-CUGAN", "", "300%"),
            ("SE_UP2X_DENOISE1X", "Real-CUGAN", "", "300%"),
            ("SE_UP2X_DENOISE2X", "Real-CUGAN", "", "300%"),
            ("SE_UP2X_DENOISE3X", "Real-CUGAN", recommended, "300%"),
            ("SE_UP3X", "Real-CUGAN", "", "500%"),
            ("SE_UP3X_CONSERVATIVE", "Real-CUGAN", "", "500%"),
            ("SE_UP3X_DENOISE3X", "Real-CUGAN", "", "500%"),
            ("SE_UP4X", "Real-CUGAN", "", "400%"),
            ("SE_UP4X_CONSERVATIVE", "Real-CUGAN", "", "400%"),
            ("SE_UP4X_DENOISE3X", "Real-CUGAN", "", "400%"),
            ("ANIMAVIDEOV3_UP2X", "Real-ESRGAN", recommended, "200%"),
            ("ANIMAVIDEOV3_UP3X", "Real-ESRGAN", "", "300%"),
            ("ANIMAVIDEOV3_UP4X", "Real-ESRGAN", "", "400%"),
            ("X4PLUS_UP4X", "Real-ESRGAN", "", "600%"),
            ("X4PLUSANIME_UP4X", "Real-ESRGAN", "", "400%"),
        ]
        was_sorting = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        cur_upper = self.curModelName.upper()
        matched_row = -1
        for v in AllModelNames:
            rowCont = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowCont)
            nameItem = QTableWidgetItem(v[0])
            algoItem = QTableWidgetItem(v[1])
            algoItem.setTextAlignment(Qt.AlignCenter)
            costItem = QTableWidgetItem(v[3])
            costItem.setTextAlignment(Qt.AlignCenter)
            descItem = QTableWidgetItem(v[2])
            descItem.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(rowCont, 0, nameItem)
            self.tableWidget.setItem(rowCont, 1, algoItem)
            self.tableWidget.setItem(rowCont, 2, costItem)
            self.tableWidget.setItem(rowCont, 3, descItem)
            full_name = "MODEL_" + v[1].replace("-", "").upper() + "_" + v[0].upper()
            if cur_upper and full_name == cur_upper:
                matched_row = rowCont
        self.tableWidget.setSortingEnabled(was_sorting)

        if matched_row >= 0:
            self.tableWidget.selectRow(matched_row)
            self.tableWidget.scrollToItem(
                self.tableWidget.item(matched_row, 0),
                QAbstractItemView.PositionAtCenter,
            )
