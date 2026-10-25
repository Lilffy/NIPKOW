set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)

# 优先使用 PATH 中的 arm-none-eabi-，否则用环境变量 ARM_GCC_DIR
if(DEFINED ENV{ARM_GCC_DIR})
    set(_TOOLCHAIN_PREFIX "$ENV{ARM_GCC_DIR}/bin/arm-none-eabi-")
else()
    set(_TOOLCHAIN_PREFIX "arm-none-eabi-")
endif()

set(CMAKE_C_COMPILER   "${_TOOLCHAIN_PREFIX}gcc")
set(CMAKE_ASM_COMPILER "${_TOOLCHAIN_PREFIX}gcc")
set(CMAKE_OBJCOPY      "${_TOOLCHAIN_PREFIX}objcopy")
set(CMAKE_SIZE         "${_TOOLCHAIN_PREFIX}size")
set(CMAKE_AR           "${_TOOLCHAIN_PREFIX}ar")
set(CMAKE_GDB          "${_TOOLCHAIN_PREFIX}gdb")

set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)
set(CMAKE_EXECUTABLE_SUFFIX ".elf")
