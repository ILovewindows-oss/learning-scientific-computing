#include <limits>
#include <vector>

void step(float* r, const float* d, int n)
{
    std::vector<float> t(n*n);

    #pragma omp parallel for
    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            t[n*j + i] = d[n*i + j];
        }
    }

    #pragma omp parallel for
    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            float v = std::numeric_limits<float>::infinity();

            asm("# inner loop");
            for (int k = 0; k < n; ++k) 
            {
                float x = d[n*i + k];
                float y = t[n*k + j];
                float z = x + y;
                v = std::min(v, z);
            }

            r[n*i + j] = v;
        }
    }
}
