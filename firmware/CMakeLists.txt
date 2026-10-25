cmake_minimum_required(VERSION 3.20)

set(CMAKE_TOOLCHAIN_FILE "${CMAKE_CURRENT_SOURCE_DIR}/cmake/arm-none-eabi.cmake")

project(nipkow-fw C ASM)

set(MCU_FLAGS
    -mcpu=cortex-m4
    -mthumb
    -mfpu=fpv4-sp-d16
    -mfloat-abi=hard
)

add_compile_options(${MCU_FLAGS} -Wall -Wextra -Wno-unused-parameter -ffunction-sections -fdata-sections)
add_compile_definitions(USE_HAL_DRIVER STM32F407xx HSE_VALUE=8000000)

include_directories(
    Core/Inc
    third_party/STM32F4xx_HAL_Driver/Inc
    third_party/CMSIS/Device/ST/STM32F4xx/Include
    third_party/CMSIS/Include
)

file(GLOB_RECURSE HAL_SOURCES third_party/STM32F4xx_HAL_Driver/Src/*.c)
# 模板文件（timebase/msp）不能参与编译，否则重复定义
list(FILTER HAL_SOURCES EXCLUDE REGEX "_template\\.c$")
file(GLOB APP_SOURCES Core/Src/*.c)

add_executable(${PROJECT_NAME}
    ${APP_SOURCES}
    ${HAL_SOURCES}
    Core/Startup/startup_stm32f407xx.s
)

target_link_options(${PROJECT_NAME} PRIVATE
    ${MCU_FLAGS}
    -T${CMAKE_CURRENT_SOURCE_DIR}/STM32F407VETx_FLASH.ld
    --specs=nano.specs
    --specs=nosys.specs
    -Wl,--gc-sections
    -Wl,-Map=${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.map
)

set_target_properties(${PROJECT_NAME} PROPERTIES SUFFIX ".elf")

# 生成 .bin / .hex
add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} -O binary $<TARGET_FILE:${PROJECT_NAME}> ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.bin
    COMMAND ${CMAKE_OBJCOPY} -O ihex   $<TARGET_FILE:${PROJECT_NAME}> ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.hex
    COMMAND ${CMAKE_SIZE} $<TARGET_FILE:${PROJECT_NAME}>
    COMMENT "objcopy -> bin/hex"
)
