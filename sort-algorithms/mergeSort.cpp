#include <vector>
#include <oneapi/tbb/parallel_for.h>
#include <oneapi/tbb/parallel_reduce.h>
#include <oneapi/tbb/blocked_range.h>

std::vector<int> merge(std::vector<int> vec1, std::vector<int> vec2) {
    std::vector<int> merged_vec;

    while (vec1.size() > 0 && vec2.size() > 0) {
        if (vec1[0] <= vec2[0]) {
            merged_vec.push_back(vec1[0]);
            vec1.erase(vec1.begin());
        } else {
            merged_vec.push_back(vec2[0]);
            vec2.erase(vec2.begin());
        }
    }

    if (vec1.size() > 0) {
        for (size_t i = 0; i < vec1.size(); i++) {
            merged_vec.push_back(vec1[i]);
        }
    }
    if (vec2.size() > 0) {
        for (size_t i = 0; i < vec2.size(); i++) {
            merged_vec.push_back(vec2[i]);
        }
    }

    return merged_vec;
}

std::vector<int> mergeSort(std::vector<int> vec, size_t size) {
    std::vector<std::vector<int>> mapped_vec(size);

    oneapi::tbb::parallel_for(
        oneapi::tbb::blocked_range<int>(0, size),
        [&](const oneapi::tbb::blocked_range<int> r) {
            for (int i = r.begin(); i < r.end(); i++) {
                std::vector<int> num_in_array { vec[i] };
                mapped_vec[i] = num_in_array;
            }
        }
    );

    std::vector<int> sorted = oneapi::tbb::parallel_reduce(
        oneapi::tbb::blocked_range<int>(0, size),
        std::vector<int>(),
        [&](const oneapi::tbb::blocked_range<int> r, std::vector<int> sorted) -> std::vector<int> {
            for (int i = r.begin(); i < r.end(); i++) {
                sorted = merge(sorted, mapped_vec[i]);
            }
            return sorted;
        },
        [](std::vector<int> a, std::vector<int> b) -> std::vector<int> {
            return merge(a, b);
        }
    );

    return sorted;
}