// Copyright 2018 The VGC Developers
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

#ifndef VGC_DOM_EXCEPTIONS_H
#define VGC_DOM_EXCEPTIONS_H

#include <vgc/core/exceptions.h>
#include <vgc/dom/api.h>

namespace vgc {
namespace dom {

class Node;
class Document;

/// \class vgc::dom::LogicError
/// \brief Raised when there is a logic error detected in vgc::dom.
///
/// This exception is raised whenever there is a logic error detected in
/// vgc::dom. This is the base class for all logic error exception classes in
/// vgc::dom.
///
/// The class hierarchy for vgc::dom exceptions is:
///
/// \verbatim
/// LogicError
///  +-- NotAliveError
///  +-- WrongDocumentError
///  +-- HierarchyRequestError
///       +-- WrongChildTypeError
///       +-- SecondRootElementError
/// \endverbatim
///
class VGC_DOM_API LogicError : public core::LogicError {
public:
    /// Constructs a LogicError with the given \p reason.
    ///
    explicit LogicError(const std::string& reason) : core::LogicError(reason) {}
};

/// \class vgc::dom::NotAliveError
/// \brief Raised when attempting to use a Node which is not alive.
///
/// This exception is raised whenever trying to perform an operation
/// involving a Node that has already been destroyed.
///
/// \sa Node::isAlive() and Node::destroy().
///
class VGC_DOM_API NotAliveError : public LogicError {
public:
    /// Constructs a NotAliveError informing that the Node \p node is not alive.
    ///
    NotAliveError(const Node* node);
};

/// \class vgc::dom::WrongDocumentError
/// \brief Raised when two nodes do not belong to the same document
///        but are supposed to.
///
/// This exception is raised in Node::appendChild() and Node::replaceChild() if
/// the node that you are trying to append or replace with belongs to a
/// different Document that its new parent.
///
/// \sa Node::appendChild() and Node::replaceChild().
///
class VGC_DOM_API WrongDocumentError : public LogicError {
public:
    /// Constructs a WrongDocumentError informing that the Node \p n1 and the
    /// Node \p n2 do not belong to the same Document.
    ///
    WrongDocumentError(const Node* n1, const Node* n2);
};

/// \class vgc::dom::HierarchyRequestError
/// \brief Raised when attempting to insert a Node somewhere it doesn't belong.
///
/// This exception is raised whenever a client requests to insert a Node at a
/// position where it cannot be inserted without breaking one of these two
/// invariants:
///
/// 1. A Node only has children of these allowed types:
///    - Document: allowed children are Element (at most one)
///    - Element: allowed children are Element
///
/// 2. A Node is never a child of itself or of any of its descendants (in other
///    words, the document has no cycle).
///
/// In the first case, the exception WrongChildTypeError or
/// SecondRootElementError is raised, while in the second case the exception
/// ChildCycleError is raised, all of which derive from HierarchyRequestError.
///
/// XXX TODO: Implement ChildCycleError
///
/// \sa Node::appendChild() and Node::replaceChild().
///
class VGC_DOM_API HierarchyRequestError : public LogicError {
public:
    /// Constructs a HierarchyRequestError with the given \p reason.
    ///
    HierarchyRequestError(const std::string& reason) : LogicError(reason) {}
};

/// \class vgc::dom::WrongChildTypeError
/// \brief Raised when requested to insert a child Node with incompatible
///        NodeType.
///
/// This exception is raised whenever a client requests to insert a child Node
/// whose type is not one of the allowed type. Here is the list of allowed type
/// according to the type of the parent Node:
/// - Document: allowed children are Element (at most one)
/// - Element: allowed children are Element
///
/// \sa Node::appendChild() and Node::replaceChild().
///
class VGC_DOM_API WrongChildTypeError : public HierarchyRequestError {
public:
    /// Constructs a WrongChildTypeError informing that \p parent cannot
    /// have \p child as its child due to incompatible node types.
    ///
    WrongChildTypeError(const Node* parent, const Node* child);
};

/// \class vgc::dom::SecondRootElementError
/// \brief Raised when requested to insert a second child Element to a Document.
///
/// Document nodes are only allowed to have at most one Element child node,
/// called its root element (see rootElement()). This exception is raised
/// whenever a requested operation would result in a second root element be
/// inserted as a child of the Document node.
///
class VGC_DOM_API SecondRootElementError : public HierarchyRequestError {
public:
    /// Constructs a SecondRootElementError informing that the Document \p node
    /// cannot have a second root element.
    ///
    SecondRootElementError(const Document* document);
};

} // namespace dom
} // namespace vgc

#endif // VGC_DOM_EXCEPTIONS_H
