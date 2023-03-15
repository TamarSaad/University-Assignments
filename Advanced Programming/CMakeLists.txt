cmake_minimum_required(VERSION 3.17)
project(milestone2)

set(CMAKE_CXX_STANDARD 14)
find_package (Threads)

add_executable(milestone2 MainTrain.cpp minCircle.h anomaly_detection_util.cpp timeseries.cpp SimpleAnomalyDetector.cpp timeseries.h anomaly_detection_util.h SimpleAnomalyDetector.h
        AnomalyDetector.h HybridAnomalyDetector.h HybridAnomalyDetector.cpp minCircle.cpp commands.h CLI.cpp CLI.h Server.cpp Server.h)
target_link_libraries (milestone2 ${CMAKE_THREAD_LIBS_INIT})