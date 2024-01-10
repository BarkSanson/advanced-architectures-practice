#include <iostream>
#include <vector>
#include <oneapi/tbb/parallel_for.h>
#include <tbb/tbb.h>

#include "mergeSort.hpp"
#include "quickSort.hpp"

void printVector(std::vector<int> vec) {
    for (size_t i = 0; i < vec.size(); i++) {
        std::cout << vec[i] << " ";
    }
    std::cout << std::endl;
}

int main() {
    size_t size = 20;
    std::vector<int> to_sort(size);

    oneapi::tbb::parallel_for(
        oneapi::tbb::blocked_range<int>(0, size),
        [&](const oneapi::tbb::blocked_range<int> r) {
            for (int i = r.begin(); i < r.end(); i++) {
                to_sort[i] = rand() % 100;
            }
        }
    );

    std::cout << "****MERGESORT****" << std::endl;

    std::cout << "Unsorted: ";
    printVector(to_sort);

    tbb::tick_count t0 = tbb::tick_count::now();
    auto result_merge = mergeSort(to_sort, size);
    tbb::tick_count t1 = tbb::tick_count::now();

    std::cout << "Time: " << (t1 - t0).seconds() << std::endl;
    std::cout << "Sorted: ";
    printVector(result_merge);

    std::cout << "****QUICKSORT****" << std::endl;
    std::cout << "Unsorted: ";
    printVector(to_sort);

    int high = size - 1;

    t0 = tbb::tick_count::now();
    quickSort(to_sort, 0, high);
    t1 = tbb::tick_count::now();

    std::cout << "Time: " << (t1 - t0).seconds() << std::endl;
    std::cout << "Sorted: ";
    printVector(to_sort);
}