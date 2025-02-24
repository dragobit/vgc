// Copyright 2021 The VGC Developers
// See the COPYRIGHT file at the top-level directory of this distribution
// and at https://github.com/vgc/vgc/blob/master/COPYRIGHT
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <vgc/widgets/dialog.h>

namespace vgc::widgets {

Dialog::Dialog(QWidget* parent)
    : QDialog(parent)
    , isGeometrySaved_(false) {

    connect(this, &QDialog::finished, this, &Dialog::onFinished_);
}

void Dialog::closeEvent(QCloseEvent* event) {
    saveGeometry_();
    QDialog::closeEvent(event);
}

void Dialog::hideEvent(QHideEvent* event) {
    saveGeometry_();
    QDialog::hideEvent(event);
}

void Dialog::showEvent(QShowEvent* event) {
    restoreGeometry_();
    QDialog::showEvent(event);
}

void Dialog::onFinished_(int) {
    saveGeometry_();
}

void Dialog::saveGeometry_() {
    isGeometrySaved_ = true;
    savedGeometry_ = geometry();
}

void Dialog::restoreGeometry_() {
    if (isGeometrySaved_)
        setGeometry(savedGeometry_);
}

} // namespace vgc::widgets
