#include <iostream>
#include <vector>
#include <oneapi/tbb/parallel_invoke.h>
#include <oneapi/tbb/parallel_for.h>
#include <oneapi/tbb/parallel_scan.h>

#include "quickSort.hpp"

int partition(std::vector<int>& vec, int low, int high) {
    std::cout << "\nLow: " << low << " High:" << high << "\n";

    int pivot = vec[high];
    std::cout << "Pivot: " << pivot << "\n";

    std::cout << "High - low: " << high - low << "\n";

    std::vector<int> to_sort(vec.begin() + low, vec.begin() + high + 1);
    std::cout << "To sort: ";
    for (size_t i = 0; i < to_sort.size(); i++) {
        std::cout << to_sort[i] << " ";
    }
    std::cout << "\n";

    // Map numbers to whether they are less than the pivot
    std::vector<int> is_less_than_pivot(high - low + 1);
    oneapi::tbb::parallel_for(
        oneapi::tbb::blocked_range<int>(low, high + 1),
        [&](const oneapi::tbb::blocked_range<int> r) {
            for (int i = r.begin(); i < r.end(); i++) {
                std::cout << "Is " << vec[i] << " less than " << pivot << "?";
                //std::cout << "Comparing " << vec[i] << " to " << pivot << "\n";
                is_less_than_pivot[i - low] = vec[i] < pivot;
                std::cout << is_less_than_pivot[i - low] << "\n";
            }
        }
    );

    std::cout << "Is less than pivot: ";
    for (size_t i = 0; i < is_less_than_pivot.size(); i++) {
        std::cout << is_less_than_pivot[i] << " ";
    }
    std::cout << "\n";
    
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

    //std::cout << "Less than pivot count: " << less_than_pivot_count << "\n";

    //std::cout << "Indices: ";
    //for (size_t i = 0; i < indices.size(); i++) {
    //    std::cout << "Num: " << vec[i + low - 1] << "Is less: " << is_less_than_pivot[i] << "Index: " << indices[i] << " " << "\n";
    //}
    //std::cout << "\n";

    oneapi::tbb::parallel_for(
        oneapi::tbb::blocked_range<int>(0, high - low + 1),
        [&](const oneapi::tbb::blocked_range<int> r) {
            for (int i = r.begin(); i < r.end(); i++) {
                if (is_less_than_pivot[i]) {
                    //std::cout << "Swapping " << vec[i + low] << " and " << vec[indices[i] - 1 + low];
                    //std::cout << " at indices " << i + low << " and " << indices[i] - 1 + low << "\n";
                    std::swap(vec[i + low], vec[indices[i] - 1 + low]);
                }
            }
        }
    );

    std::cout << "Swapping: " << vec[less_than_pivot_count + low] << " " << vec[high] << "\n";
    std::swap(vec[less_than_pivot_count + low], vec[high]);

    std::cout << "Partitioned: ";
    for (size_t i = low; i <= high; i++) {
        std::cout << vec[i] << " ";
    }

    return less_than_pivot_count + low;
}

void quickSort(std::vector<int>& vec, int low, int high) {
    if (low < high) {

        int i = partition(vec, low, high);

        //std::cout << "i: " << i << "\n";
        //std::cout << "i - 1: " << i - 1 << "\n";
        //std::cout << "i + 1: " << i + 1 << "\n";

        quickSort(vec, low, i - 1);
        quickSort(vec, i + 1, high);
    }
}