# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.17

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = "/mnt/c/Studies/2nd year/CS/milestone2"

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = "/mnt/c/Studies/2nd year/CS/milestone2/cmake-build-debug"

# Include any dependencies generated for this target.
include CMakeFiles/milestone2.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/milestone2.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/milestone2.dir/flags.make

CMakeFiles/milestone2.dir/MainTrain.cpp.o: CMakeFiles/milestone2.dir/flags.make
CMakeFiles/milestone2.dir/MainTrain.cpp.o: ../MainTrain.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/mnt/c/Studies/2nd year/CS/milestone2/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/milestone2.dir/MainTrain.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/milestone2.dir/MainTrain.cpp.o -c "/mnt/c/Studies/2nd year/CS/milestone2/MainTrain.cpp"

CMakeFiles/milestone2.dir/MainTrain.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/milestone2.dir/MainTrain.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "/mnt/c/Studies/2nd year/CS/milestone2/MainTrain.cpp" > CMakeFiles/milestone2.dir/MainTrain.cpp.i

CMakeFiles/milestone2.dir/MainTrain.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/milestone2.dir/MainTrain.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "/mnt/c/Studies/2nd year/CS/milestone2/MainTrain.cpp" -o CMakeFiles/milestone2.dir/MainTrain.cpp.s

CMakeFiles/milestone2.dir/anomaly_detection_util.cpp.o: CMakeFiles/milestone2.dir/flags.make
CMakeFiles/milestone2.dir/anomaly_detection_util.cpp.o: ../anomaly_detection_util.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/mnt/c/Studies/2nd year/CS/milestone2/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/milestone2.dir/anomaly_detection_util.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/milestone2.dir/anomaly_detection_util.cpp.o -c "/mnt/c/Studies/2nd year/CS/milestone2/anomaly_detection_util.cpp"

CMakeFiles/milestone2.dir/anomaly_detection_util.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/milestone2.dir/anomaly_detection_util.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "/mnt/c/Studies/2nd year/CS/milestone2/anomaly_detection_util.cpp" > CMakeFiles/milestone2.dir/anomaly_detection_util.cpp.i

CMakeFiles/milestone2.dir/anomaly_detection_util.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/milestone2.dir/anomaly_detection_util.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "/mnt/c/Studies/2nd year/CS/milestone2/anomaly_detection_util.cpp" -o CMakeFiles/milestone2.dir/anomaly_detection_util.cpp.s

CMakeFiles/milestone2.dir/timeseries.cpp.o: CMakeFiles/milestone2.dir/flags.make
CMakeFiles/milestone2.dir/timeseries.cpp.o: ../timeseries.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/mnt/c/Studies/2nd year/CS/milestone2/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/milestone2.dir/timeseries.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/milestone2.dir/timeseries.cpp.o -c "/mnt/c/Studies/2nd year/CS/milestone2/timeseries.cpp"

CMakeFiles/milestone2.dir/timeseries.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/milestone2.dir/timeseries.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "/mnt/c/Studies/2nd year/CS/milestone2/timeseries.cpp" > CMakeFiles/milestone2.dir/timeseries.cpp.i

CMakeFiles/milestone2.dir/timeseries.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/milestone2.dir/timeseries.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "/mnt/c/Studies/2nd year/CS/milestone2/timeseries.cpp" -o CMakeFiles/milestone2.dir/timeseries.cpp.s

CMakeFiles/milestone2.dir/SimpleAnomalyDetector.cpp.o: CMakeFiles/milestone2.dir/flags.make
CMakeFiles/milestone2.dir/SimpleAnomalyDetector.cpp.o: ../SimpleAnomalyDetector.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/mnt/c/Studies/2nd year/CS/milestone2/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object CMakeFiles/milestone2.dir/SimpleAnomalyDetector.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/milestone2.dir/SimpleAnomalyDetector.cpp.o -c "/mnt/c/Studies/2nd year/CS/milestone2/SimpleAnomalyDetector.cpp"

CMakeFiles/milestone2.dir/SimpleAnomalyDetector.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/milestone2.dir/SimpleAnomalyDetector.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "/mnt/c/Studies/2nd year/CS/milestone2/SimpleAnomalyDetector.cpp" > CMakeFiles/milestone2.dir/SimpleAnomalyDetector.cpp.i

CMakeFiles/milestone2.dir/SimpleAnomalyDetector.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/milestone2.dir/SimpleAnomalyDetector.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "/mnt/c/Studies/2nd year/CS/milestone2/SimpleAnomalyDetector.cpp" -o CMakeFiles/milestone2.dir/SimpleAnomalyDetector.cpp.s

CMakeFiles/milestone2.dir/HybridAnomalyDetector.cpp.o: CMakeFiles/milestone2.dir/flags.make
CMakeFiles/milestone2.dir/HybridAnomalyDetector.cpp.o: ../HybridAnomalyDetector.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/mnt/c/Studies/2nd year/CS/milestone2/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_5) "Building CXX object CMakeFiles/milestone2.dir/HybridAnomalyDetector.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/milestone2.dir/HybridAnomalyDetector.cpp.o -c "/mnt/c/Studies/2nd year/CS/milestone2/HybridAnomalyDetector.cpp"

CMakeFiles/milestone2.dir/HybridAnomalyDetector.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/milestone2.dir/HybridAnomalyDetector.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "/mnt/c/Studies/2nd year/CS/milestone2/HybridAnomalyDetector.cpp" > CMakeFiles/milestone2.dir/HybridAnomalyDetector.cpp.i

