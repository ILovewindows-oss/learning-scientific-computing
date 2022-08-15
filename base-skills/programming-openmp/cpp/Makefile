CXX      := g++
CXXFLAGS := -g -O3 -march=native -std=c++17

v0: main.cpp step_v0.cpp
	$(CXX) $(CXXFLAGS) -fopenmp main.cpp step_v0.cpp -o program_v0

v1: main.cpp step_v1.cpp
	$(CXX) $(CXXFLAGS) -fopenmp main.cpp step_v1.cpp -o program_v1

v2: main.cpp step_v2.cpp
	$(CXX) $(CXXFLAGS) -fopenmp main.cpp step_v2.cpp -o program_v2

clean:
	rm -rf *.s main_v*
