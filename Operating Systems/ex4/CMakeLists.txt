cmake_minimum_required(VERSION 3.17)
project(ex4 C)

set(CMAKE_C_STANDARD 90)

add_executable(ex4 ex4_client.c ex4_srv.c)