CMakeFiles/milestone2.dir/HybridAnomalyDetector.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/milestone2.dir/HybridAnomalyDetector.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "/mnt/c/Studies/2nd year/CS/milestone2/HybridAnomalyDetector.cpp" -o CMakeFiles/milestone2.dir/HybridAnomalyDetector.cpp.s

CMakeFiles/milestone2.dir/minCircle.cpp.o: CMakeFiles/milestone2.dir/flags.make
CMakeFiles/milestone2.dir/minCircle.cpp.o: ../minCircle.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/mnt/c/Studies/2nd year/CS/milestone2/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_6) "Building CXX object CMakeFiles/milestone2.dir/minCircle.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/milestone2.dir/minCircle.cpp.o -c "/mnt/c/Studies/2nd year/CS/milestone2/minCircle.cpp"

CMakeFiles/milestone2.dir/minCircle.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/milestone2.dir/minCircle.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "/mnt/c/Studies/2nd year/CS/milestone2/minCircle.cpp" > CMakeFiles/milestone2.dir/minCircle.cpp.i

CMakeFiles/milestone2.dir/minCircle.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/milestone2.dir/minCircle.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "/mnt/c/Studies/2nd year/CS/milestone2/minCircle.cpp" -o CMakeFiles/milestone2.dir/minCircle.cpp.s

CMakeFiles/milestone2.dir/CLI.cpp.o: CMakeFiles/milestone2.dir/flags.make
CMakeFiles/milestone2.dir/CLI.cpp.o: ../CLI.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/mnt/c/Studies/2nd year/CS/milestone2/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_7) "Building CXX object CMakeFiles/milestone2.dir/CLI.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/milestone2.dir/CLI.cpp.o -c "/mnt/c/Studies/2nd year/CS/milestone2/CLI.cpp"

CMakeFiles/milestone2.dir/CLI.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/milestone2.dir/CLI.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "/mnt/c/Studies/2nd year/CS/milestone2/CLI.cpp" > CMakeFiles/milestone2.dir/CLI.cpp.i

CMakeFiles/milestone2.dir/CLI.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/milestone2.dir/CLI.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "/mnt/c/Studies/2nd year/CS/milestone2/CLI.cpp" -o CMakeFiles/milestone2.dir/CLI.cpp.s

CMakeFiles/milestone2.dir/Server.cpp.o: CMakeFiles/milestone2.dir/flags.make
CMakeFiles/milestone2.dir/Server.cpp.o: ../Server.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/mnt/c/Studies/2nd year/CS/milestone2/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_8) "Building CXX object CMakeFiles/milestone2.dir/Server.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/milestone2.dir/Server.cpp.o -c "/mnt/c/Studies/2nd year/CS/milestone2/Server.cpp"

CMakeFiles/milestone2.dir/Server.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/milestone2.dir/Server.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "/mnt/c/Studies/2nd year/CS/milestone2/Server.cpp" > CMakeFiles/milestone2.dir/Server.cpp.i

CMakeFiles/milestone2.dir/Server.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/milestone2.dir/Server.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "/mnt/c/Studies/2nd year/CS/milestone2/Server.cpp" -o CMakeFiles/milestone2.dir/Server.cpp.s

# Object files for target milestone2
milestone2_OBJECTS = \
"CMakeFiles/milestone2.dir/MainTrain.cpp.o" \
"CMakeFiles/milestone2.dir/anomaly_detection_util.cpp.o" \
"CMakeFiles/milestone2.dir/timeseries.cpp.o" \
"CMakeFiles/milestone2.dir/SimpleAnomalyDetector.cpp.o" \
"CMakeFiles/milestone2.dir/HybridAnomalyDetector.cpp.o" \
"CMakeFiles/milestone2.dir/minCircle.cpp.o" \
"CMakeFiles/milestone2.dir/CLI.cpp.o" \
"CMakeFiles/milestone2.dir/Server.cpp.o"

# External object files for target milestone2
milestone2_EXTERNAL_OBJECTS =

milestone2: CMakeFiles/milestone2.dir/MainTrain.cpp.o
milestone2: CMakeFiles/milestone2.dir/anomaly_detection_util.cpp.o
milestone2: CMakeFiles/milestone2.dir/timeseries.cpp.o
milestone2: CMakeFiles/milestone2.dir/SimpleAnomalyDetector.cpp.o
milestone2: CMakeFiles/milestone2.dir/HybridAnomalyDetector.cpp.o
milestone2: CMakeFiles/milestone2.dir/minCircle.cpp.o
milestone2: CMakeFiles/milestone2.dir/CLI.cpp.o
milestone2: CMakeFiles/milestone2.dir/Server.cpp.o
milestone2: CMakeFiles/milestone2.dir/build.make
milestone2: CMakeFiles/milestone2.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir="/mnt/c/Studies/2nd year/CS/milestone2/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_9) "Linking CXX executable milestone2"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/milestone2.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/milestone2.dir/build: milestone2

.PHONY : CMakeFiles/milestone2.dir/build

CMakeFiles/milestone2.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/milestone2.dir/cmake_clean.cmake
.PHONY : CMakeFiles/milestone2.dir/clean

CMakeFiles/milestone2.dir/depend:
	cd "/mnt/c/Studies/2nd year/CS/milestone2/cmake-build-debug" && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" "/mnt/c/Studies/2nd year/CS/milestone2" "/mnt/c/Studies/2nd year/CS/milestone2" "/mnt/c/Studies/2nd year/CS/milestone2/cmake-build-debug" "/mnt/c/Studies/2nd year/CS/milestone2/cmake-build-debug" "/mnt/c/Studies/2nd year/CS/milestone2/cmake-build-debug/CMakeFiles/milestone2.dir/DependInfo.cmake" --color=$(COLOR)
.PHONY : CMakeFiles/milestone2.dir/depend
