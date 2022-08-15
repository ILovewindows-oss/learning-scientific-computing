#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

extern void step(float* r, const float* d, int n);

float next_float()
{
    static std::random_device rd;
    static std::default_random_engine e(rd());
    static std::uniform_real_distribution<float> floats(0.0, 1.0);
    return floats(e);
}

int main()
{
    constexpr int n = 4000;
    std::vector<float> r(n*n);
    std::vector<float> d(n*n);
    std::generate(d.begin(), d.end(), next_float);

    const auto time_start = std::chrono::high_resolution_clock::now();
    step(r.data(), d.data(), n);
    const auto time_end = std::chrono::high_resolution_clock::now();
    const std::chrono::duration<float> delta_seconds = time_end - time_start;
    std::cout << std::setprecision(7) << delta_seconds.count() << std::endl;
}