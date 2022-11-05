cmake_minimum_required(VERSION 3.12)

include($ENV{PICO_SDK_PATH}/pico_sdk_init.cmake)
pico_sdk_init()

project(hello_serial)

# adding executables
add_executable(hello_serial hello-serial.c)
pico_add_extra_outputs(hello_serial)

# link libraries
target_link_libraries(hello_serial pico_stdlib)

# enable USB and diable UART output
pico_enable_stdio_usb(hello_serial 1)
pico_enable_stdio_uart(hello_serial 0)

# completion for YCM
SET(CMAKE_EXPORT_COMPILE_COMMANDS ON)

IF( EXISTS "${CMAKE_CURRENT_BINARY_DIR}/compile_commands.json" )
  EXECUTE_PROCESS( COMMAND ${CMAKE_COMMAND} -E copy_if_different
    ${CMAKE_CURRENT_BINARY_DIR}/compile_commands.json
    ${CMAKE_CURRENT_SOURCE_DIR}/compile_commands.json
  )
ENDIF()
