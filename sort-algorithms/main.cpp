#include <iostream>
#include <vector>
#include <oneapi/tbb/parallel_for.h>
#include <tbb/tbb.h>

#include "mergeSort.hpp"
#include "quickSort.hpp"
#include "radixSort.hpp"

// #include "quickSort_proposal.hpp"
// #include "radixSort_proposal.hpp"

void printVector(std::vector<int> vec) {
    for (size_t i = 0; i < vec.size(); i++) {
        std::cout << vec[i] << " ";
    }
    std::cout << std::endl;
}

int main() {
    size_t size = 50;
    std::vector<int> to_sort(size);

    srand(time(NULL));

    generate(to_sort.begin(), to_sort.end(), []() { return rand() % 100; });

    std::cout << "****MERGESORT****" << std::endl;

    std::cout << "Unsorted: ";
    printVector(to_sort);

    tbb::tick_count t0 = tbb::tick_count::now();
    auto result_merge = mergeSort(to_sort, to_sort.size());
    tbb::tick_count t1 = tbb::tick_count::now();

    std::cout << "Sorted: ";
    printVector(result_merge);
    std::cout << "Time: " << (t1 - t0).seconds() << std::endl;

    std::cout << "****QUICKSORT****" << std::endl;
    std::cout << "Unsorted: ";
    printVector(to_sort);

    int high = size - 1;

    std::vector<int> to_sort_copy(to_sort);
    t0 = tbb::tick_count::now();
    quickSort(to_sort_copy, 0, high);
    t1 = tbb::tick_count::now();

    std::cout << "\nSorted: ";
    printVector(to_sort_copy);
    std::cout << "Time: " << (t1 - t0).seconds() << std::endl;

    std::cout << "****RADIXSORT****" << std::endl;

    std::cout << "Unsorted: ";
    printVector(to_sort);

    t0 = tbb::tick_count::now();
    auto result_radix = radixSort(to_sort, size);
    t1 = tbb::tick_count::now();

    std::cout << "\nSorted: ";
    printVector(result_radix);
    std::cout << "Time: " << (t1 - t0).seconds() << std::endl;
}