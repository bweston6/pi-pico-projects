cmake_minimum_required(VERSION 3.13)

include($ENV{PICO_SDK_PATH}/pico_sdk_init.cmake)

project(wifi-test C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()

# adding executables
add_executable(wifi-test wifi-test.c)
pico_add_extra_outputs(wifi-test)

# link libraries
target_link_libraries(wifi-test pico_stdlib pico_cyw43_arch_lwip_threadsafe_background)

# include headers
target_include_directories(wifi-test PRIVATE ${CMAKE_CURRENT_LIST_DIR}/lib)

# enable USB and diable UART output
pico_enable_stdio_usb(wifi-test 1)
pico_enable_stdio_uart(wifi-test 0)
