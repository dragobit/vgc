// Copyright 2022 The VGC Developers
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

#ifndef VGC_WIDGETS_LOGCATEGORIES_H
#define VGC_WIDGETS_LOGCATEGORIES_H

#include <vgc/core/logging.h>
#include <vgc/widgets/api.h>

namespace vgc::widgets {

VGC_DECLARE_LOG_CATEGORY(VGC_WIDGETS_API, LogVgcWidgets, Debug)
VGC_DECLARE_LOG_CATEGORY(VGC_WIDGETS_API, LogVgcWidgetsFiles, Info)
VGC_DECLARE_LOG_CATEGORY(VGC_WIDGETS_API, LogVgcWidgetsFonts, Info)
VGC_DECLARE_LOG_CATEGORY(VGC_WIDGETS_API, LogVgcWidgetsSplitter, Info)

} // namespace vgc::widgets

#endif // VGC_WIDGETS_LOGCATEGORIES_H
