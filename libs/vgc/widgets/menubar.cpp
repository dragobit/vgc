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

#include <vgc/widgets/menubar.h>

#include <QPaintEvent>
#include <QPainter>

namespace vgc::widgets {

MenuBar::MenuBar(QWidget* parent)
    : QMenuBar(parent)
    , activeBorderBottomColor_(Qt::transparent) {
}

MenuBar::~MenuBar() {
}

QColor MenuBar::activeBorderBottomColor() const {
    return activeBorderBottomColor_;
}

void MenuBar::setActiveBorderBottomColor(QColor c) {
    activeBorderBottomColor_ = c;
}

void MenuBar::paintEvent(QPaintEvent* e) {
    if (e->rect().height() < height()) {
        // By default, the border-bottom of the QMenuBar is not included in
        // the redrawn area when hovering on a menu item. Since we do desire
        // to change the color of the border-bottom in this case, we need to
        // extend the redrawn area a little.
        update(e->rect().x(), e->rect().y(), e->rect().width(), height());
    }
    else {
        // Draw the QMenuBar as usual
        QMenuBar::paintEvent(e);

        // Paint over the border-bottom of the QMenuBar below the active item
        QAction* action = activeAction();
        if (action) {
            QPainter p(this);
            QRect itemRect = actionGeometry(action);
            QRect menuRect = rect();
            QRect activeBorderBottomRect(
                itemRect.x(),                           // x
                itemRect.height(),                      // y
                itemRect.width(),                       // width
                menuRect.height() - itemRect.height()); // height
            p.fillRect(activeBorderBottomRect, activeBorderBottomColor());
        }
    }
}

} // namespace vgc::widgets
