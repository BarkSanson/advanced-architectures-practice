#include <iostream>
#include <vector>
#include <oneapi/tbb/parallel_for.h>

#include "./mergeSort.hpp"

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

    std::cout << "****MERGE SORT****" << std::endl;

    std::cout << "Unsorted: ";
    printVector(to_sort);

    tbb::tick_count t0 = tbb::tick_count::now();
    auto result = mergeSort(to_sort, size);
    tbb::tick_count t1 = tbb::tick_count::now();

    std::cout << "Time: " << (t1 - t0).seconds() << std::endl;
    std::cout << "Sorted: ";
    printVector(result);
}