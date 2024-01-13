#include <iostream>
#include <vector>
#include <oneapi/tbb/parallel_invoke.h>
#include <oneapi/tbb/parallel_for.h>
#include <oneapi/tbb/parallel_scan.h>

#include "quickSort.hpp"

int partition(std::vector<int>& vec, int low, int high) {
    std::vector<int> to_sort(vec.begin() + low, vec.begin() + high + 1);

    // Take last element as pivot
    int pivot = to_sort[to_sort.size() - 1];

    // Map numbers to whether they are less than the pivot
    std::vector<int> is_less_than_pivot(high - low + 1);
    oneapi::tbb::parallel_for(
        oneapi::tbb::blocked_range<int>(0, to_sort.size()),
        [&](const oneapi::tbb::blocked_range<int> r) {
            for (int i = r.begin(); i < r.end(); i++) {
                is_less_than_pivot[i] = to_sort[i] < pivot;
            }
        }
    );

    // Scan the numbers to find the index of the 1s
    std::vector<int> indices(high - low + 1);
    int less_than_pivot_count = oneapi::tbb::parallel_scan(
        oneapi::tbb::blocked_range<int>(0, indices.size()),
        0,
        [&](const oneapi::tbb::blocked_range<int> r, int last, bool is_final_scan) {
            int sum = last;
            for (int i = r.begin(); i < r.end(); i++) {
                if (is_less_than_pivot[i]) {
                    sum++;
                }
                if (is_final_scan) {
                    indices[i] = sum;
                }
            }
            return sum;
        },
        [](int left, int right) {
            return left + right;
        }
    );

    for (int i = 0; i < indices.size(); i++) {
        if (is_less_than_pivot[i]) {
            std::swap(to_sort[i], to_sort[indices[i] - 1]);
            std::swap(is_less_than_pivot[i], is_less_than_pivot[indices[i] - 1]);
        }
    } 

    std::swap(to_sort[less_than_pivot_count], to_sort[to_sort.size() - 1]);

    std::copy(to_sort.begin(), to_sort.end(), vec.begin() + low);

    return less_than_pivot_count + low;
}

void quickSort(std::vector<int>& vec, int low, int high) {
    if (low < high) {

        int i = partition(vec, low, high);

        oneapi::tbb::parallel_invoke(
            [&]() {
                quickSort(vec, low, i - 1);
            },
            [&]() {
                quickSort(vec, i + 1, high);
            }
        );
    }
}