vgc_add_library(geometry
    THIRD_DEPENDENCIES
        libtess2

    VGC_DEPENDENCIES
        core

    HEADER_FILES
        api.h
        bezier.h
        bezierspline.h
        bezierspline1d.h
        bezierspline2d.h
        camera2d.h
        catmullrom.h
        curve.h
        curvecommand.h
        curves2d.h
        logcategories.h
        mat.h
        mat2d.h
        mat2f.h
        mat3d.h
        mat3f.h
        mat4d.h
        mat4f.h
        range1d.h
        range1f.h
        rect2d.h
        rect2f.h
        stride.h
        triangle2d.h
        triangle2f.h
        vec.h
        vec2d.h
        vec2f.h
        vec3d.h
        vec3f.h
        vec4d.h
        vec4f.h

    CPP_FILES
        camera2d.cpp
        curve.cpp
        curves2d.cpp
        logcategories.cpp
        mat2d.cpp
        mat2f.cpp
        mat3d.cpp
        mat3f.cpp
        mat4d.cpp
        mat4f.cpp
        range1d.cpp
        range1f.cpp
        rect2d.cpp
        rect2f.cpp
        triangle2d.cpp
        triangle2f.cpp
        vec2d.cpp
        vec2f.cpp
        vec3d.cpp
        vec3f.cpp
        vec4d.cpp
        vec4f.cpp

    NATVIS_FILES
        tools/vgcgeometry.natvis
)

add_subdirectory(wraps)
add_subdirectory(tests)
